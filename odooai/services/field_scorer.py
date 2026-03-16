"""
Module: services/field_scorer.py
Role: Score and select the most useful Odoo fields for LLM consumption.
      When the LLM omits the fields parameter, auto-select top N fields
      by relevance instead of returning all 100+ fields from Odoo.
Dependencies: none (pure Python)
"""

from __future__ import annotations

# Field types excluded entirely (carry zero useful info for LLM queries).
_EXCLUDED_TYPES = frozenset({"binary", "html", "one2many", "many2many", "properties"})

# Prefixes indicating noise fields (chatter, activity, website messaging).
_NOISE_PREFIXES = ("message_", "activity_", "website_message_")

# Essential fields always included (score 1000).
_ESSENTIAL_FIELDS = frozenset({"id", "name", "display_name"})

# Business-relevant field names that get a bonus score.
_BUSINESS_PATTERNS: dict[str, int] = {
    "state": 80,
    "amount_total": 80,
    "amount_untaxed": 70,
    "partner_id": 70,
    "date_order": 70,
    "date_invoice": 70,
    "invoice_date": 70,
    "date": 60,
    "create_date": 50,
    "user_id": 50,
    "company_id": 40,
    "currency_id": 40,
    "pricelist_id": 30,
}

# Score by field type (higher = more useful for LLM queries).
_TYPE_SCORES: dict[str, int] = {
    "char": 200,
    "monetary": 200,
    "selection": 200,
    "integer": 180,
    "float": 180,
    "date": 180,
    "datetime": 160,
    "many2one": 150,
    "boolean": 120,
    "text": 100,
}


def score_field(field_name: str, field_meta: dict[str, object]) -> int:
    """
    Score a single Odoo field by usefulness for LLM consumption.

    Returns -1 for excluded fields (binary, html, noise prefixes).

    Args:
        field_name: Technical field name (e.g. 'partner_id').
        field_meta: Odoo fields_get() metadata dict for this field.

    Returns:
        Integer score. -1 means excluded, 0+ means eligible.
    """
    field_type = str(field_meta.get("type", ""))

    if field_type in _EXCLUDED_TYPES:
        return -1

    if any(field_name.startswith(p) for p in _NOISE_PREFIXES):
        return -1

    if field_name in _ESSENTIAL_FIELDS:
        return 1000

    score = 0

    if field_meta.get("required"):
        score += 500

    score += _TYPE_SCORES.get(field_type, 50)
    score += _BUSINESS_PATTERNS.get(field_name, 0)

    return score


def select_top_fields(
    fields_meta: dict[str, dict[str, object]],
    top_n: int = 15,
) -> list[str]:
    """
    Select the top N most useful fields from an Odoo model's fields_get() result.

    Always includes 'id'. Excludes binary, html, o2m, m2m, and noise fields.

    Args:
        fields_meta: Full fields_get() result from Odoo.
        top_n: Maximum number of fields to return (default 15).

    Returns:
        List of field names, sorted by descending score, capped at top_n.
    """
    scored: list[tuple[str, int]] = []

    for fname, fmeta in fields_meta.items():
        s = score_field(fname, fmeta)
        if s >= 0:
            scored.append((fname, s))

    scored.sort(key=lambda x: (-x[1], x[0]))

    result = [fname for fname, _ in scored[:top_n]]

    if "id" not in result:
        result.append("id")

    return result
