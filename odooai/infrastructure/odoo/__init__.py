"""Odoo API connectors (XML-RPC and JSON-2)."""

from odooai.infrastructure.odoo._http import close_http_pool
from odooai.infrastructure.odoo.client import OdooClient

__all__ = ["OdooClient", "close_http_pool"]
