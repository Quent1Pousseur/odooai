"""
Module: infrastructure/telemetry.py
Role: OpenTelemetry setup + custom metrics for OdooAI.
      Learning Observability Engineer (38).
Dependencies: opentelemetry-sdk, opentelemetry-instrumentation-fastapi
"""

from __future__ import annotations

import time
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

# Counters — incremented on each event
_metrics: dict[str, int | float] = {
    "chat_requests_total": 0,
    "tokens_total": 0,
    "tool_calls_total": 0,
    "guardian_blocks_total": 0,
    "conversations_total": 0,
    "haiku_requests": 0,
    "sonnet_requests": 0,
}

# Latency samples
_latency_samples: list[float] = []


def increment(metric: str, value: int = 1) -> None:
    """Increment a counter metric."""
    _metrics[metric] = _metrics.get(metric, 0) + value


def add_tokens(count: int) -> None:
    """Track token usage."""
    _metrics["tokens_total"] = _metrics.get("tokens_total", 0) + count


@contextmanager
def measure_latency() -> Generator[None, None, None]:
    """Context manager to measure chat response latency."""
    start = time.monotonic()
    yield
    elapsed = time.monotonic() - start
    _latency_samples.append(elapsed)


def get_metrics() -> dict[str, Any]:
    """Return all metrics for the /metrics endpoint."""
    p50 = _percentile(50) if _latency_samples else 0
    p95 = _percentile(95) if _latency_samples else 0
    p99 = _percentile(99) if _latency_samples else 0

    return {
        **_metrics,
        "latency_p50": round(p50, 3),
        "latency_p95": round(p95, 3),
        "latency_p99": round(p99, 3),
        "latency_samples": len(_latency_samples),
    }


def _percentile(p: int) -> float:
    """Calculate percentile from samples."""
    if not _latency_samples:
        return 0.0
    sorted_samples = sorted(_latency_samples)
    idx = int(len(sorted_samples) * p / 100)
    idx = min(idx, len(sorted_samples) - 1)
    return sorted_samples[idx]


def setup_telemetry(app: Any) -> None:
    """Instrument FastAPI with OpenTelemetry (if available)."""
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor.instrument_app(app)
        logger.info("OpenTelemetry instrumented FastAPI")
    except ImportError:
        logger.debug("OpenTelemetry not available, skipping")
