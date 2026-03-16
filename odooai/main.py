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

    from odooai.domain.entities.connection import OdooApiType
    from odooai.infrastructure.odoo._http import close_http_pool

    # Wire concrete implementations
    # OdooClient needs a real Odoo connection — use placeholder in dev
    odoo_client = OdooClient(
        base_url=settings.odoo_url or "http://localhost:8069",
        db=settings.odoo_db or "odoo",
        api_type=OdooApiType.JSON2,
    )

    wire(
        odoo_client=odoo_client,
        cache=RedisClient(),
        llm_provider=AnthropicProvider(),
        crypto=AESCrypto(
            key_b64=settings.odoo_crypto_key,
            previous_key_b64=settings.odoo_crypto_key_previous,
        ),
    )

    yield

    await close_http_pool()


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
