"""
Module: knowledge/schemas/security.py
Role: Schemas for Odoo security definitions (ACL, record rules, groups).
Dependencies: pydantic
"""

from pydantic import BaseModel


class AccessRight(BaseModel, frozen=True):
    """Access control list entry from ir.model.access.csv."""

    id: str  # External ID
    model: str  # Model technical name
    group: str = ""  # Group external ID (empty = public)
    perm_read: bool = False
    perm_write: bool = False
    perm_create: bool = False
    perm_unlink: bool = False


class RecordRule(BaseModel, frozen=True):
    """Record rule from XML security definitions."""

    id: str
    name: str
    model: str
    domain: str = "[]"  # Domain filter expression
    groups: list[str] = []  # Group external IDs
    perm_read: bool = True
    perm_write: bool = True
    perm_create: bool = True
    perm_unlink: bool = True


class SecurityGroup(BaseModel, frozen=True):
    """Security group definition from XML."""

    id: str  # External ID
    name: str
    category: str = ""
    implied_ids: list[str] = []  # Inherited groups
    comment: str = ""
