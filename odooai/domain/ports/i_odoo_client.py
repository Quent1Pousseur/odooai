"""
Module: domain/ports/i_odoo_client.py
Role: Abstract interface for Odoo API communication.
Dependencies: domain value objects
"""

from abc import ABC, abstractmethod
from typing import Any

from odooai.domain.value_objects.odoo_user_info import OdooUserInfo


class IOdooClient(ABC):
    """Port for Odoo API operations (XML-RPC or JSON-RPC)."""

    @abstractmethod
    async def authenticate(
        self,
        url: str,
        database: str,
        login: str,
        api_key: str,
    ) -> OdooUserInfo:
        """Authenticate and return user info."""

    @abstractmethod
    async def search_read(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        domain: list[Any],
        fields: list[str],
        limit: int = 10,
        offset: int = 0,
        order: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search and read records."""

    @abstractmethod
    async def search_count(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        domain: list[Any],
    ) -> int:
        """Count records matching a domain."""

    @abstractmethod
    async def create(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        values: dict[str, Any],
    ) -> int:
        """Create a record and return its ID."""

    @abstractmethod
    async def write(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        ids: list[int],
        values: dict[str, Any],
    ) -> bool:
        """Update records."""

    @abstractmethod
    async def execute(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        method: str,
        res_ids: list[int],
    ) -> Any:
        """Execute a model method (e.g. action_confirm)."""

    @abstractmethod
    async def get_model_fields(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
    ) -> dict[str, dict[str, Any]]:
        """Return fields_get() metadata for a model."""

    @abstractmethod
    async def check_access_rights(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        operation: str,
    ) -> bool:
        """Check if the user has access rights for an operation on a model."""
