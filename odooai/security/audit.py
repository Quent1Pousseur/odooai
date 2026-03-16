"""
Module: security/audit.py
Role: Audit log writer for all data operations.
      Uses structlog for structured output. DB persistence in Phase 2.
Dependencies: structlog
"""

from __future__ import annotations

from typing import Any

import structlog

logger = structlog.get_logger("odooai.audit")


def log_access(
    model: str,
    operation: str,
    uid: int,
    record_ids: list[int] | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    """
    Log a data access operation for audit trail.

    Args:
        model: Odoo model accessed.
        operation: Operation type (search_read, create, write, execute).
        uid: Odoo user ID performing the operation.
        record_ids: IDs of records affected (if applicable).
        metadata: Additional context (category, anonymized, etc.).
    """
    logger.info(
        "data_access",
        model=model,
        operation=operation,
        uid=uid,
        record_ids=record_ids or [],
        record_count=len(record_ids) if record_ids else 0,
        **(metadata or {}),
    )


def log_blocked(
    model: str,
    method: str,
    uid: int,
    reason: str,
) -> None:
    """
    Log a blocked access attempt.

    Args:
        model: Odoo model that was targeted.
        method: Method that was attempted.
        uid: Odoo user ID that attempted the access.
        reason: Why the access was blocked.
    """
    logger.warning(
        "access_blocked",
        model=model,
        method=method,
        uid=uid,
        reason=reason,
    )
