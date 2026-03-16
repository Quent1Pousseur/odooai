"""
Module: agents/_tools.py
Role: Define and execute Odoo tools for LLM tool-use pattern.
      Each tool call is validated by the Guardian before execution.
Dependencies: security/guardian, infrastructure/odoo
"""

from __future__ import annotations

from typing import Any

import structlog

from odooai.agents.orchestrator import guarded_odoo_read, guarded_odoo_write_check
from odooai.domain.ports.i_odoo_client import IOdooClient

logger = structlog.get_logger(__name__)

# Max tool calls per question to prevent infinite loops and cost blowup
MAX_TOOL_CALLS = 3

# Tools exposed to the LLM
TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "odoo_search_read",
        "description": (
            "Search and read records from the client's Odoo database. "
            "Returns a list of records with the requested fields. "
            "Use this to answer questions about the client's data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": "Odoo model technical name (e.g. 'sale.order', 'account.move')",
                },
                "domain": {
                    "type": "array",
                    "description": "Odoo domain filter (e.g. [['state','=','draft']])",
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fields to return (e.g. ['name','state','amount_total'])",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max records to return (default 10)",
                    "default": 10,
                },
            },
            "required": ["model", "domain", "fields"],
        },
    },
    {
        "name": "odoo_search_count",
        "description": (
            "Count records matching a filter in the client's Odoo database. "
            "Use this to answer 'how many' questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Odoo model technical name"},
                "domain": {"type": "array", "description": "Odoo domain filter"},
            },
            "required": ["model", "domain"],
        },
    },
]


async def execute_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    odoo_client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """
    Execute a tool call from the LLM, with Guardian validation.

    Returns a string result to feed back to the LLM.
    """
    try:
        if tool_name == "odoo_search_read":
            return await _exec_search_read(tool_input, odoo_client, uid, api_key)
        if tool_name == "odoo_search_count":
            return await _exec_search_count(tool_input, odoo_client, uid, api_key)
        return f"Unknown tool: {tool_name}"
    except Exception as exc:
        user_msg = getattr(exc, "user_message", str(exc))
        logger.warning("Tool execution failed", tool=tool_name, error=user_msg)
        return f"Erreur: {user_msg}"


async def _exec_search_read(
    inp: dict[str, Any],
    client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """Execute odoo_search_read with Guardian validation."""
    model = str(inp.get("model", ""))
    domain = inp.get("domain", [])
    fields = inp.get("fields", ["name"])
    limit = min(int(inp.get("limit", 10)), 20)  # Cap at 20

    # Guardian gates
    guarded_odoo_write_check(model, "search_read", domain)

    # Execute
    raw = await client.search_read(api_key, model, domain, fields, limit=limit, uid=uid)

    # Sanitize
    result = guarded_odoo_read(model, raw, fields, uid=uid)

    # Format for LLM
    if not result.records:
        return f"Aucun enregistrement trouve pour {model} avec ce filtre."

    lines = [f"{len(result.records)} enregistrement(s) {model} :"]
    for r in result.records:
        parts = [f"{k}={v}" for k, v in r.items() if k != "id"]
        lines.append(f"  - {', '.join(parts)}")

    if result.was_anonymized:
        lines.append("(Donnees anonymisees pour raisons de securite)")

    return "\n".join(lines)


async def _exec_search_count(
    inp: dict[str, Any],
    client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """Execute odoo_search_count with Guardian validation."""
    model = str(inp.get("model", ""))
    domain = inp.get("domain", [])

    # Guardian gates
    guarded_odoo_write_check(model, "search_count", domain)

    # Execute
    count = await client.search_count(api_key, model, domain, uid=uid)

    return f"{count} enregistrement(s) {model} correspondent a ce filtre."
