"""
Module: infrastructure/odoo/client.py
Role: OdooClient facade — routes operations to JSON-2 or XML-RPC backend.
      One instance per Odoo connection (base_url + db + api_type).
Dependencies: domain ports, _json2, _xmlrpc
"""

from typing import Any

import structlog

from odooai.domain.entities.connection import OdooApiType
from odooai.domain.ports.i_odoo_client import IOdooClient
from odooai.domain.value_objects.odoo_user_info import OdooUserInfo
from odooai.exceptions import OdooConnectionError
from odooai.infrastructure.odoo._json2 import json2_authenticate, json2_call, json2_version
from odooai.infrastructure.odoo._xmlrpc import (
    xmlrpc_authenticate,
    xmlrpc_execute_kw,
    xmlrpc_version,
)

logger = structlog.get_logger(__name__)


class OdooClient(IOdooClient):
    """
    Async Odoo client supporting JSON-2 (Odoo 19+) and XML-RPC (Odoo 17/18).

    The api_type is fixed at construction. All methods present the same interface
    regardless of the underlying protocol.
    """

    def __init__(
        self,
        base_url: str,
        db: str,
        api_type: OdooApiType = OdooApiType.JSON2,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._db = db
        self._api_type = api_type

    async def authenticate(self, login: str, api_key: str) -> OdooUserInfo:
        """Authenticate and detect admin/internal/portal. Rejects portal."""
        if self._api_type == OdooApiType.XML_RPC:
            return await xmlrpc_authenticate(self._base_url, self._db, login, api_key)
        return await json2_authenticate(self._base_url, self._db, login, api_key)

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
        """Search and read records."""
        kw: dict[str, Any] = {"fields": fields, "limit": limit, "offset": offset}
        if order:
            kw["order"] = order
        return await self._call(  # type: ignore[no-any-return]
            api_key,
            uid,
            model,
            "search_read",
            args=[domain],
            kwargs=kw,
            json2_body={"domain": domain, **kw},
        )

    async def search_count(
        self,
        api_key: str,
        model: str,
        domain: list[Any],
        uid: int = 0,
    ) -> int:
        """Count matching records."""
        return await self._call(  # type: ignore[no-any-return]
            api_key,
            uid,
            model,
            "search_count",
            args=[domain],
            kwargs={},
            json2_body={"domain": domain},
        )

    async def create(
        self,
        api_key: str,
        model: str,
        values: dict[str, Any],
        uid: int = 0,
    ) -> int:
        """Create a record."""
        return await self._call(  # type: ignore[no-any-return]
            api_key,
            uid,
            model,
            "create",
            args=[values],
            kwargs={},
            json2_body={"vals_list": [values]},
        )

    async def write(
        self,
        api_key: str,
        model: str,
        ids: list[int],
        values: dict[str, Any],
        uid: int = 0,
    ) -> bool:
        """Update records."""
        return await self._call(  # type: ignore[no-any-return]
            api_key,
            uid,
            model,
            "write",
            args=[ids, values],
            kwargs={},
            json2_body={"ids": ids, "vals": values},
        )

    async def execute(
        self,
        api_key: str,
        model: str,
        method: str,
        res_ids: list[int],
        uid: int = 0,
        kwargs: dict[str, Any] | None = None,
    ) -> Any:
        """Execute a model method."""
        return await self._call(
            api_key,
            uid,
            model,
            method,
            args=[res_ids],
            kwargs=kwargs or {},
            json2_body={"ids": res_ids, **(kwargs or {})},
        )

    async def get_model_fields(
        self,
        api_key: str,
        model: str,
        uid: int = 0,
    ) -> dict[str, dict[str, Any]]:
        """Return fields_get() metadata for a model."""
        attrs = ["string", "type", "required", "readonly", "relation", "selection"]
        return await self._call(  # type: ignore[no-any-return]
            api_key,
            uid,
            model,
            "fields_get",
            args=[],
            kwargs={"attributes": attrs},
            json2_body={"attributes": attrs},
        )

    async def check_access_rights(
        self,
        api_key: str,
        model: str,
        operation: str,
        uid: int = 0,
    ) -> bool:
        """Check Odoo-level access rights."""
        if self._api_type == OdooApiType.XML_RPC:
            try:
                result = await xmlrpc_execute_kw(
                    self._base_url,
                    self._db,
                    uid,
                    api_key,
                    model,
                    "check_access_rights",
                    [operation],
                    {"raise_exception": False},
                )
                return bool(result)
            except Exception:
                return False

        # JSON-2: probe with search_count (Odoo enforces access automatically)
        try:
            await json2_call(
                self._base_url,
                self._db,
                api_key,
                model,
                "search_count",
                {"domain": []},
            )
            return True
        except Exception:
            return False

    async def get_server_version(self) -> str:
        """Detect Odoo server version."""
        if self._api_type == OdooApiType.XML_RPC:
            return await xmlrpc_version(self._base_url)
        return await json2_version(self._base_url, self._db)

    # ──────────────────────────────────────────────────────────────
    # Internal routing
    # ──────────────────────────────────────────────────────────────

    async def _call(
        self,
        api_key: str,
        uid: int,
        model: str,
        method: str,
        args: list[Any],
        kwargs: dict[str, Any],
        json2_body: dict[str, Any],
    ) -> Any:
        """Route a call to the appropriate backend."""
        if self._api_type == OdooApiType.XML_RPC:
            if not uid:
                raise OdooConnectionError(
                    "XML-RPC requires uid — authenticate first",
                    user_message="Internal error: missing user ID for Odoo call.",
                )
            return await xmlrpc_execute_kw(
                self._base_url,
                self._db,
                uid,
                api_key,
                model,
                method,
                args,
                kwargs,
            )
        return await json2_call(
            self._base_url,
            self._db,
            api_key,
            model,
            method,
            json2_body,
        )
