"""
Module: knowledge/code_analyst/_field_parser.py
Role: Parse Odoo field definitions from AST nodes.
Dependencies: ast (stdlib)
"""

from __future__ import annotations

import ast
from typing import Any

from odooai.knowledge.schemas.models import FieldDefinition

# Odoo field type classes → technical type name
FIELD_TYPES: dict[str, str] = {
    "Char": "char",
    "Text": "text",
    "Html": "html",
    "Integer": "integer",
    "Float": "float",
    "Boolean": "boolean",
    "Date": "date",
    "Datetime": "datetime",
    "Binary": "binary",
    "Selection": "selection",
    "Many2one": "many2one",
    "One2many": "one2many",
    "Many2many": "many2many",
    "Monetary": "monetary",
    "Reference": "reference",
    "Image": "binary",
}


def extract_fields(node: ast.ClassDef) -> dict[str, FieldDefinition]:
    """Extract Odoo field definitions from a class body."""
    fields: dict[str, FieldDefinition] = {}
    for item in node.body:
        if not isinstance(item, ast.Assign) or len(item.targets) != 1:
            continue
        target = item.targets[0]
        if not isinstance(target, ast.Name) or target.id.startswith("_"):
            continue
        field = _parse_field_assignment(target.id, item.value)
        if field:
            fields[field.name] = field
    return fields


def _parse_field_assignment(name: str, value: ast.expr) -> FieldDefinition | None:
    """Parse: name = fields.Char(string='Name', required=True)."""
    if not isinstance(value, ast.Call):
        return None

    field_type = _get_field_type(value.func)
    if not field_type:
        return None

    kwargs = _extract_call_kwargs(value)

    # Odoo Expert requirement #4: computed fields default to store=False
    compute = kwargs.get("compute")
    store = kwargs.get("store", True)
    if compute and "store" not in kwargs:
        store = False

    return FieldDefinition(
        name=name,
        type=field_type,
        string=str(kwargs.get("string", "")),
        required=bool(kwargs.get("required", False)),
        readonly=bool(kwargs.get("readonly", False)),
        store=bool(store),
        compute=str(compute) if compute else None,
        depends=kwargs.get("depends", []),
        related=str(kwargs.get("related")) if kwargs.get("related") else None,
        relation=str(kwargs.get("comodel_name", "")) or None,
        selection=kwargs.get("selection", []),
        default=str(kwargs.get("default")) if kwargs.get("default") is not None else None,
        help=str(kwargs.get("help", "")),
        comodel_name=str(kwargs.get("comodel_name", "")) or None,
        inverse_name=str(kwargs.get("inverse_name", "")) or None,
    )


def _get_field_type(func: ast.expr) -> str | None:
    """Extract Odoo field type from AST call function node."""
    if isinstance(func, ast.Attribute) and isinstance(func.attr, str):
        return FIELD_TYPES.get(func.attr)
    return None


def _extract_call_kwargs(call: ast.Call) -> dict[str, Any]:
    """Extract keyword arguments from an AST Call node."""
    kwargs: dict[str, Any] = {}

    # First positional arg is often comodel_name or selection
    if call.args:
        try:
            first = ast.literal_eval(call.args[0])
            if isinstance(first, str):
                kwargs["comodel_name"] = first
            elif isinstance(first, list):
                kwargs["selection"] = first
        except (ValueError, TypeError):
            pass

    for kw in call.keywords:
        if kw.arg is None:
            continue
        try:
            kwargs[kw.arg] = ast.literal_eval(kw.value)
        except (ValueError, TypeError):
            # Non-literal value (lambda, function ref, etc.)
            # Store name references cleanly, skip complex expressions
            if isinstance(kw.value, ast.Name):
                kwargs[kw.arg] = kw.value.id

    return kwargs
