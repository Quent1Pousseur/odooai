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
MAX_TOOL_CALLS = 10

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
    {
        "name": "odoo_read_group",
        "description": (
            "Group and aggregate records from Odoo. "
            "Use this for statistics: totals, averages, counts by group. "
            "Example: total revenue by salesperson, count of orders by state."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": "Odoo model technical name",
                },
                "domain": {
                    "type": "array",
                    "description": "Odoo domain filter",
                },
                "groupby": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fields to group by (e.g. ['state', 'user_id'])",
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fields to aggregate (e.g. ['amount_total:sum'])",
                },
            },
            "required": ["model", "domain", "groupby", "fields"],
        },
    },
    {
        "name": "odoo_fields_get",
        "description": (
            "Get the list of fields available on an Odoo model. "
            "Use this BEFORE search_read if you are not sure which fields exist. "
            "Returns field names with their types."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": "Odoo model technical name (e.g. 'sale.order')",
                },
            },
            "required": ["model"],
        },
    },
]


def _normalize_domain(domain: Any) -> list[Any]:
    """
    Normalize LLM-generated domains to valid Odoo format.

    The LLM sometimes generates:
    - Nested lists: [["field", "=", "value"]] (correct)
    - Flat tuples: [("field", "=", "value")] (correct)
    - Dicts: [{"field": "state", "operator": "=", "value": "draft"}] (wrong)
    - Strings: "[('field','=','value')]" (wrong)
    """
    if isinstance(domain, str):
        # Try to parse string representation
        try:
            import ast

            parsed = ast.literal_eval(domain)
            if isinstance(parsed, list):
                return parsed
        except (ValueError, SyntaxError):
            pass
        return []

    if not isinstance(domain, list):
        return []

    normalized: list[Any] = []
    for item in domain:
        if isinstance(item, dict):
            # Convert {"field": "x", "operator": "=", "value": "y"} → ["x", "=", "y"]
            field = item.get("field", item.get("name", ""))
            operator = item.get("operator", item.get("op", "="))
            value = item.get("value", "")
            if field:
                normalized.append([str(field), str(operator), value])
        elif isinstance(item, str):
            # Logical operator (&, |, !)
            normalized.append(item)
        elif isinstance(item, (list, tuple)):
            normalized.append(list(item))
        else:
            normalized.append(item)

    return normalized


def _normalize_list(value: Any) -> list[str]:
    """Normalize a value to a list of strings. LLM sometimes sends strings."""
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        try:
            import ast

            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
        except (ValueError, SyntaxError):
            pass
        # Comma-separated fallback
        return [v.strip().strip("'\"") for v in value.split(",") if v.strip()]
    return ["name"]


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
        if tool_name == "odoo_read_group":
            return await _exec_read_group(tool_input, odoo_client, uid, api_key)
        if tool_name == "odoo_fields_get":
            return await _exec_fields_get(tool_input, odoo_client, uid, api_key)
        return f"Unknown tool: {tool_name}"
    except Exception as exc:
        error_str = str(exc)
        user_msg = getattr(exc, "user_message", error_str)
        logger.warning(
            "Tool execution failed",
            tool=tool_name,
            error=user_msg,
            input=str(tool_input)[:200],
        )
        # Give the LLM useful info to retry with different params
        if "Invalid field" in error_str:
            return (
                f"Erreur: champ invalide dans la requete. "
                f"Essaie avec moins de champs ou un filtre different. "
                f"Detail: {error_str.split('ValueError: ')[-1][:150]}"
            )
        if "access" in error_str.lower() or "permission" in error_str.lower():
            return "Erreur: acces refuse a ce modele. Essaie un autre modele."
        return f"Erreur: {user_msg[:200]}"


async def _exec_search_read(
    inp: dict[str, Any],
    client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """Execute odoo_search_read with Guardian validation."""
    model = str(inp.get("model", ""))
    domain = _normalize_domain(inp.get("domain", []))
    fields = _normalize_list(inp.get("fields", ["name"]))
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
    domain = _normalize_domain(inp.get("domain", []))

    # Guardian gates
    guarded_odoo_write_check(model, "search_count", domain)

    # Execute
    count = await client.search_count(api_key, model, domain, uid=uid)

    return f"{count} enregistrement(s) {model} correspondent a ce filtre."


async def _exec_read_group(
    inp: dict[str, Any],
    client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """Execute odoo_read_group with Guardian validation."""
    model = str(inp.get("model", ""))
    domain = _normalize_domain(inp.get("domain", []))
    groupby = _normalize_list(inp.get("groupby", []))
    fields = _normalize_list(inp.get("fields", ["__count"]))

    # Guardian gates
    guarded_odoo_write_check(model, "read_group", domain)

    # Execute
    raw = await client.read_group(api_key, model, domain, fields, groupby, uid=uid)

    # Format for LLM
    if not raw:
        return f"Aucun resultat pour le regroupement {model}."

    lines = [f"{len(raw)} groupe(s) {model} :"]
    for group in raw:
        parts = [f"{k}={v}" for k, v in group.items() if not k.startswith("__")]
        lines.append(f"  - {', '.join(parts)}")

    return "\n".join(lines)


async def _exec_fields_get(
    inp: dict[str, Any],
    client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """Execute odoo_fields_get — list available fields on a model."""
    model = str(inp.get("model", ""))

    # Guardian gate
    guarded_odoo_write_check(model, "fields_get")

    try:
        raw = await client.execute(
            api_key,
            model,
            "fields_get",
            [],
            uid=uid,
            kwargs={"attributes": ["string", "type", "required"]},
        )
    except Exception as exc:
        error_str = str(exc)
        if "doesn't exist" in error_str:
            return f"Le modele '{model}' n'existe pas sur cette instance."
        return f"Erreur: {error_str[:200]}"

    if not isinstance(raw, dict):
        return f"Impossible de lire les champs de {model}."

    lines = [f"Champs de {model} ({len(raw)} total) :"]
    for fname, fdata in list(raw.items())[:30]:
        if fname.startswith("__"):
            continue
        ftype = fdata.get("type", "?")
        req = " *" if fdata.get("required") else ""
        label = fdata.get("string", "")
        lines.append(f"  {fname}: {ftype}{req} — {label}")

    if len(raw) > 30:
        lines.append(f"  ... et {len(raw) - 30} autres champs")

    return "\n".join(lines)
