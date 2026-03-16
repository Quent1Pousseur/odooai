"""
Module: agents/_live_context.py
Role: Fetch live data from an Odoo instance for domain-specific context.
Dependencies: domain ports, security guardian
"""

from __future__ import annotations

from typing import Any

import structlog

from odooai.agents.orchestrator import guarded_odoo_read
from odooai.domain.ports.i_odoo_client import IOdooClient

logger = structlog.get_logger(__name__)


async def fetch_live_context(
    odoo_client: Any,
    uid: int,
    api_key: str,
    domain_id: str,
) -> str:
    """Fetch relevant live data from Odoo instance for the detected domain."""
    if not isinstance(odoo_client, IOdooClient):
        return ""

    parts: list[str] = []

    try:
        if domain_id == "sales_crm":
            data = guarded_odoo_read(
                "sale.order",
                await odoo_client.search_read(
                    api_key,
                    "sale.order",
                    [("state", "in", ["draft", "sent", "sale"])],
                    ["name", "state", "partner_id", "amount_total", "date_order"],
                    limit=10,
                    uid=uid,
                ),
                ["name", "state", "partner_id", "amount_total", "date_order"],
                uid=uid,
            )
            parts.append(f"Dernieres commandes ({data.record_count}) :")
            for r in data.records:
                parts.append(f"  - {r.get('name')} | {r.get('state')} | {r.get('amount_total')}")

        elif domain_id == "supply_chain":
            data = guarded_odoo_read(
                "stock.picking",
                await odoo_client.search_read(
                    api_key,
                    "stock.picking",
                    [("state", "not in", ["done", "cancel"])],
                    ["name", "state", "partner_id", "scheduled_date"],
                    limit=10,
                    uid=uid,
                ),
                ["name", "state", "partner_id", "scheduled_date"],
                uid=uid,
            )
            parts.append(f"Transferts en cours ({data.record_count}) :")
            for r in data.records:
                parts.append(f"  - {r.get('name')} | {r.get('state')}")

        elif domain_id == "accounting":
            data = guarded_odoo_read(
                "account.move",
                await odoo_client.search_read(
                    api_key,
                    "account.move",
                    [("state", "=", "draft"), ("move_type", "=", "out_invoice")],
                    ["name", "partner_id", "amount_total", "invoice_date_due"],
                    limit=10,
                    uid=uid,
                ),
                ["name", "partner_id", "amount_total", "invoice_date_due"],
                uid=uid,
            )
            parts.append(f"Factures brouillon ({data.record_count}) :")
            for r in data.records:
                parts.append(f"  - {r.get('name')} | {r.get('amount_total')}")

    except Exception as exc:
        logger.warning("Failed to fetch live data", domain=domain_id, error=str(exc))
        parts.append(f"(Donnees live non disponibles : {type(exc).__name__})")

    return "\n".join(parts) if parts else ""
