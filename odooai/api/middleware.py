"""
Module: api/middleware.py
Role: ASGI middleware for request ID injection + JWT authentication.
Dependencies: uuid, starlette, jwt
"""

import uuid
from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response

# Paths that don't require authentication
PUBLIC_PATHS = frozenset(
    {
        "/health",
        "/metrics",
        "/api/auth/signup",
        "/api/auth/login",
        "/api/waitlist",
        "/docs",
        "/openapi.json",
    }
)

# Path prefixes that don't require auth
PUBLIC_PREFIXES = ("/api/auth/",)


async def request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Inject a unique X-Request-ID header into every request and response."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def _is_public_path(path: str) -> bool:
    """Check if a path is public (no auth required)."""
    if path in PUBLIC_PATHS:
        return True
    return any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)


async def auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """
    JWT authentication middleware.

    Checks Authorization: Bearer <token> header on protected endpoints.
    Sets request.state.user_id and request.state.user_email if authenticated.
    Skips auth for public paths and in development mode (optional).
    """
    from odooai.config import get_settings

    settings = get_settings()
    path = request.url.path

    # Public paths — no auth needed
    if _is_public_path(path):
        return await call_next(request)

    # In development, auth is optional (for backward compatibility)
    auth_header = request.headers.get("Authorization", "")

    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            from odooai.api.routers.auth import decode_token

            payload = decode_token(token)
            request.state.user_id = payload.get("sub", "")
            request.state.user_email = payload.get("email", "")
        except Exception:
            if settings.is_production:
                return Response(
                    content='{"detail": "Invalid or expired token"}',
                    status_code=401,
                    media_type="application/json",
                )
    elif settings.is_production:
        # In production, auth is required for protected endpoints
        return Response(
            content='{"detail": "Authentication required"}',
            status_code=401,
            media_type="application/json",
        )
    else:
        # In development, set anonymous user
        request.state.user_id = "anonymous"
        request.state.user_email = "dev@localhost"

    return await call_next(request)
