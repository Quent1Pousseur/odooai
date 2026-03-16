"""Tests for Security Guardian pipeline."""

import pytest

from odooai.domain.value_objects.model_category import ModelCategory, ModelClassifier
from odooai.exceptions import BlockedMethodError, BlockedModelError
from odooai.security.guardian import (
    guard_method,
    guard_model_access,
    sanitize_response,
)


class TestGuardModelAccess:
    """Test the model classification gate."""

    def setup_method(self) -> None:
        ModelClassifier.clear_overrides()

    def test_blocked_raises(self) -> None:
        with pytest.raises(BlockedModelError, match="BLOCKED"):
            guard_model_access("ir.rule")

    def test_all_blocked_models_rejected(self) -> None:
        for model in (
            "ir.rule",
            "ir.model.access",
            "res.users",
            "res.groups",
            "ir.config_parameter",
            "ir.cron",
            "ir.mail_server",
        ):
            with pytest.raises(BlockedModelError):
                guard_model_access(model)

    def test_standard_passes(self) -> None:
        assert guard_model_access("sale.order") == ModelCategory.STANDARD

    def test_open_passes(self) -> None:
        assert guard_model_access("product.product") == ModelCategory.OPEN

    def test_sensitive_passes(self) -> None:
        assert guard_model_access("account.move") == ModelCategory.SENSITIVE


class TestGuardMethod:
    """Test the method blocking gate."""

    def test_unlink_blocked(self) -> None:
        with pytest.raises(BlockedMethodError, match="permanently blocked"):
            guard_method("unlink")

    def test_sudo_blocked(self) -> None:
        with pytest.raises(BlockedMethodError):
            guard_method("sudo")

    def test_underscore_sudo_blocked(self) -> None:
        with pytest.raises(BlockedMethodError):
            guard_method("_sudo")

    def test_search_read_allowed(self) -> None:
        guard_method("search_read")  # Should not raise

    def test_create_allowed(self) -> None:
        guard_method("create")

    def test_write_allowed(self) -> None:
        guard_method("write")

    def test_action_confirm_allowed(self) -> None:
        guard_method("action_confirm")


class TestSanitizeResponse:
    """Test the full sanitization pipeline."""

    def test_empty_records(self) -> None:
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=[],
            requested_fields=["id", "name"],
        )
        assert result.record_count == 0
        assert result.records == ()

    def test_standard_no_anonymization(self) -> None:
        records = [{"id": 1, "name": "SO001", "amount_total": 1500.0}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["id", "name", "amount_total"],
        )
        assert result.was_anonymized is False
        assert result.records[0]["amount_total"] == 1500.0

    def test_sensitive_anonymizes_amounts(self) -> None:
        records = [{"id": 1, "amount_total": 45780.50, "name": "INV/001"}]
        result = sanitize_response(
            model="account.move",
            category=ModelCategory.SENSITIVE,
            records=records,
            requested_fields=["id", "amount_total", "name"],
        )
        assert result.was_anonymized is True
        assert result.records[0]["amount_total"] == 45800.0

    def test_sensitive_anonymizes_emails(self) -> None:
        records = [{"id": 1, "email": "john@example.com"}]
        result = sanitize_response(
            model="hr.employee",
            category=ModelCategory.SENSITIVE,
            records=records,
            requested_fields=["id", "email"],
        )
        assert result.records[0]["email"] == "j***@e***.com"

    def test_sensitive_anonymizes_hr_names(self) -> None:
        records = [{"id": 1, "name": "John Doe"}]
        result = sanitize_response(
            model="hr.employee",
            category=ModelCategory.SENSITIVE,
            records=records,
            requested_fields=["id", "name"],
        )
        assert result.records[0]["name"] == "J*** D***"

    def test_sensitive_non_hr_names_now_masked(self) -> None:
        """Post red-team: names masked on ALL SENSITIVE models (prompt injection prevention)."""
        records = [{"id": 1, "name": "Invoice 001"}]
        result = sanitize_response(
            model="account.move",
            category=ModelCategory.SENSITIVE,
            records=records,
            requested_fields=["id", "name"],
        )
        assert result.records[0]["name"] == "I*** 0***"

    def test_open_no_processing(self) -> None:
        records = [{"id": 1, "name": "Product A", "list_price": 99.99}]
        result = sanitize_response(
            model="product.product",
            category=ModelCategory.OPEN,
            records=records,
            requested_fields=["id", "name", "list_price"],
        )
        assert result.was_anonymized is False
        assert result.records[0]["list_price"] == 99.99

    def test_hidden_fields_removed(self) -> None:
        records = [{"id": 1, "name": "Test", "password": "secret123"}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["id", "name", "password"],
        )
        assert "password" not in result.records[0]

    def test_many2one_normalized(self) -> None:
        records = [{"id": 1, "partner_id": [42, "Acme Corp"]}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["id", "partner_id"],
        )
        assert result.records[0]["partner_id"] == {"id": 42, "name": "Acme Corp"}

    def test_fields_filtered(self) -> None:
        records = [{"id": 1, "name": "SO001", "secret_note": "internal"}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["id", "name"],
        )
        assert "secret_note" not in result.records[0]
        assert "name" in result.records[0]

    def test_id_always_kept(self) -> None:
        records = [{"id": 1, "name": "SO001"}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["name"],
        )
        assert "id" in result.records[0]

    def test_fields_returned_tuple(self) -> None:
        records = [{"id": 1, "name": "SO001", "state": "draft"}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["id", "name", "state"],
        )
        assert isinstance(result.fields_returned, tuple)
        assert "id" in result.fields_returned
        assert "name" in result.fields_returned

    def test_m2o_name_masked_on_sensitive(self) -> None:
        """Many2one display names must be masked on SENSITIVE models."""
        records = [{"id": 1, "partner_id": [42, "John Doe"]}]
        result = sanitize_response(
            model="account.move",
            category=ModelCategory.SENSITIVE,
            records=records,
            requested_fields=["id", "partner_id"],
        )
        partner = result.records[0]["partner_id"]
        assert partner["id"] == 42
        assert partner["name"] == "J*** D***"

    def test_m2o_name_not_masked_on_standard(self) -> None:
        """Many2one display names should NOT be masked on STANDARD models."""
        records = [{"id": 1, "partner_id": [42, "Acme Corp"]}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["id", "partner_id"],
        )
        assert result.records[0]["partner_id"]["name"] == "Acme Corp"

    def test_hidden_field_pattern_match(self) -> None:
        """Fields matching _key, _secret, _token patterns should be hidden."""
        records = [{"id": 1, "name": "Test", "encryption_key": "abc", "oauth_token": "xyz"}]
        result = sanitize_response(
            model="sale.order",
            category=ModelCategory.STANDARD,
            records=records,
            requested_fields=["id", "name", "encryption_key", "oauth_token"],
        )
        assert "encryption_key" not in result.records[0]
        assert "oauth_token" not in result.records[0]
        assert "name" in result.records[0]

    def test_res_partner_is_sensitive(self) -> None:
        """res.partner should be classified as SENSITIVE."""
        category = guard_model_access("res.partner")
        assert category == ModelCategory.SENSITIVE
