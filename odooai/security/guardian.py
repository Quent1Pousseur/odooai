"""
Module: security/guardian.py
Role: Security Guardian — the central security pipeline for all Odoo data access.
      Intercepts data BEFORE it reaches the LLM. ZERO LLM dependency.
      Pure deterministic logic: classify, validate, filter, anonymize, audit.
Dependencies: domain/value_objects, services/model_classifier, security/anonymizer
"""

from __future__ import annotations

from typing import Any

import structlog

from odooai.domain.value_objects.model_category import ModelCategory
from odooai.domain.value_objects.sanitized_response import SanitizedResponse
from odooai.exceptions import BlockedMethodError
from odooai.security.anonymizer import anonymize_record
from odooai.security.audit import log_access
from odooai.services.model_classifier import check_model_access

logger = structlog.get_logger(__name__)

# Methods that are PERMANENTLY blocked — never callable via OdooAI.
BLOCKED_METHODS: frozenset[str] = frozenset({"unlink", "sudo", "_sudo"})

# Fields that should never be exposed to the LLM, regardless of model category.
_ALWAYS_HIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "password",
        "password_crypt",
        "api_key",
        "token",
        "secret",
        "credit_card",
        "session_token",
    }
)


def guard_model_access(model: str) -> ModelCategory:
    """
    Gate: classify a model and reject BLOCKED ones.

    Args:
        model: Odoo technical model name.

    Returns:
        ModelCategory (SENSITIVE, STANDARD, or OPEN).

    Raises:
        BlockedModelError: If the model is permanently blocked.
    """
    return check_model_access(model)


def guard_method(method: str) -> None:
    """
    Gate: reject permanently blocked methods.

    Args:
        method: Odoo method name.

    Raises:
        BlockedMethodError: If the method is blocked (unlink, sudo).
    """
    if method in BLOCKED_METHODS:
        raise BlockedMethodError(
            message=f"Method '{method}' is permanently blocked",
            user_message=f"Method '{method}' is not allowed. Use archive instead of delete.",
        )


def sanitize_response(
    model: str,
    category: ModelCategory,
    records: list[dict[str, Any]],
    requested_fields: list[str],
    uid: int = 0,
    operation: str = "search_read",
) -> SanitizedResponse:
    """
    Full security pipeline: filter fields, anonymize sensitive data, audit.

    This is the main entry point called after every Odoo data retrieval.

    Args:
        model: Odoo model name.
        category: Pre-classified ModelCategory.
        records: Raw Odoo records.
        requested_fields: Fields the caller requested.
        uid: Odoo user ID (for audit).
        operation: Operation type (for audit).

    Returns:
        SanitizedResponse with clean data safe for LLM consumption.
    """
    if not records:
        return SanitizedResponse(model=model, record_count=0)

    # Step 1: Filter hidden fields from all records
    filtered = [_filter_fields(record, requested_fields) for record in records]

    # Step 2: Anonymize if SENSITIVE
    was_anonymized = False
    if category == ModelCategory.SENSITIVE:
        filtered = [anonymize_record(record, model) for record in filtered]
        was_anonymized = True

    # Step 3: Determine fields actually returned
    fields_returned = tuple(sorted(filtered[0].keys())) if filtered else ()

    # Step 4: Audit log
    record_ids = [r.get("id", 0) for r in records if "id" in r]
    log_access(
        model=model,
        operation=operation,
        uid=uid,
        record_ids=record_ids,
        metadata={"category": category.value, "anonymized": was_anonymized},
    )

    logger.debug(
        "Guardian: response sanitized",
        model=model,
        category=category.value,
        record_count=len(filtered),
        anonymized=was_anonymized,
    )

    return SanitizedResponse(
        model=model,
        records=tuple(filtered),
        fields_returned=fields_returned,
        record_count=len(filtered),
        was_anonymized=was_anonymized,
    )


def _filter_fields(
    record: dict[str, Any],
    requested_fields: list[str],
) -> dict[str, Any]:
    """
    Remove hidden fields and normalize Many2one values.

    Always keeps 'id'. Removes fields in _ALWAYS_HIDDEN_FIELDS.
    If requested_fields is non-empty, only keeps those + id.
    """
    result: dict[str, Any] = {}

    for field, value in record.items():
        # Always remove hidden fields
        if field in _ALWAYS_HIDDEN_FIELDS:
            continue

        # If specific fields requested, only keep those + id
        if requested_fields and field != "id" and field not in requested_fields:
            continue

        # Normalize Many2one tuples: [id, name] → {"id": ..., "name": ...}
        result[field] = _normalize_value(value)

    return result


def _normalize_value(value: Any) -> Any:
    """Normalize Odoo field values for clean LLM consumption."""
    if isinstance(value, (list, tuple)) and len(value) == 2 and isinstance(value[0], int):
        return {"id": value[0], "name": value[1]}
    return value
