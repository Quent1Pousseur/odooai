"""
Module: main.py
Role: FastAPI application factory with lifespan management and dependency wiring.
Dependencies: fastapi, infrastructure, api
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import sentry_sdk
import structlog
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from odooai.api.dependencies import wire
from odooai.api.middleware import auth_middleware, request_id_middleware
from odooai.api.routers.auth import router as auth_router
from odooai.api.routers.chat import router as chat_router
from odooai.api.routers.conversations import router as conversations_router
from odooai.api.routers.health import router as health_router
from odooai.api.routers.metrics import router as metrics_router
from odooai.api.routers.waitlist import router as waitlist_router
from odooai.config import get_settings
from odooai.domain.entities.connection import OdooApiType
from odooai.infrastructure.cache.redis_client import RedisClient
from odooai.infrastructure.crypto import AESCrypto
from odooai.infrastructure.llm.anthropic_provider import AnthropicProvider
from odooai.infrastructure.odoo._http import close_http_pool
from odooai.infrastructure.odoo.client import OdooClient
from odooai.logging import setup_logging

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: wire dependencies on startup, cleanup on shutdown."""
    settings = get_settings()

    # Sentry error tracking (learning SOC #26 — 3 lines)
    if settings.sentry_dsn:
        sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.1)

    # Configure structured logging
    setup_logging(log_level=settings.log_level, is_production=settings.is_production)

    # Fail-fast in production if config is incomplete
    if settings.is_production:
        settings.validate_production()

    # Initialize database
    from odooai.infrastructure.db.database import close_db, init_db

    await init_db()

    # Wire concrete implementations
    odoo_client = OdooClient(
        base_url=settings.odoo_url or "http://localhost:8069",
        db=settings.odoo_db or "odoo",
        api_type=OdooApiType.JSON2,
    )

    # Crypto: skip in dev if key not configured
    crypto: AESCrypto | None = None
    if settings.odoo_crypto_key:
        crypto = AESCrypto(
            key_b64=settings.odoo_crypto_key,
            previous_key_b64=settings.odoo_crypto_key_previous,
        )

    wire(
        odoo_client=odoo_client,
        cache=RedisClient(),
        llm_provider=AnthropicProvider(),
        crypto=crypto,
    )

    logger.info(
        "OdooAI started",
        environment=settings.environment,
        odoo_url=settings.odoo_url or "(not configured)",
    )

    yield

    await close_http_pool()
    await close_db()
    logger.info("OdooAI shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="OdooAI",
        description="AI Business Analyst that has read every line of Odoo source code.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Rate limiting (learning DevSecOps #24)
    limiter = Limiter(key_func=get_remote_address)
    application.state.limiter = limiter
    application.add_exception_handler(
        RateLimitExceeded,
        _rate_limit_exceeded_handler,  # type: ignore[arg-type]
    )

    # CORS — restrictif en prod, permissif en dev
    from starlette.middleware.cors import CORSMiddleware

    settings = get_settings()
    origins = (
        ["https://odooai.com", "https://www.odooai.com"]
        if settings.is_production
        else ["http://localhost:3000"]
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
    application.add_middleware(BaseHTTPMiddleware, dispatch=request_id_middleware)
    application.include_router(auth_router)
    application.include_router(health_router)
    application.include_router(chat_router)
    application.include_router(conversations_router)
    application.include_router(waitlist_router)
    application.include_router(metrics_router)

    # OpenTelemetry (learning Observability #38)
    from odooai.infrastructure.telemetry import setup_telemetry

    setup_telemetry(application)

    return application


app = create_app()
