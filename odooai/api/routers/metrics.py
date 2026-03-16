"""
Module: api/routers/metrics.py
Role: Expose application metrics for monitoring.
Dependencies: infrastructure/telemetry
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from odooai.infrastructure.telemetry import get_metrics

router = APIRouter(tags=["monitoring"])


@router.get("/metrics")
async def metrics() -> dict[str, Any]:
    """Return application metrics."""
    return get_metrics()
