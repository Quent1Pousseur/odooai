"""
Module: domain/value_objects/odoo_user_info.py
Role: Immutable representation of an authenticated Odoo user.
Dependencies: none (pure Python)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OdooUserInfo:
    """Authenticated Odoo user information returned after login."""

    uid: int
    login: str
    name: str
    is_system: bool
    is_internal: bool
    lang: str
    tz: str
