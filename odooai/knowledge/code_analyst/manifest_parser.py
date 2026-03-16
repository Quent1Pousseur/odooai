"""
Module: knowledge/code_analyst/manifest_parser.py
Role: Parse Odoo __manifest__.py files safely using ast.literal_eval.
      Never uses eval() — only parses literal Python expressions.
Dependencies: ast (stdlib)
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import structlog

from odooai.knowledge.schemas.manifest import ModuleManifest

logger = structlog.get_logger(__name__)


def parse_manifest(module_path: Path) -> ModuleManifest | None:
    """
    Parse __manifest__.py from an Odoo module directory.

    Uses ast.literal_eval for security — only parses literal expressions
    (dicts, lists, strings, numbers, booleans). No code execution.

    Args:
        module_path: Path to the Odoo module root directory.

    Returns:
        ModuleManifest or None if parsing fails (best-effort).
    """
    manifest_file = module_path / "__manifest__.py"
    if not manifest_file.exists():
        logger.warning("No __manifest__.py found", path=str(module_path))
        return None

    try:
        content = manifest_file.read_text(encoding="utf-8")
        data = ast.literal_eval(content)
    except (ValueError, SyntaxError) as exc:
        logger.error(
            "Failed to parse __manifest__.py",
            path=str(manifest_file),
            error=str(exc),
        )
        return None

    if not isinstance(data, dict):
        logger.error("Manifest is not a dict", path=str(manifest_file))
        return None

    technical_name = module_path.name

    return _dict_to_manifest(data, technical_name)


def _dict_to_manifest(data: dict[str, Any], technical_name: str) -> ModuleManifest:
    """Convert a manifest dict to a ModuleManifest schema."""
    return ModuleManifest(
        name=str(data.get("name", technical_name)),
        technical_name=technical_name,
        version=str(data.get("version", "")),
        category=str(data.get("category", "")),
        summary=str(data.get("summary", "")),
        description=str(data.get("description", "")),
        author=str(data.get("author", "")),
        website=str(data.get("website", "")),
        depends=_ensure_str_list(data.get("depends", [])),
        installable=bool(data.get("installable", True)),
        application=bool(data.get("application", False)),
        license=str(data.get("license", "")),
    )


def _ensure_str_list(value: Any) -> list[str]:
    """Ensure a value is a list of strings."""
    if isinstance(value, list):
        return [str(item) for item in value]
    return []
