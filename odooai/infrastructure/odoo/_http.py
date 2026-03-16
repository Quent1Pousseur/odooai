"""
Module: infrastructure/odoo/_http.py
Role: Module-level httpx connection pool shared across all OdooClient instances.
Dependencies: httpx
"""

import httpx
import structlog

logger = structlog.get_logger(__name__)

DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 2

_http_pool = httpx.AsyncClient(
    timeout=DEFAULT_TIMEOUT,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
)


def get_http_pool() -> httpx.AsyncClient:
    """Return the shared httpx connection pool."""
    return _http_pool


async def close_http_pool() -> None:
    """Close the shared httpx pool. Called at application shutdown."""
    await _http_pool.aclose()
    logger.info("Odoo httpx pool closed")
