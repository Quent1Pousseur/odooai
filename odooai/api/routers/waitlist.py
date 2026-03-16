"""
Module: api/routers/waitlist.py
Role: Simple email capture for landing page waitlist.
Dependencies: fastapi
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import structlog
from fastapi import APIRouter
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["waitlist"])

WAITLIST_FILE = Path("waitlist.json")


class WaitlistRequest(BaseModel):
    """Email signup request."""

    email: str


@router.post("/api/waitlist")
async def signup(request: WaitlistRequest) -> dict[str, str]:
    """Add an email to the waitlist."""
    entries: list[dict[str, str]] = []
    if WAITLIST_FILE.exists():
        entries = json.loads(WAITLIST_FILE.read_text())

    # Deduplicate
    if any(e["email"] == request.email for e in entries):
        return {"status": "already_registered"}

    entries.append(
        {
            "email": request.email,
            "signed_up_at": datetime.now(UTC).isoformat(),
        }
    )
    WAITLIST_FILE.write_text(json.dumps(entries, indent=2))

    logger.info("Waitlist signup", email=request.email, total=len(entries))
    return {"status": "ok"}
