"""
Module: security/audit.py
Role: Audit log writer for all data operations.
      Stub for Sprint 1 — full implementation with DB persistence in SEC-001.
Dependencies: structlog (future)
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


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
        metadata: Additional context for the audit log.
    """
    logger.info(
        "audit: %s on %s by uid=%d ids=%s",
        operation,
        model,
        uid,
        record_ids or [],
        extra=metadata or {},
    )
