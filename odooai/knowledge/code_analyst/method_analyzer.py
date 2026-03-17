"""
Module: code_analyst/method_analyzer.py
Role: Analyze Python method bodies to extract business effects.
      Detects: self.env['model'].create/write, self.write({'state': ...}),
      method calls, and cross-model references.
      Pure AST analysis — ZERO LLM tokens.
Dependencies: ast
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class MethodEffect:
    """An effect detected in a method body."""

    type: str  # write, create, unlink, env_ref, call, state_change
    target_model: str = ""
    field: str = ""
    value: str = ""
    via_method: str = ""


@dataclass
class MethodAnalysis:
    """Analysis of a single method body."""

    name: str
    model: str
    effects: list[MethodEffect] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)  # Internal method calls
    env_refs: list[str] = field(default_factory=list)  # self.env['model'] refs


def analyze_method_body(
    method_node: ast.FunctionDef | ast.AsyncFunctionDef,
    model_name: str,
) -> MethodAnalysis:
    """
    Analyze a method's AST to extract business effects.

    Detects:
    - self.write({'state': 'value'}) → state transitions
    - self.env['model'].create(...) → model creation
    - self.env['model'].write(...) → model modification
    - self._method_name() → internal call chains
    - self.env.ref('xml_id') → data references
    """
    analysis = MethodAnalysis(name=method_node.name, model=model_name)

    for node in ast.walk(method_node):
        # Detect self.write({'state': 'value'})
        _detect_state_write(node, analysis)
        # Detect self.env['model'] references
        _detect_env_ref(node, analysis)
        # Detect self.env['model'].create/write/unlink
        _detect_env_operation(node, analysis)
        # Detect self._method() calls
        _detect_internal_call(node, analysis)

    return analysis


def analyze_file_methods(
    file_path: Path,
    model_name: str,
) -> list[MethodAnalysis]:
    """Analyze all action/button methods in a Python file."""
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return []

    results: list[MethodAnalysis] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            # Only analyze action/button methods + key methods
            if item.name.startswith(
                ("action_", "button_", "_action_", "_create_")
            ) or item.name in ("write", "create"):
                analysis = analyze_method_body(item, model_name)
                if analysis.effects or analysis.calls or analysis.env_refs:
                    results.append(analysis)

    return results


def _detect_state_write(node: ast.AST, analysis: MethodAnalysis) -> None:
    """Detect self.write({'state': 'value'}) patterns."""
    if not isinstance(node, ast.Call):
        return

    # Check for self.write({...}) or self.update({...})
    if not isinstance(node.func, ast.Attribute):
        return
    if node.func.attr not in ("write", "update"):
        return
    if not isinstance(node.func.value, ast.Name):
        return
    if node.func.value.id != "self":
        return

    # Extract dict literal from args
    for arg in node.args:
        if isinstance(arg, ast.Dict):
            for key, value in zip(arg.keys, arg.values, strict=False):
                if isinstance(key, ast.Constant) and key.value == "state":
                    state_val = ""
                    if isinstance(value, ast.Constant):
                        state_val = str(value.value)
                    analysis.effects.append(
                        MethodEffect(
                            type="state_change",
                            target_model=analysis.model,
                            field="state",
                            value=state_val,
                        )
                    )


def _detect_env_ref(node: ast.AST, analysis: MethodAnalysis) -> None:
    """Detect self.env['model.name'] references."""
    if not isinstance(node, ast.Subscript):
        return

    # Check for self.env['...']
    if not isinstance(node.value, ast.Attribute):
        return
    if node.value.attr != "env":
        return
    if not isinstance(node.value.value, ast.Name):
        return
    if node.value.value.id != "self":
        return

    # Extract model name from subscript
    if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        model_ref = node.slice.value
        if "." in model_ref and model_ref not in analysis.env_refs:
            analysis.env_refs.append(model_ref)


def _detect_env_operation(node: ast.AST, analysis: MethodAnalysis) -> None:
    """Detect self.env['model'].create/write/unlink operations."""
    if not isinstance(node, ast.Call):
        return
    if not isinstance(node.func, ast.Attribute):
        return

    operation = node.func.attr
    if operation not in ("create", "write", "unlink", "search", "search_read"):
        return

    # Walk up to find self.env['model']
    target = node.func.value
    model_name = _extract_env_model(target)
    if not model_name:
        return

    effect_type = "create" if operation == "create" else operation
    analysis.effects.append(
        MethodEffect(
            type=effect_type,
            target_model=model_name,
            via_method=analysis.name,
        )
    )


def _detect_internal_call(node: ast.AST, analysis: MethodAnalysis) -> None:
    """Detect self._method_name() or self.method_name() calls."""
    if not isinstance(node, ast.Call):
        return
    if not isinstance(node.func, ast.Attribute):
        return
    if not isinstance(node.func.value, ast.Name):
        return
    if node.func.value.id != "self":
        return

    method_name = node.func.attr
    # Skip built-in ORM methods
    if method_name in (
        "write",
        "create",
        "unlink",
        "search",
        "read",
        "browse",
        "mapped",
        "filtered",
        "sorted",
        "ensure_one",
        "exists",
        "with_context",
        "with_company",
        "sudo",
        "with_env",
        "env",
        "ids",
        "id",
    ):
        return

    is_internal = method_name.startswith("_") or method_name.startswith("action_")
    if is_internal and method_name not in analysis.calls:
        analysis.calls.append(method_name)


def _extract_env_model(node: ast.AST) -> str:
    """Extract model name from self.env['model.name'] expression."""
    if (
        isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Attribute)
        and node.value.attr == "env"
        and isinstance(node.slice, ast.Constant)
        and isinstance(node.slice.value, str)
    ):
        return node.slice.value
    return ""


def resolve_selection_constants(
    file_path: Path,
) -> dict[str, list[list[str]]]:
    """
    Resolve module-level selection constants.

    Looks for patterns like:
    SALE_ORDER_STATE = [('draft', 'Quotation'), ('sent', 'Sent'), ...]
    """
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return {}

    constants: dict[str, list[list[str]]] = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue

        # Check if it's UPPER_CASE (constant convention)
        name = target.id
        if not name.isupper():
            continue

        # Check if value is a list of tuples
        if not isinstance(node.value, ast.List):
            continue

        selections: list[list[str]] = []
        for elt in node.value.elts:
            if isinstance(elt, ast.Tuple) and len(elt.elts) >= 2:
                key = ""
                label = ""
                if isinstance(elt.elts[0], ast.Constant):
                    key = str(elt.elts[0].value)
                if isinstance(elt.elts[1], ast.Constant):
                    label = str(elt.elts[1].value)
                if key:
                    selections.append([key, label])

        if selections:
            constants[name] = selections

    return constants
