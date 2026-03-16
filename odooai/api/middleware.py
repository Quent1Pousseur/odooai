"""
Module: api/middleware.py
Role: ASGI middleware for request ID injection.
Dependencies: uuid, starlette
"""

import uuid
from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response


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
