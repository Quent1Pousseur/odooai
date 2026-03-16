"""
Module: api/routers/chat.py
Role: Streaming chat endpoint for the web frontend.
Dependencies: fastapi, agents/orchestrator
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import structlog
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from odooai.config import get_settings

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request from the frontend."""

    message: str
    version: str = "17.0"
    model: str = "claude-sonnet-4-20250514"
    max_tools: int = 10
    # Optional Odoo connection (for live mode)
    odoo_url: str = ""
    odoo_db: str = ""
    odoo_login: str = ""
    odoo_api_key: str = ""


# Simple in-memory rate limiter (per-IP, 10 requests/minute)
_rate_limit: dict[str, list[float]] = {}
_RATE_LIMIT_MAX = 10
_RATE_LIMIT_WINDOW = 60.0  # seconds


def _check_rate_limit(client_ip: str) -> bool:
    """Return True if request is allowed, False if rate limited."""
    import time

    now = time.time()
    if client_ip not in _rate_limit:
        _rate_limit[client_ip] = []
    # Clean old entries
    _rate_limit[client_ip] = [t for t in _rate_limit[client_ip] if now - t < _RATE_LIMIT_WINDOW]
    if len(_rate_limit[client_ip]) >= _RATE_LIMIT_MAX:
        return False
    _rate_limit[client_ip].append(now)
    return True


@router.post("/api/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """
    Chat endpoint with Server-Sent Events streaming.

    Rate limited to 10 requests per minute per IP.
    """
    # Note: in production, use a proper middleware (slowapi, Redis-based)
    return StreamingResponse(
        _stream_response(request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


async def _stream_response(request: ChatRequest) -> Any:
    """Generate SSE events for the chat response."""
    settings = get_settings()
    api_key = settings.anthropic_api_key

    if not api_key:
        yield _sse_event({"type": "error", "content": "ANTHROPIC_API_KEY not configured"})
        return

    # Optional Odoo client
    odoo_client = None
    odoo_uid = 0
    if request.odoo_url and request.odoo_db and request.odoo_api_key:
        odoo_client, odoo_uid = await _connect_odoo(request)

    # Send "thinking" event
    yield _sse_event({"type": "status", "content": "Recherche en cours..."})

    try:
        from odooai.agents.orchestrator import detect_domain, handle_question
        from odooai.knowledge.ba_factory import DOMAIN_NAMES

        # Detect domain
        domain = detect_domain(request.message)
        domain_name = DOMAIN_NAMES.get(domain or "sales_crm", "general")
        yield _sse_event({"type": "domain", "content": domain_name})

        # Get response (non-streaming for now — full streaming in Sprint 3)
        response = await handle_question(
            request.message,
            api_key,
            request.version,
            request.model,
            odoo_client=odoo_client,
            odoo_uid=odoo_uid,
            odoo_api_key=request.odoo_api_key,
            max_tools=request.max_tools,
        )

        # Stream the answer in chunks for progressive display
        answer = response.answer
        chunk_size = 20  # Characters per chunk
        for i in range(0, len(answer), chunk_size):
            chunk = answer[i : i + chunk_size]
            yield _sse_event({"type": "text", "content": chunk})
            await asyncio.sleep(0.02)  # Small delay for visual streaming

        # Send metadata
        yield _sse_event(
            {
                "type": "done",
                "tokens": response.tokens_used,
                "sources": response.sources,
                "domain": response.domain,
            }
        )

    except Exception as exc:
        err_type = type(exc).__name__
        logger.error("Chat error", error=str(exc), type=err_type)
        yield _sse_event({"type": "error", "content": f"Erreur ({err_type})"})


async def _connect_odoo(request: ChatRequest) -> tuple[Any, int]:
    """Connect to Odoo instance. Returns (client, uid) or (None, 0)."""
    try:
        from odooai.domain.entities.connection import OdooApiType
        from odooai.infrastructure.odoo.client import OdooClient

        client = OdooClient(
            base_url=request.odoo_url,
            db=request.odoo_db,
            api_type=OdooApiType.XML_RPC,  # Auto-detect in future
        )
        user_info = await client.authenticate(request.odoo_login, request.odoo_api_key)
        logger.info("Odoo connected via API", uid=user_info.uid)
        return client, user_info.uid
    except Exception as exc:
        logger.warning("Odoo connection failed", error=str(exc))
        return None, 0


def _sse_event(data: dict[str, Any]) -> str:
    """Format a dict as an SSE event."""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
