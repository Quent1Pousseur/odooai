"""
Module: api/routers/chat.py
Role: Streaming chat endpoint for the web frontend.
Dependencies: fastapi, agents/orchestrator
"""

from __future__ import annotations

import json
from typing import Any

import structlog
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from odooai.config import get_settings

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["chat"])
limiter = Limiter(key_func=get_remote_address)


class ChatRequest(BaseModel):
    """Chat request from the frontend."""

    message: str
    conversation_id: str = ""  # Empty = new conversation
    version: str = "17.0"
    model: str = "claude-sonnet-4-20250514"
    max_tools: int = 10
    # Optional Odoo connection (for live mode)
    odoo_url: str = ""
    odoo_db: str = ""
    odoo_login: str = ""
    odoo_api_key: str = ""


@router.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request, body: ChatRequest) -> StreamingResponse:
    """
    Chat endpoint with Server-Sent Events streaming.

    Rate limited to 10 requests per minute per IP (slowapi).
    """
    return StreamingResponse(
        _stream_response(body),
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
    real_odoo_api_key = ""
    if request.odoo_url and request.odoo_db and request.odoo_api_key:
        odoo_client, odoo_uid, real_odoo_api_key = await _connect_odoo(request)

    # Send "thinking" event
    yield _sse_event({"type": "status", "content": "Recherche en cours..."})

    try:
        from odooai.agents._streaming import stream_ba_response
        from odooai.infrastructure.db.database import get_session
        from odooai.infrastructure.db.models import Conversation, Message

        # Get or create conversation
        conversation_id = request.conversation_id
        try:
            async for session in get_session():
                if not conversation_id:
                    conv = Conversation(
                        title=request.message[:100],
                    )
                    session.add(conv)
                    await session.commit()
                    await session.refresh(conv)
                    conversation_id = str(conv.id)

                # Save user message
                user_msg = Message(
                    conversation_id=conversation_id,
                    role="user",
                    content=request.message,
                )
                session.add(user_msg)
                await session.commit()
                break
        except Exception:
            pass  # DB optional — continue without persistence

        yield _sse_event({"type": "conversation_id", "content": conversation_id})

        # Load conversation history (last 10 messages for context)
        conversation_history: list[dict[str, str]] = []
        if conversation_id:
            try:
                async for session in get_session():
                    from sqlalchemy import select

                    result = await session.execute(
                        select(Message)
                        .where(Message.conversation_id == conversation_id)
                        .order_by(Message.created_at.desc())
                        .limit(10),
                    )
                    history_msgs = list(reversed(result.scalars().all()))
                    # Exclude the current user message (already added above)
                    for m in history_msgs[:-1]:
                        conversation_history.append({"role": m.role, "content": m.content})
                    break
            except Exception:
                pass

        # Stream response — RAG handles context, no domain classification needed
        full_response = ""
        total_tokens = 0
        async for event in stream_ba_response(
            request.message,
            None,  # No BA Profile — RAG provides context
            api_key,
            request.model,
            conversation_history=conversation_history,
            odoo_client=odoo_client,
            odoo_uid=odoo_uid,
            odoo_api_key=real_odoo_api_key,
            max_tools=request.max_tools,
        ):
            yield _sse_event(event)
            if event.get("type") == "text":
                full_response += event.get("content", "")
            if event.get("type") == "done":
                total_tokens = event.get("tokens", 0)

        # Save assistant message
        try:
            async for session in get_session():
                if conversation_id and full_response:
                    assistant_msg = Message(
                        conversation_id=conversation_id,
                        role="assistant",
                        content=full_response,
                        tokens=total_tokens,
                    )
                    session.add(assistant_msg)
                    await session.commit()
                break
        except Exception:
            pass  # DB optional

    except Exception as exc:
        err_type = type(exc).__name__
        logger.error("Chat error", error=str(exc), type=err_type)
        yield _sse_event({"type": "error", "content": f"Erreur ({err_type})"})


async def _connect_odoo(request: ChatRequest) -> tuple[Any, int, str]:
    """Connect to Odoo instance. Returns (client, uid, real_api_key) or (None, 0, "")."""
    try:
        from odooai.domain.entities.connection import OdooApiType
        from odooai.infrastructure.odoo.client import OdooClient

        odoo_url = request.odoo_url
        odoo_db = request.odoo_db
        odoo_login = request.odoo_login
        odoo_api_key = request.odoo_api_key

        # Support saved connections: api_key = "connection:UUID"
        if odoo_api_key.startswith("connection:"):
            import contextlib

            from sqlalchemy import select

            from odooai.config import get_settings
            from odooai.infrastructure.crypto import AESCrypto
            from odooai.infrastructure.db.database import get_session
            from odooai.infrastructure.db.models import OdooConnection

            conn_id = odoo_api_key.split(":", 1)[1]
            settings = get_settings()

            session_gen = get_session()
            session = await session_gen.__anext__()
            try:
                result = await session.execute(
                    select(OdooConnection).where(OdooConnection.id == conn_id),
                )
                conn = result.scalar_one_or_none()
            finally:
                with contextlib.suppress(StopAsyncIteration):
                    await session_gen.__anext__()

            if not conn or not settings.odoo_crypto_key:
                logger.warning("Saved connection not found", conn_id=conn_id)
                return None, 0, ""

            crypto = AESCrypto(key_b64=settings.odoo_crypto_key)
            odoo_url = conn.url
            odoo_db = conn.db_name
            odoo_login = conn.login
            odoo_api_key = crypto.decrypt(conn.api_key_encrypted)

        client = OdooClient(
            base_url=odoo_url,
            db=odoo_db,
            api_type=OdooApiType.XML_RPC,
        )
        user_info = await client.authenticate(odoo_login, odoo_api_key)
        logger.info("Odoo connected via API", uid=user_info.uid)
        return client, user_info.uid, odoo_api_key
    except Exception as exc:
        logger.warning("Odoo connection failed", error=str(exc))
        return None, 0, ""


def _sse_event(data: dict[str, Any]) -> str:
    """Format a dict as an SSE event."""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
