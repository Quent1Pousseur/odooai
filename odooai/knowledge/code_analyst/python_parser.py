"""
Module: knowledge/code_analyst/python_parser.py
Role: Parse Odoo Python source files via AST to extract models, fields, and methods.
      Uses ast.parse (safe — no code execution) to analyze the syntax tree.
Dependencies: ast (stdlib), _field_parser
"""

from __future__ import annotations

import ast
import contextlib
from pathlib import Path
from typing import Any

import structlog

from odooai.knowledge.code_analyst._field_parser import extract_fields
from odooai.knowledge.schemas.actions import ActionMethod
from odooai.knowledge.schemas.constraints import OnchangeMethod, PythonConstraint, SqlConstraint
from odooai.knowledge.schemas.models import ModelDefinition

logger = structlog.get_logger(__name__)

_MODEL_BASES = {"Model", "TransientModel", "AbstractModel"}


def parse_python_file(
    file_path: Path,
    module_name: str,
) -> tuple[
    list[ModelDefinition],
    list[ActionMethod],
    list[PythonConstraint],
    list[OnchangeMethod],
    list[SqlConstraint],
]:
    """
    Parse a single Python file and extract Odoo model definitions.

    Returns:
        Tuple of (models, action_methods, python_constraints,
                  onchange_methods, sql_constraints).
    """
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as exc:
        logger.warning("Syntax error in Python file", path=str(file_path), error=str(exc))
        return [], [], [], [], []

    models: list[ModelDefinition] = []
    actions: list[ActionMethod] = []
    constraints: list[PythonConstraint] = []
    onchanges: list[OnchangeMethod] = []
    sql_constraints: list[SqlConstraint] = []

    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        if not _is_odoo_model(node):
            continue

        result = _parse_model_class(node, module_name)
        if result[0]:
            models.append(result[0])
            actions.extend(result[1])
            constraints.extend(result[2])
            onchanges.extend(result[3])
            sql_constraints.extend(result[4])

    return models, actions, constraints, onchanges, sql_constraints


def _is_odoo_model(node: ast.ClassDef) -> bool:
    """Check if a class inherits from an Odoo model base class."""
    for base in node.bases:
        if isinstance(base, ast.Attribute) and base.attr in _MODEL_BASES:
            return True
        if isinstance(base, ast.Name) and base.id in _MODEL_BASES:
            return True
    return False


def _get_base_type(node: ast.ClassDef) -> str:
    """Determine the base type (Model, TransientModel, AbstractModel)."""
    for base in node.bases:
        if isinstance(base, ast.Attribute) and base.attr in _MODEL_BASES:
            return str(base.attr)
        if isinstance(base, ast.Name) and base.id in _MODEL_BASES:
            return str(base.id)
    return "Model"


def _parse_model_class(
    node: ast.ClassDef,
    module_name: str,
) -> tuple[
    ModelDefinition | None,
    list[ActionMethod],
    list[PythonConstraint],
    list[OnchangeMethod],
    list[SqlConstraint],
]:
    """Parse a single Odoo model class definition."""
    base_type = _get_base_type(node)
    attrs = _extract_class_attributes(node)

    model_name = str(attrs.get("_name", ""))
    inherit = attrs.get("_inherit", [])
    if isinstance(inherit, str):
        inherit = [inherit]

    # _inherit without _name = extension (Odoo Expert requirement #3)
    is_extension = bool(inherit) and not model_name
    if is_extension:
        model_name = inherit[0] if inherit else node.name

    if not model_name:
        return None, [], [], [], []

    fields = extract_fields(node)
    actions, constraints, onchanges = _extract_methods(node, model_name)
    sql_constraints = _extract_sql_constraints(node)

    # _inherits (delegation — Odoo Expert requirement #1)
    inherits_raw = attrs.get("_inherits", {})
    inherits = inherits_raw if isinstance(inherits_raw, dict) else {}

    model = ModelDefinition(
        name=model_name,
        description=str(attrs.get("_description", "")),
        inherit=[str(i) for i in inherit],
        inherits={str(k): str(v) for k, v in inherits.items()},
        is_transient=base_type == "TransientModel",
        is_abstract=base_type == "AbstractModel",
        is_extension=is_extension,
        fields=fields,
        order=str(attrs.get("_order", "")),
        rec_name=str(attrs.get("_rec_name", "")),
        table=str(attrs.get("_table", "")),
    )

    return model, actions, constraints, onchanges, sql_constraints


def _extract_class_attributes(node: ast.ClassDef) -> dict[str, Any]:
    """Extract class-level assignments (_name, _inherit, _inherits, etc.)."""
    attrs: dict[str, Any] = {}
    for item in node.body:
        if isinstance(item, ast.Assign) and len(item.targets) == 1:
            target = item.targets[0]
            if isinstance(target, ast.Name) and target.id.startswith("_"):
                with contextlib.suppress(ValueError, TypeError):
                    attrs[target.id] = ast.literal_eval(item.value)
    return attrs


def _extract_methods(
    node: ast.ClassDef,
    model_name: str,
) -> tuple[list[ActionMethod], list[PythonConstraint], list[OnchangeMethod]]:
    """Extract action methods, constraints, and onchange methods."""
    actions: list[ActionMethod] = []
    constraints: list[PythonConstraint] = []
    onchanges: list[OnchangeMethod] = []

    for item in node.body:
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        decorators = _get_decorator_names(item)
        docstring = ast.get_docstring(item) or ""

        constrains_fields = _get_decorator_args(item, "constrains")
        if constrains_fields:
            constraints.append(
                PythonConstraint(
                    method_name=item.name,
                    fields=constrains_fields,
                    docstring=docstring,
                )
            )

        onchange_fields = _get_decorator_args(item, "onchange")
        if onchange_fields:
            onchanges.append(
                OnchangeMethod(
                    method_name=item.name,
                    fields=onchange_fields,
                    docstring=docstring,
                )
            )

        if item.name.startswith(("action_", "button_")):
            actions.append(
                ActionMethod(
                    name=item.name,
                    model=model_name,
                    docstring=docstring,
                    decorators=decorators,
                )
            )

    return actions, constraints, onchanges


def _get_decorator_names(func: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Get list of decorator names as strings."""
    names: list[str] = []
    for dec in func.decorator_list:
        if isinstance(dec, ast.Attribute):
            names.append(f"api.{dec.attr}" if isinstance(dec.value, ast.Name) else str(dec.attr))
        elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
            names.append(f"api.{dec.func.attr}")
        elif isinstance(dec, ast.Name):
            names.append(dec.id)
    return names


def _get_decorator_args(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    decorator_name: str,
) -> list[str]:
    """Get args of @api.constrains('f1', 'f2') or @api.onchange('f1')."""
    for dec in func.decorator_list:
        if (
            isinstance(dec, ast.Call)
            and isinstance(dec.func, ast.Attribute)
            and dec.func.attr == decorator_name
        ):
            return [str(ast.literal_eval(a)) for a in dec.args if _is_string_literal(a)]
    return []


def _is_string_literal(node: ast.expr) -> bool:
    """Check if an AST node is a string literal."""
    try:
        return isinstance(ast.literal_eval(node), str)
    except (ValueError, TypeError):
        return False


def _extract_sql_constraints(node: ast.ClassDef) -> list[SqlConstraint]:
    """Extract _sql_constraints from a class."""
    for item in node.body:
        if (
            isinstance(item, ast.Assign)
            and len(item.targets) == 1
            and isinstance(item.targets[0], ast.Name)
            and item.targets[0].id == "_sql_constraints"
        ):
            try:
                raw = ast.literal_eval(item.value)
                if isinstance(raw, list):
                    return [
                        SqlConstraint(
                            name=str(c[0]),
                            sql=str(c[1]),
                            message=str(c[2]),
                        )
                        for c in raw
                        if isinstance(c, (list, tuple)) and len(c) >= 3
                    ]
            except (ValueError, TypeError):
                pass
    return []
