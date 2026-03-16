"""
Module: knowledge/schemas/menus.py
Role: Schemas for Odoo menu hierarchy.
Dependencies: pydantic
"""

from pydantic import BaseModel


class MenuItem(BaseModel, frozen=True):
    """Menu item from XML definitions."""

    id: str  # External ID
    name: str
    parent_id: str = ""  # Parent menu external ID
    action: str = ""  # Window action reference
    sequence: int = 10
    groups: list[str] = []  # Access groups
