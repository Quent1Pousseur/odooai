"""
Module: infrastructure/odoo/client.py
Role: Stub Odoo client. Full implementation in ODAI-CORE-002.
Dependencies: domain/ports/i_odoo_client
"""

from typing import Any

from odooai.domain.ports.i_odoo_client import IOdooClient
from odooai.domain.value_objects.odoo_user_info import OdooUserInfo


class OdooClient(IOdooClient):
    """Stub Odoo client — raises NotImplementedError for all operations."""

    async def authenticate(
        self,
        url: str,
        database: str,
        login: str,
        api_key: str,
    ) -> OdooUserInfo:
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")

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
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")

    async def search_count(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        domain: list[Any],
    ) -> int:
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")

    async def create(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        values: dict[str, Any],
    ) -> int:
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")

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
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")

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
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")

    async def get_model_fields(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
    ) -> dict[str, dict[str, Any]]:
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")

    async def check_access_rights(
        self,
        url: str,
        database: str,
        uid: int,
        api_key: str,
        model: str,
        operation: str,
    ) -> bool:
        raise NotImplementedError("OdooClient: implement in ODAI-CORE-002")
