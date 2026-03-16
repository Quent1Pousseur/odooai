"""
Module: api/routers/conversations.py
Role: CRUD endpoints for conversations and message history.
Dependencies: sqlalchemy, infrastructure/db
"""

from __future__ import annotations

from typing import Any

import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from odooai.infrastructure.db.database import get_session
from odooai.infrastructure.db.models import Conversation, Message

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


class ConversationOut(BaseModel):
    """Conversation response."""

    id: str
    title: str
    domain_id: str
    created_at: str
    updated_at: str


class MessageOut(BaseModel):
    """Message response."""

    id: str
    role: str
    content: str
    tokens: int
    created_at: str


@router.post("", response_model=ConversationOut)
async def create_conversation(
    session: AsyncSession = Depends(get_session),
) -> Any:
    """Create a new conversation."""
    conv = Conversation()
    session.add(conv)
    await session.commit()
    await session.refresh(conv)
    return _conv_to_dict(conv)


@router.get("", response_model=list[ConversationOut])
async def list_conversations(
    session: AsyncSession = Depends(get_session),
) -> Any:
    """List all conversations, most recent first."""
    result = await session.execute(
        select(Conversation).order_by(Conversation.updated_at.desc()).limit(50)
    )
    conversations = result.scalars().all()
    return [_conv_to_dict(c) for c in conversations]


@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
async def get_messages(
    conversation_id: str,
    session: AsyncSession = Depends(get_session),
) -> Any:
    """Get all messages in a conversation."""
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    return [_msg_to_dict(m) for m in messages]


def _conv_to_dict(conv: Conversation) -> dict[str, Any]:
    return {
        "id": str(conv.id),
        "title": str(conv.title),
        "domain_id": str(conv.domain_id or ""),
        "created_at": str(conv.created_at),
        "updated_at": str(conv.updated_at),
    }


def _msg_to_dict(msg: Message) -> dict[str, Any]:
    return {
        "id": str(msg.id),
        "role": str(msg.role),
        "content": str(msg.content),
        "tokens": int(msg.tokens or 0),
        "created_at": str(msg.created_at),
    }
