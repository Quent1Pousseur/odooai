"""
Module: infrastructure/cache/redis_client.py
Role: Stub Redis cache client. Full implementation when Redis is needed.
Dependencies: domain/ports/i_cache
"""

from typing import Any

from odooai.domain.ports.i_cache import ICache


class RedisClient(ICache):
    """Stub cache client — in-memory dict for development."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self._store.get(key)

    async def get_json(self, key: str) -> Any | None:
        import json

        raw = self._store.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set_json(self, key: str, value: Any, ttl: int = 300) -> None:
        import json

        self._store[key] = json.dumps(value)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def exists(self, key: str) -> bool:
        return key in self._store
