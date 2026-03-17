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
            "WORKFLOW — follow these steps:\n"
            "1. If unsure about fields → call odoo_schema first\n"
            "2. Search with a broad filter → refine if too many results\n"
            "3. If search returns nothing → try different field names "
            "or broader domain\n"
            "4. For Many2one fields, Odoo returns [id, name]\n"
            "5. Max 50 records per call — use limit wisely"
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
        "name": "odoo_schema",
        "description": (
            "Explore Odoo model structure. 3 modes:\n\n"
            "MODE 'compact' (default, cheapest):\n"
            "  Returns field names with types on one line each.\n"
            "  Use BEFORE search_read if unsure about field names.\n"
            "  Example: 'name: char*, partner_id: many2one, "
            "state: selection'\n"
            "  (* = required)\n\n"
            "MODE 'detailed':\n"
            "  Returns full metadata: type, required, readonly, "
            "string label, selection values, relation target.\n"
            "  Use when you need selection options or relation "
            "targets.\n\n"
            "MODE 'list':\n"
            "  Returns all model names available on this instance.\n"
            "  Use to discover which models exist.\n"
            "  Pass model='_all' with mode='list'.\n\n"
            "ALWAYS call this before querying an unfamiliar model."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": "Model name, or '_all' for list mode",
                },
                "mode": {
                    "type": "string",
                    "enum": ["compact", "detailed", "list"],
                    "description": "compact (default), detailed, or list",
                },
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
            "CRITICAL SAFETY RULES:\n"
            "1. NEVER create or modify records without explicit user "
            "approval. Always present what you will do and ask "
            "'Shall I proceed?' BEFORE calling this tool.\n"
            "2. NEVER invent data. If the user says 'create a quote' "
            "but does not specify the customer or products, ASK.\n"
            "3. Always search for the correct IDs first (customer, "
            "product) using odoo_search_read before creating.\n\n"
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
        if tool_name == "odoo_schema":
            return await _exec_schema(tool_input, odoo_client, uid, api_key)
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


def _normalize_records(
    records: list[dict[str, Any]] | tuple[dict[str, Any], ...],
) -> list[dict[str, Any]]:
    """Normalize Odoo records for clean LLM consumption.

    Converts Many2one [id, "name"] → {"id": id, "name": "name"}
    so the LLM can easily extract IDs for create/write operations.
    """
    clean: list[dict[str, Any]] = []
    for record in records:
        normalized: dict[str, Any] = {}
        for key, value in record.items():
            if isinstance(value, list) and len(value) == 2 and isinstance(value[0], int):
                # Many2one: [42, "Partner Name"] → {"id": 42, "name": "Partner Name"}
                normalized[key] = {"id": value[0], "name": value[1]}
            else:
                normalized[key] = value
        clean.append(normalized)
    return clean


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

    # Format for LLM — return clean JSON
    import json

    if not result.records:
        return f"No records found for {model} with this filter."

    # Normalize Many2one: [id, "name"] → {"id": id, "name": "name"}
    clean = _normalize_records(result.records)
    return json.dumps(clean, ensure_ascii=False, default=str)


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

    # Format for LLM — return JSON
    import json

    if not raw:
        return f"No results for read_group on {model}."

    return json.dumps(raw, ensure_ascii=False, default=str)


async def _exec_schema(
    inp: dict[str, Any],
    client: IOdooClient,
    uid: int,
    api_key: str,
) -> str:
    """Execute odoo_schema — explore model structure in 3 modes."""
    model = str(inp.get("model", ""))
    mode = str(inp.get("mode", "compact"))

    # LIST mode — return all model names
    if mode == "list" or model == "_all":
        try:
            models_raw = await client.search_read(
                api_key,
                "ir.model",
                [["transient", "=", False]],
                ["model", "name"],
                limit=200,
                uid=uid,
            )
            if isinstance(models_raw, list):
                model_lines = [f"{m['model']}: {m.get('name', '')}" for m in models_raw]
                return "\n".join(model_lines)
            return "Could not list models."
        except Exception as exc:
            return f"Error listing models: {str(exc)[:150]}"

    # Guardian gate
    guarded_odoo_write_check(model, "fields_get")

    try:
        attrs = ["string", "type", "required"]
        if mode == "detailed":
            attrs.extend(["readonly", "selection", "relation"])
        raw = await client.execute(
            api_key,
            model,
            "fields_get",
            [],
            uid=uid,
            kwargs={"attributes": attrs},
        )
    except Exception as exc:
        error_str = str(exc)
        if "doesn't exist" in error_str:
            return f"Model '{model}' does not exist on this instance."
        return f"Error: {error_str[:200]}"

    if not isinstance(raw, dict):
        return f"Model {model} not found."

    # COMPACT mode — one line per field, minimal tokens
    if mode == "compact":
        lines: list[str] = []
        for fname, fd in sorted(raw.items()):
            if fname.startswith("__"):
                continue
            req = "*" if fd.get("required") else ""
            lines.append(f"{fname}: {fd.get('type', '?')}{req}")
        return "\n".join(lines)

    # DETAILED mode — full metadata as JSON
    import json

    compact: dict[str, dict[str, Any]] = {}
    for fname, fd in sorted(raw.items()):
        if fname.startswith("__"):
            continue
        entry: dict[str, Any] = {
            "type": fd.get("type", ""),
            "label": fd.get("string", ""),
            "required": fd.get("required", False),
        }
        if fd.get("readonly"):
            entry["readonly"] = True
        if fd.get("selection"):
            entry["selection"] = fd["selection"]
        if fd.get("relation"):
            entry["relation"] = fd["relation"]
        compact[fname] = entry

    return json.dumps(compact, ensure_ascii=False)


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
        # Adapt args based on method
        if method == "create":
            # create expects: execute(model, "create", [], kwargs={vals: {...}})
            vals = raw_args[0] if raw_args else {}
            result = await client.execute(
                api_key,
                model,
                method,
                [],
                uid=uid,
                kwargs={"vals": vals},
            )
        elif method == "write":
            # write expects: execute(model, "write", [ids], kwargs={vals: {...}})
            ids = raw_args[0] if raw_args and isinstance(raw_args[0], list) else []
            vals = raw_args[1] if len(raw_args) > 1 else {}
            result = await client.execute(
                api_key,
                model,
                method,
                ids,
                uid=uid,
                kwargs={"vals": vals},
            )
        elif method == "copy":
            # copy expects: execute(model, "copy", [id])
            ids = raw_args[0] if raw_args and isinstance(raw_args[0], list) else raw_args[:1]
            result = await client.execute(
                api_key,
                model,
                method,
                ids,
                uid=uid,
            )
        else:
            # Workflow methods: execute(model, "action_confirm", [id])
            ids = raw_args[0] if raw_args and isinstance(raw_args[0], list) else raw_args
            if not isinstance(ids, list):
                ids = [ids] if ids else []
            result = await client.execute(
                api_key,
                model,
                method,
                ids,
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
                f"Error: invalid field. Check with odoo_schema. "
                f"Detail: {error_str.split('ValueError: ')[-1][:150]}"
            )
        return f"Error: {error_str[:200]}"
