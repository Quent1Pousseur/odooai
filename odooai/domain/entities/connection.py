"""
Module: domain/entities/connection.py
Role: Mutable entity representing an Odoo instance connection.
Dependencies: none (pure Python)
"""

from dataclasses import dataclass
from enum import StrEnum


class OdooApiType(StrEnum):
    """Odoo API protocol type."""

    XML_RPC = "xml_rpc"
    JSON_RPC = "json_rpc"


@dataclass
class OdooConnection:
    """Configuration for connecting to an Odoo instance."""

    url: str
    database: str
    api_type: OdooApiType
    version: str | None = None
