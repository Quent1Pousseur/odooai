"""
Module: knowledge/code_analyst/xml_parser.py
Role: Parse Odoo XML files (views, security, menus) and CSV (access rights).
Dependencies: xml.etree.ElementTree (stdlib), csv (stdlib)
"""

from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from pathlib import Path

import structlog

from odooai.knowledge.schemas.menus import MenuItem
from odooai.knowledge.schemas.security import AccessRight, RecordRule, SecurityGroup
from odooai.knowledge.schemas.views import ViewDefinition, ViewField

logger = structlog.get_logger(__name__)


def parse_access_csv(file_path: Path) -> list[AccessRight]:
    """Parse ir.model.access.csv into AccessRight schemas."""
    if not file_path.exists():
        return []
    try:
        with file_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rights: list[AccessRight] = []
            for row in reader:
                rights.append(
                    AccessRight(
                        id=row.get("id", ""),
                        model=row.get("model_id:id", "").replace("model_", "").replace("_", "."),
                        group=row.get("group_id:id", ""),
                        perm_read=row.get("perm_read", "0") == "1",
                        perm_write=row.get("perm_write", "0") == "1",
                        perm_create=row.get("perm_create", "0") == "1",
                        perm_unlink=row.get("perm_unlink", "0") == "1",
                    )
                )
            return rights
    except Exception as exc:
        logger.warning("Failed to parse access CSV", path=str(file_path), error=str(exc))
        return []


def parse_xml_file(
    file_path: Path,
) -> tuple[list[ViewDefinition], list[RecordRule], list[SecurityGroup], list[MenuItem]]:
    """
    Parse an Odoo XML data file.

    Extracts views, record rules, security groups, and menus.
    Best-effort: logs errors and returns partial results.

    Returns:
        Tuple of (views, record_rules, security_groups, menus).
    """
    if not file_path.exists():
        return [], [], [], []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as exc:
        logger.warning("Failed to parse XML", path=str(file_path), error=str(exc))
        return [], [], [], []

    views: list[ViewDefinition] = []
    rules: list[RecordRule] = []
    groups: list[SecurityGroup] = []
    menus: list[MenuItem] = []

    for record in root.iter("record"):
        model = record.get("model", "")
        if model == "ir.ui.view":
            view = _parse_view_record(record)
            if view:
                views.append(view)
        elif model == "ir.rule":
            rule = _parse_rule_record(record)
            if rule:
                rules.append(rule)
        elif model == "res.groups":
            group = _parse_group_record(record)
            if group:
                groups.append(group)

    for menuitem in root.iter("menuitem"):
        menu = _parse_menuitem(menuitem)
        if menu:
            menus.append(menu)

    return views, rules, groups, menus


def _parse_view_record(record: ET.Element) -> ViewDefinition | None:
    """Parse a single ir.ui.view record."""
    fields = _get_field_dict(record)
    view_id = record.get("id", "")
    name = fields.get("name", "")
    model = fields.get("model", "")
    view_type = fields.get("type", "form")
    inherit_id = fields.get("inherit_id", "")

    if not model and not inherit_id:
        return None

    # Extract field references from arch
    arch_fields: list[ViewField] = []
    arch = record.find(".//field[@name='arch']")
    if arch is not None:
        arch_fields = _extract_view_fields(arch)
        if not view_type or view_type == "form":
            view_type = _detect_view_type(arch)

    return ViewDefinition(
        id=view_id,
        name=name,
        model=model,
        type=view_type,
        inherit_id=inherit_id,
        is_inherited=bool(inherit_id),
        fields=arch_fields,
    )


def _parse_rule_record(record: ET.Element) -> RecordRule | None:
    """Parse a single ir.rule record."""
    fields = _get_field_dict(record)
    return RecordRule(
        id=record.get("id", ""),
        name=fields.get("name", ""),
        model=fields.get("model_id", ""),
        domain=fields.get("domain_force", "[]"),
        groups=[g.strip() for g in fields.get("groups", "").split(",") if g.strip()],
    )


def _parse_group_record(record: ET.Element) -> SecurityGroup | None:
    """Parse a single res.groups record."""
    fields = _get_field_dict(record)
    return SecurityGroup(
        id=record.get("id", ""),
        name=fields.get("name", ""),
        category=fields.get("category_id", ""),
        comment=fields.get("comment", ""),
    )


def _parse_menuitem(elem: ET.Element) -> MenuItem | None:
    """Parse a <menuitem> shortcut element."""
    menu_id = elem.get("id", "")
    if not menu_id:
        return None
    return MenuItem(
        id=menu_id,
        name=elem.get("name", ""),
        parent_id=elem.get("parent", ""),
        action=elem.get("action", ""),
        sequence=int(elem.get("sequence", "10")),
        groups=[g.strip() for g in elem.get("groups", "").split(",") if g.strip()],
    )


def _get_field_dict(record: ET.Element) -> dict[str, str]:
    """Extract field name→value mapping from a <record> element."""
    result: dict[str, str] = {}
    for field in record.findall("field"):
        name = field.get("name", "")
        # Value can be in text, ref attribute, or eval attribute
        value = field.text or field.get("ref", "") or field.get("eval", "")
        if name:
            result[name] = value.strip() if value else ""
    return result


def _extract_view_fields(arch_elem: ET.Element) -> list[ViewField]:
    """Extract field references from a view arch XML."""
    fields: list[ViewField] = []
    for field in arch_elem.iter("field"):
        name = field.get("name", "")
        if name:
            fields.append(
                ViewField(
                    name=name,
                    widget=field.get("widget", ""),
                    invisible=field.get("invisible", ""),
                    readonly=field.get("readonly", ""),
                    required=field.get("required", ""),
                )
            )
    return fields


def _detect_view_type(arch_elem: ET.Element) -> str:
    """Detect view type from arch content."""
    for tag in ("form", "tree", "kanban", "search", "pivot", "graph", "calendar"):
        if arch_elem.find(f".//{tag}") is not None:
            return tag
    return "form"
