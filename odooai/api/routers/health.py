"""
Module: api/routers/health.py
Role: Health check endpoint.
Dependencies: fastapi
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
