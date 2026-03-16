"""
Module: domain/ports/i_odoo_client.py
Role: Abstract interface for Odoo API communication.
      Implementations store url/db at construction time (one client per Odoo instance).
Dependencies: domain value objects
"""

from abc import ABC, abstractmethod
from typing import Any

from odooai.domain.value_objects.odoo_user_info import OdooUserInfo


class IOdooClient(ABC):
    """Port for Odoo API operations (XML-RPC or JSON-2)."""

    @abstractmethod
    async def authenticate(self, login: str, api_key: str) -> OdooUserInfo:
        """
        Authenticate against Odoo and return user info.

        Detects admin/internal/portal status. Rejects portal users.

        Raises:
            OdooAuthError: Invalid credentials or portal user.
            OdooConnectionError: Network failure.
        """

    @abstractmethod
    async def search_read(
        self,
        api_key: str,
        model: str,
        domain: list[Any],
        fields: list[str],
        limit: int = 10,
        offset: int = 0,
        uid: int = 0,
        order: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search and read records in a single round-trip."""

    @abstractmethod
    async def search_count(
        self,
        api_key: str,
        model: str,
        domain: list[Any],
        uid: int = 0,
    ) -> int:
        """Count records matching a domain."""

    @abstractmethod
    async def read_group(
        self,
        api_key: str,
        model: str,
        domain: list[Any],
        fields: list[str],
        groupby: list[str],
        uid: int = 0,
        order: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Aggregate records using GROUP BY (Odoo read_group)."""

    @abstractmethod
    async def name_search(
        self,
        api_key: str,
        model: str,
        name: str,
        domain: list[Any] | None = None,
        limit: int = 10,
        uid: int = 0,
    ) -> list[dict[str, Any]]:
        """Search records by display name. Returns list of {id, name} dicts."""

    @abstractmethod
    async def create(
        self,
        api_key: str,
        model: str,
        values: dict[str, Any],
        uid: int = 0,
    ) -> int:
        """Create a record and return its ID."""

    @abstractmethod
    async def write(
        self,
        api_key: str,
        model: str,
        ids: list[int],
        values: dict[str, Any],
        uid: int = 0,
    ) -> bool:
        """Update records."""

    @abstractmethod
    async def execute(
        self,
        api_key: str,
        model: str,
        method: str,
        res_ids: list[int],
        uid: int = 0,
        kwargs: dict[str, Any] | None = None,
    ) -> Any:
        """Execute a model method (e.g. action_confirm)."""

    @abstractmethod
    async def get_model_fields(
        self,
        api_key: str,
        model: str,
        uid: int = 0,
    ) -> dict[str, dict[str, Any]]:
        """Return fields_get() metadata for a model."""

    @abstractmethod
    async def check_access_rights(
        self,
        api_key: str,
        model: str,
        operation: str,
        uid: int = 0,
    ) -> bool:
        """Check if the user has access rights for an operation on a model."""

    @abstractmethod
    async def get_server_version(self) -> str:
        """Detect the Odoo server version. Returns '' on failure."""
