"""
Module: api/routers/auth.py
Role: Authentication endpoints — signup, login, JWT tokens.
Dependencies: bcrypt, jwt, sqlalchemy
"""

from __future__ import annotations

import contextlib
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
import structlog
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select

from odooai.config import get_settings

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


class AuthRequest(BaseModel):
    """Signup/login request."""

    email: str
    password: str


class AuthResponse(BaseModel):
    """Auth response with JWT token."""

    token: str
    user_id: str


def _hash_password(password: str) -> str:
    """Hash a password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()


def _verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def _create_token(user_id: str, email: str) -> str:
    """Create a JWT token."""
    settings = get_settings()
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(UTC) + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, str]:
    """Decode and validate a JWT token."""
    settings = get_settings()
    try:
        payload: dict[str, str] = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")  # noqa: B904
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")  # noqa: B904


@router.post("/signup", response_model=AuthResponse)
@limiter.limit("5/minute")
async def signup(request: Request, body: AuthRequest) -> AuthResponse:
    """Register a new user."""
    from odooai.infrastructure.db.database import get_session
    from odooai.infrastructure.db.models import User

    if len(body.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        # Check if email already exists
        existing = await session.execute(
            select(User).where(User.email == body.email),
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already registered")

        user = User(
            email=body.email,
            password_hash=_hash_password(body.password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    finally:
        with contextlib.suppress(StopAsyncIteration):
            await session_gen.__anext__()

    token = _create_token(user.id, user.email)
    logger.info("User signed up", email=body.email, user_id=user.id)
    return AuthResponse(token=token, user_id=user.id)


@router.post("/login", response_model=AuthResponse)
@limiter.limit("10/minute")
async def login(request: Request, body: AuthRequest) -> AuthResponse:
    """Login with email and password."""
    from odooai.infrastructure.db.database import get_session
    from odooai.infrastructure.db.models import User

    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        result = await session.execute(
            select(User).where(User.email == body.email),
        )
        user = result.scalar_one_or_none()
    finally:
        with contextlib.suppress(StopAsyncIteration):
            await session_gen.__anext__()

    if not user or not _verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    token = _create_token(user.id, user.email)
    logger.info("User logged in", email=body.email, user_id=user.id)
    return AuthResponse(token=token, user_id=user.id)
