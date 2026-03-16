"""Tests for domain value objects (frozen dataclasses)."""

import pytest

from odooai.domain.value_objects.odoo_user_info import OdooUserInfo
from odooai.domain.value_objects.sanitized_response import SanitizedResponse


class TestOdooUserInfo:
    """Test OdooUserInfo frozen dataclass."""

    def test_creation(self) -> None:
        info = OdooUserInfo(
            uid=2,
            login="admin",
            name="Admin",
            is_system=True,
            is_internal=True,
            lang="en_US",
            tz="UTC",
        )
        assert info.uid == 2
        assert info.login == "admin"

    def test_frozen(self) -> None:
        info = OdooUserInfo(
            uid=2,
            login="admin",
            name="Admin",
            is_system=True,
            is_internal=True,
            lang="en_US",
            tz="UTC",
        )
        with pytest.raises(AttributeError):
            info.uid = 99  # type: ignore[misc]

    def test_equality(self) -> None:
        a = OdooUserInfo(
            uid=2,
            login="a",
            name="A",
            is_system=False,
            is_internal=True,
            lang="fr_FR",
            tz="Europe/Paris",
        )
        b = OdooUserInfo(
            uid=2,
            login="a",
            name="A",
            is_system=False,
            is_internal=True,
            lang="fr_FR",
            tz="Europe/Paris",
        )
        assert a == b


class TestSanitizedResponse:
    """Test SanitizedResponse frozen dataclass."""

    def test_defaults(self) -> None:
        resp = SanitizedResponse(model="sale.order")
        assert resp.records == ()
        assert resp.fields_returned == ()
        assert resp.record_count == 0
        assert resp.was_anonymized is False

    def test_with_data(self) -> None:
        resp = SanitizedResponse(
            model="sale.order",
            records=({"id": 1, "name": "SO001"},),
            fields_returned=("id", "name"),
            record_count=1,
            was_anonymized=True,
        )
        assert len(resp.records) == 1
        assert resp.was_anonymized is True

    def test_frozen(self) -> None:
        resp = SanitizedResponse(model="sale.order")
        with pytest.raises(AttributeError):
            resp.model = "other"  # type: ignore[misc]
