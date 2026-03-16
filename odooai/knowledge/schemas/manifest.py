"""
Module: knowledge/schemas/manifest.py
Role: Schema for Odoo module manifest (__manifest__.py).
Dependencies: pydantic
"""

from pydantic import BaseModel


class ModuleManifest(BaseModel, frozen=True):
    """Metadata extracted from __manifest__.py."""

    name: str
    technical_name: str
    version: str = ""
    category: str = ""
    summary: str = ""
    description: str = ""
    author: str = ""
    website: str = ""
    depends: list[str] = []
    installable: bool = True
    application: bool = False
    license: str = ""
