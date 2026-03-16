"""
Module: knowledge/schemas/views.py
Role: Schemas for Odoo view definitions extracted from XML.
Dependencies: pydantic
"""

from pydantic import BaseModel


class ViewField(BaseModel, frozen=True):
    """A field reference found in a view."""

    name: str
    widget: str = ""
    invisible: str = ""  # Invisible condition
    readonly: str = ""  # Readonly condition
    required: str = ""  # Required condition


class ViewDefinition(BaseModel, frozen=True):
    """View definition extracted from XML."""

    id: str  # External ID
    name: str
    model: str
    type: str  # form, tree, kanban, search, pivot, graph, calendar
    inherit_id: str = ""  # Parent view (empty = root view)
    is_inherited: bool = False  # True if this extends another view
    priority: int = 16  # View priority
    fields: list[ViewField] = []  # Fields referenced in the view
    arch_summary: str = ""  # Brief description of view structure
