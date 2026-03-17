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

# Tools exposed to the LLM — descriptions are PLAYBOOKS
TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "odoo_search_read",
        "description": (
            "Search and read records from the user's Odoo database.\n\n"
            "USE THIS for: listing records, finding specific data, "
            "answering questions about the user's business data.\n\n"
            "DOMAIN SYNTAX: [['field','operator','value']]\n"
            "Operators: =, !=, >, <, >=, <=, like, ilike, in, not in, "
            "child_of, parent_of\n"
            "OR logic: ['|', condition1, condition2]\n"
            "Dot notation: 'partner_id.country_id.code'\n\n"
            "COMMON MODELS:\n"
            "- sale.order: quotations & sales orders "
            "(state: draft/sent/sale/cancel)\n"
            "- account.move: invoices & journal entries "
            "(move_type: out_invoice/in_invoice/entry, "
            "state: draft/posted/cancel)\n"
            "- stock.picking: delivery/reception orders\n"
            "- res.partner: contacts/customers/vendors\n"
            "- product.product: products\n"
            "- hr.employee: employees\n"
            "- purchase.order: purchase orders\n"
            "- crm.lead: CRM opportunities\n\n"
            "TIPS:\n"
            "- If unsure about fields, call odoo_fields_get first\n"
            "- Use limit to avoid fetching too many records\n"
            "- For Many2one fields, Odoo returns [id, name]"
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
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fields to return",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max records (default 10, max 50)",
                    "default": 10,
                },
            },
            "required": ["model", "domain", "fields"],
        },
    },
    {
        "name": "odoo_search_count",
        "description": (
            "Count records matching a filter. "
            "Use for 'how many' questions. Faster than search_read."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "domain": {"type": "array"},
            },
            "required": ["model", "domain"],
        },
    },
    {
        "name": "odoo_read_group",
        "description": (
            "Aggregate records with GROUP BY. Much faster than fetching "
            "all records.\n\n"
            "USE THIS for: totals, averages, counts by group, "
            "rankings, statistics.\n\n"
            "FIELD SPECS: 'field:agg' where agg = sum, avg, min, "
            "max, count\n"
            "DATE GROUPING: 'date_field:month', 'date_field:quarter', "
            "'date_field:year'\n\n"
            "EXAMPLES:\n"
            "- Revenue by customer: model=sale.order, "
            "fields=['amount_total:sum'], groupby=['partner_id']\n"
            "- Orders by state: model=sale.order, "
            "fields=['__count'], groupby=['state']\n"
            "- Monthly revenue: model=sale.order, "
            "fields=['amount_total:sum'], groupby=['date_order:month']"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "domain": {"type": "array"},
                "groupby": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["model", "domain", "groupby", "fields"],
        },
    },
    {
        "name": "odoo_fields_get",
        "description": (
            "List fields available on a model with their types.\n\n"
            "ALWAYS call this BEFORE search_read if you are not 100% "
            "sure which fields exist on the model. This prevents "
            "'Invalid field' errors.\n\n"
            "Also useful to check if a model exists on this instance."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
            },
            "required": ["model"],
        },
    },
    {
        "name": "odoo_execute",
        "description": (
            "Execute any method on an Odoo model. This is the most "
            "powerful tool — handles create, write, copy, and all "
            "workflow transitions.\n\n"
            "MANDATORY: Always confirm with the user before executing "
            "write operations.\n\n"
            "CREATE a record:\n"
            "  method='create', args=[{field: value}]\n"
            "  Example: create a quotation:\n"
            "    model='sale.order', method='create',\n"
            "    args=[{'partner_id': 42}]\n\n"
            "WRITE (update) records:\n"
            "  method='write', args=[[record_ids], {field: value}]\n"
            "  Example: update a partner name:\n"
            "    model='res.partner', method='write',\n"
            "    args=[[42], {'name': 'New Name'}]\n\n"
            "WORKFLOW TRANSITIONS (no args needed):\n"
            "  method='action_confirm' — confirm quotation → sale\n"
            "  method='action_cancel' — cancel\n"
            "  method='action_draft' — reset to draft\n"
            "  method='action_post' — validate journal entry\n"
            "  method='button_validate' — validate transfer\n"
            "  args=[[record_id]] (just the ID, no other args)\n\n"
            "ONE2MANY inline creation:\n"
            "  'order_line': [(0, 0, {child_values})]\n"
            "  Example: quotation with lines:\n"
            "    args=[{'partner_id': 42, 'order_line': [\n"
            "      (0, 0, {'product_id': 1, 'product_uom_qty': 5})"
            "\n    ]}]\n\n"
            "MANY2MANY commands:\n"
            "  [(6, 0, [ids])] — replace all\n"
            "  [(4, id, 0)] — add one\n"
            "  [(3, id, 0)] — remove one\n\n"
            "BLOCKED: unlink (delete) and sudo are permanently "
            "blocked for safety.\n\n"
            "PITFALLS:\n"
            "- Do NOT pass args for workflow methods — just [id]\n"
            "- For Many2one fields, pass integer ID not name\n"
            "- For selection fields, use technical key ('draft') "
            "not label ('Quotation')\n"
            "- For dates, use ISO format: '2025-04-15'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "method": {
                    "type": "string",
                    "description": "Method name: create, write, "
                    "copy, action_confirm, action_post, etc.",
                },
                "args": {
                    "type": "array",
                    "description": "Method arguments",
                },
            },
            "required": ["model", "method", "args"],
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
        if tool_name == "odoo_execute":
            return await _exec_execute(tool_input, odoo_client, uid, api_key)
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


async def _exec_execute(
    inp: dict[str, Any],
    client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """Execute any Odoo method — the universal tool."""
    model = str(inp.get("model", ""))
    method = str(inp.get("method", ""))
    raw_args = inp.get("args", [])

    # Normalize args
    if isinstance(raw_args, str):
        import ast

        try:
            raw_args = ast.literal_eval(raw_args)
        except (ValueError, SyntaxError):
            return "Error: args is not a valid list."
    if not isinstance(raw_args, list):
        raw_args = [raw_args]

    # Blocked methods
    blocked = {"unlink", "sudo", "_sudo"}
    if method in blocked:
        return f"Error: method '{method}' is blocked for safety."

    # Guardian gate
    guarded_odoo_write_check(model, method)

    try:
        result = await client.execute(
            api_key,
            model,
            method,
            raw_args,
            uid=uid,
        )
        logger.info("Execute OK", model=model, method=method)

        # Format result based on method
        if method == "create":
            return f"Created {model} ID={result}"
        if method == "write":
            return f"Updated {model} successfully."
        if method == "copy":
            return f"Copied to {model} ID={result}"
        if method.startswith("action_") or method.startswith("button_"):
            return f"Executed {model}.{method} successfully."
        return f"Result: {str(result)[:500]}"
    except Exception as exc:
        error_str = str(exc)
        if "doesn't exist" in error_str:
            return f"Error: model '{model}' does not exist."
        if "Invalid field" in error_str:
            return (
                f"Error: invalid field. Check with odoo_fields_get. "
                f"Detail: {error_str.split('ValueError: ')[-1][:150]}"
            )
        return f"Error: {error_str[:200]}"
