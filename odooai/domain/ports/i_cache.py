"""
Module: domain/ports/i_cache.py
Role: Abstract interface for caching.
Dependencies: none
"""

from abc import ABC, abstractmethod
from typing import Any


class ICache(ABC):
    """Port for cache operations (Redis or in-memory)."""

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Get a string value by key."""

    @abstractmethod
    async def get_json(self, key: str) -> Any | None:
        """Get and deserialize a JSON value by key."""

    @abstractmethod
    async def set_json(self, key: str, value: Any, ttl: int = 300) -> None:
        """Serialize and store a JSON value with TTL in seconds."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a key."""

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists."""
