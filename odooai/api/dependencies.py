"""
Module: api/dependencies.py
Role: Dependency injection wiring for FastAPI.
      No DI framework — module-level singletons set via wire().
Dependencies: domain/ports
"""

from odooai.domain.ports.i_cache import ICache
from odooai.domain.ports.i_crypto import ICrypto
from odooai.domain.ports.i_llm_provider import ILLMProvider
from odooai.domain.ports.i_odoo_client import IOdooClient

_odoo_client: IOdooClient | None = None
_cache: ICache | None = None
_llm_provider: ILLMProvider | None = None
_crypto: ICrypto | None = None


def wire(
    odoo_client: IOdooClient,
    cache: ICache,
    llm_provider: ILLMProvider,
    crypto: ICrypto | None,
) -> None:
    """
    Wire concrete implementations to module-level singletons.

    Called once during application lifespan startup.
    """
    global _odoo_client, _cache, _llm_provider, _crypto
    _odoo_client = odoo_client
    _cache = cache
    _llm_provider = llm_provider
    _crypto = crypto


def get_odoo_client() -> IOdooClient:
    """FastAPI Depends() factory for IOdooClient."""
    assert _odoo_client is not None, "Dependencies not wired. Call wire() first."
    return _odoo_client


def get_cache() -> ICache:
    """FastAPI Depends() factory for ICache."""
    assert _cache is not None, "Dependencies not wired. Call wire() first."
    return _cache


def get_llm_provider() -> ILLMProvider:
    """FastAPI Depends() factory for ILLMProvider."""
    assert _llm_provider is not None, "Dependencies not wired. Call wire() first."
    return _llm_provider


def get_crypto() -> ICrypto:
    """FastAPI Depends() factory for ICrypto."""
    assert _crypto is not None, "Dependencies not wired. Call wire() first."
    return _crypto
