"""Tests for OdooClient facade and error mapping."""

from unittest.mock import AsyncMock, patch

import pytest

from odooai.domain.entities.connection import OdooApiType
from odooai.domain.value_objects.odoo_user_info import OdooUserInfo
from odooai.exceptions import OdooAuthError, OdooConnectionError
from odooai.infrastructure.odoo._errors import (
    raise_from_json2_error,
    raise_from_xmlrpc_fault,
)
from odooai.infrastructure.odoo.client import OdooClient


class TestOdooClientInit:
    """Test client construction."""

    def test_strips_trailing_slash(self) -> None:
        client = OdooClient(base_url="https://example.com/", db="test")
        assert client._base_url == "https://example.com"

    def test_default_api_type_is_json2(self) -> None:
        client = OdooClient(base_url="https://example.com", db="test")
        assert client._api_type == OdooApiType.JSON2

    def test_xmlrpc_api_type(self) -> None:
        client = OdooClient(
            base_url="https://example.com",
            db="test",
            api_type=OdooApiType.XML_RPC,
        )
        assert client._api_type == OdooApiType.XML_RPC


class TestOdooClientRouting:
    """Test that calls route to the correct backend."""

    @pytest.mark.asyncio
    async def test_authenticate_routes_json2(self) -> None:
        with patch(
            "odooai.infrastructure.odoo.client.json2_authenticate",
            new_callable=AsyncMock,
        ) as mock:
            mock.return_value = OdooUserInfo(
                uid=2,
                login="admin",
                name="Admin",
                is_system=True,
                is_internal=True,
                lang="en_US",
                tz="UTC",
            )
            client = OdooClient("https://odoo.test", "mydb", OdooApiType.JSON2)
            info = await client.authenticate("admin", "key123")
            assert info.uid == 2
            mock.assert_called_once_with("https://odoo.test", "mydb", "admin", "key123")

    @pytest.mark.asyncio
    async def test_authenticate_routes_xmlrpc(self) -> None:
        with patch(
            "odooai.infrastructure.odoo.client.xmlrpc_authenticate",
            new_callable=AsyncMock,
        ) as mock:
            mock.return_value = OdooUserInfo(
                uid=5,
                login="user@co.com",
                name="User",
                is_system=False,
                is_internal=True,
                lang="fr_FR",
                tz="Europe/Paris",
            )
            client = OdooClient("https://odoo.test", "mydb", OdooApiType.XML_RPC)
            info = await client.authenticate("user@co.com", "key456")
            assert info.uid == 5
            assert info.is_internal is True

    @pytest.mark.asyncio
    async def test_search_read_routes_json2(self) -> None:
        with patch(
            "odooai.infrastructure.odoo.client.json2_call",
            new_callable=AsyncMock,
        ) as mock:
            mock.return_value = [{"id": 1, "name": "SO001"}]
            client = OdooClient("https://odoo.test", "mydb", OdooApiType.JSON2)
            result = await client.search_read(
                api_key="key",
                model="sale.order",
                domain=[],
                fields=["id", "name"],
            )
            assert result == [{"id": 1, "name": "SO001"}]

    @pytest.mark.asyncio
    async def test_xmlrpc_requires_uid(self) -> None:
        client = OdooClient("https://odoo.test", "mydb", OdooApiType.XML_RPC)
        with pytest.raises(OdooConnectionError, match="requires uid"):
            await client.search_read(
                api_key="key",
                model="sale.order",
                domain=[],
                fields=["id"],
                uid=0,
            )


class TestErrorMapping:
    """Test error mapping functions."""

    def test_json2_auth_error(self) -> None:
        with pytest.raises(OdooAuthError):
            raise_from_json2_error(401, {"message": "Unauthorized"})

    def test_json2_forbidden(self) -> None:
        with pytest.raises(OdooAuthError):
            raise_from_json2_error(403, {"message": "Forbidden"})

    def test_json2_not_found(self) -> None:
        from odooai.exceptions import OdooRecordNotFoundError

        with pytest.raises(OdooRecordNotFoundError):
            raise_from_json2_error(404, {"message": "Not found"})

    def test_json2_validation_error(self) -> None:
        from odooai.exceptions import OdooValidationError

        with pytest.raises(OdooValidationError):
            raise_from_json2_error(400, {"name": "ValidationError", "message": "bad"})

    def test_xmlrpc_access_error(self) -> None:
        with pytest.raises(OdooAuthError):
            raise_from_xmlrpc_fault("AccessError: denied", "sale.order", "read")

    def test_xmlrpc_missing_error(self) -> None:
        from odooai.exceptions import OdooRecordNotFoundError

        with pytest.raises(OdooRecordNotFoundError):
            raise_from_xmlrpc_fault("MissingError: record does not exist", "sale.order", "read")

    def test_xmlrpc_cannot_marshal_no_raise(self) -> None:
        # "cannot marshal" should NOT raise — it means the action succeeded
        raise_from_xmlrpc_fault("cannot marshal <class 'recordset'>", "sale.order", "message_post")

    def test_xmlrpc_validation_error(self) -> None:
        from odooai.exceptions import OdooValidationError

        with pytest.raises(OdooValidationError):
            raise_from_xmlrpc_fault("ValidationError: field required", "sale.order", "create")


class TestOdooClientVersion:
    """Test version detection routing."""

    @pytest.mark.asyncio
    async def test_version_routes_json2(self) -> None:
        with patch(
            "odooai.infrastructure.odoo.client.json2_version",
            new_callable=AsyncMock,
        ) as mock:
            mock.return_value = "19.0"
            client = OdooClient("https://odoo.test", "mydb", OdooApiType.JSON2)
            version = await client.get_server_version()
            assert version == "19.0"

    @pytest.mark.asyncio
    async def test_version_routes_xmlrpc(self) -> None:
        with patch(
            "odooai.infrastructure.odoo.client.xmlrpc_version",
            new_callable=AsyncMock,
        ) as mock:
            mock.return_value = "17.0"
            client = OdooClient("https://odoo.test", "mydb", OdooApiType.XML_RPC)
            version = await client.get_server_version()
            assert version == "17.0"
