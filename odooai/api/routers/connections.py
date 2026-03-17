"""
Module: api/routers/connections.py
Role: CRUD for saved Odoo connections (credentials encrypted).
Dependencies: fastapi, sqlalchemy, crypto
"""

from __future__ import annotations

import contextlib
from datetime import UTC, datetime
from typing import Any

import structlog
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select

from odooai.config import get_settings

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/connections", tags=["connections"])


class ConnectionCreate(BaseModel):
    """Create a new Odoo connection."""

    name: str
    url: str
    db_name: str
    login: str
    api_key: str


class ConnectionResponse(BaseModel):
    """Connection response (no API key)."""

    id: str
    name: str
    url: str
    db_name: str
    login: str
    odoo_version: str
    is_default: bool
    last_connected_at: str | None


@router.post("", response_model=ConnectionResponse)
async def create_connection(
    request: Request,
    body: ConnectionCreate,
) -> ConnectionResponse:
    """Save a new Odoo connection (API key encrypted)."""
    from odooai.infrastructure.crypto import AESCrypto
    from odooai.infrastructure.db.database import get_session
    from odooai.infrastructure.db.models import OdooConnection

    settings = get_settings()
    if not settings.odoo_crypto_key:
        raise HTTPException(
            status_code=500,
            detail="ODOO_CRYPTO_KEY not configured — cannot encrypt credentials",
        )

    crypto = AESCrypto(key_b64=settings.odoo_crypto_key)
    encrypted_key = crypto.encrypt(body.api_key)

    user_id = getattr(request.state, "user_id", "anonymous")

    conn = OdooConnection(
        user_id=user_id,
        name=body.name,
        url=body.url.rstrip("/"),
        db_name=body.db_name,
        login=body.login,
        api_key_encrypted=encrypted_key,
    )

    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        session.add(conn)
        await session.commit()
        await session.refresh(conn)
    finally:
        with contextlib.suppress(StopAsyncIteration):
            await session_gen.__anext__()

    logger.info("Connection saved", name=body.name, user=user_id)
    return _to_response(conn)


@router.get("", response_model=list[ConnectionResponse])
async def list_connections(request: Request) -> list[ConnectionResponse]:
    """List saved connections for the current user."""
    from odooai.infrastructure.db.database import get_session
    from odooai.infrastructure.db.models import OdooConnection

    user_id = getattr(request.state, "user_id", "anonymous")

    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        result = await session.execute(
            select(OdooConnection).where(OdooConnection.user_id == user_id),
        )
        connections = result.scalars().all()
    finally:
        with contextlib.suppress(StopAsyncIteration):
            await session_gen.__anext__()

    return [_to_response(c) for c in connections]


@router.delete("/{connection_id}")
async def delete_connection(
    request: Request,
    connection_id: str,
) -> dict[str, str]:
    """Delete a saved connection."""
    from odooai.infrastructure.db.database import get_session
    from odooai.infrastructure.db.models import OdooConnection

    user_id = getattr(request.state, "user_id", "anonymous")

    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        result = await session.execute(
            select(OdooConnection).where(
                OdooConnection.id == connection_id,
                OdooConnection.user_id == user_id,
            ),
        )
        conn = result.scalar_one_or_none()
        if not conn:
            raise HTTPException(status_code=404, detail="Connection not found")
        await session.delete(conn)
        await session.commit()
    finally:
        with contextlib.suppress(StopAsyncIteration):
            await session_gen.__anext__()

    return {"status": "deleted"}


@router.post("/{connection_id}/test")
async def test_connection(
    request: Request,
    connection_id: str,
) -> dict[str, Any]:
    """Test if a saved connection works."""
    from odooai.infrastructure.crypto import AESCrypto
    from odooai.infrastructure.db.database import get_session
    from odooai.infrastructure.db.models import OdooConnection
    from odooai.infrastructure.odoo.client import OdooClient

    settings = get_settings()
    if not settings.odoo_crypto_key:
        raise HTTPException(status_code=500, detail="Crypto not configured")

    user_id = getattr(request.state, "user_id", "anonymous")

    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        result = await session.execute(
            select(OdooConnection).where(
                OdooConnection.id == connection_id,
                OdooConnection.user_id == user_id,
            ),
        )
        conn = result.scalar_one_or_none()
    finally:
        with contextlib.suppress(StopAsyncIteration):
            await session_gen.__anext__()

    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")

    crypto = AESCrypto(key_b64=settings.odoo_crypto_key)
    api_key = crypto.decrypt(conn.api_key_encrypted)

    try:
        from odooai.domain.entities.connection import OdooApiType

        # Auto-detect: try JSON-2 first (Odoo 19+), fallback to XML-RPC (17/18)
        client = OdooClient(base_url=conn.url, db=conn.db_name, api_type=OdooApiType.XML_RPC)
        uid = await client.authenticate(conn.login, api_key)

        # Update last_connected_at
        session_gen2 = get_session()
        session2 = await session_gen2.__anext__()
        try:
            result2 = await session2.execute(
                select(OdooConnection).where(OdooConnection.id == connection_id),
            )
            c = result2.scalar_one_or_none()
            if c:
                c.last_connected_at = datetime.now(UTC)
                await session2.commit()
        finally:
            with contextlib.suppress(StopAsyncIteration):
                await session_gen2.__anext__()

        return {"status": "ok", "uid": uid}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


def _to_response(conn: Any) -> ConnectionResponse:
    """Convert DB model to response (no API key)."""
    return ConnectionResponse(
        id=conn.id,
        name=conn.name,
        url=conn.url,
        db_name=conn.db_name,
        login=conn.login,
        odoo_version=conn.odoo_version or "",
        is_default=conn.is_default,
        last_connected_at=str(conn.last_connected_at) if conn.last_connected_at else None,
    )
