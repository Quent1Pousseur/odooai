"""
Module: main.py
Role: FastAPI application factory with lifespan management and dependency wiring.
Dependencies: fastapi, infrastructure, api
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from odooai.api.dependencies import wire
from odooai.api.middleware import request_id_middleware
from odooai.api.routers.health import router as health_router
from odooai.config import get_settings
from odooai.infrastructure.cache.redis_client import RedisClient
from odooai.infrastructure.crypto import AESCrypto
from odooai.infrastructure.llm.anthropic_provider import AnthropicProvider
from odooai.infrastructure.odoo.client import OdooClient


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: wire dependencies on startup, cleanup on shutdown."""
    settings = get_settings()

    # Wire concrete implementations
    wire(
        odoo_client=OdooClient(),
        cache=RedisClient(),
        llm_provider=AnthropicProvider(),
        crypto=AESCrypto(
            key_b64=settings.odoo_crypto_key,
            previous_key_b64=settings.odoo_crypto_key_previous,
        ),
    )

    yield

    # Cleanup (future: close connection pools)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="OdooAI",
        description="AI Business Analyst that has read every line of Odoo source code.",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.add_middleware(BaseHTTPMiddleware, dispatch=request_id_middleware)
    application.include_router(health_router)

    return application


app = create_app()
