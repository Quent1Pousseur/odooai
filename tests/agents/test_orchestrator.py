"""Tests for Orchestrator — domain detection + Guardian wire."""

import pytest

from odooai.agents.orchestrator import (
    detect_domain,
    guarded_odoo_read,
    guarded_odoo_write_check,
)
from odooai.domain.value_objects.model_category import ModelCategory, ModelClassifier
from odooai.exceptions import BlockedMethodError, BlockedModelError, DomainInjectionError


class TestDetectDomain:
    """Test keyword-based domain detection."""

    def test_sales_keywords(self) -> None:
        assert detect_domain("Comment creer un devis ?") == "sales_crm"

    def test_stock_keywords(self) -> None:
        assert detect_domain("Comment gerer mon inventaire ?") == "supply_chain"

    def test_accounting_keywords(self) -> None:
        assert detect_domain("Comment configurer les relances de paiement ?") == "accounting"

    def test_hr_keywords(self) -> None:
        assert detect_domain("Comment gerer les conges des employes ?") == "hr_payroll"

    def test_manufacturing_keywords(self) -> None:
        assert detect_domain("Comment creer un ordre de fabrication ?") == "manufacturing"

    def test_no_match_returns_none(self) -> None:
        assert detect_domain("Quelle est la meteo ?") is None

    def test_multi_domain_highest_score(self) -> None:
        # "commande client stock" → sales (commande, client) > supply_chain (stock)
        result = detect_domain("commande client")
        assert result == "sales_crm"


class TestGuardedOdooRead:
    """Test Guardian wire for read operations."""

    def setup_method(self) -> None:
        ModelClassifier.clear_overrides()

    def test_blocked_model_rejected(self) -> None:
        with pytest.raises(BlockedModelError):
            guarded_odoo_read("ir.rule", [{"id": 1}], ["id"])

    def test_standard_model_passes(self) -> None:
        result = guarded_odoo_read(
            "sale.order",
            [{"id": 1, "name": "SO001", "amount_total": 1500.0}],
            ["id", "name", "amount_total"],
        )
        assert result.record_count == 1
        assert result.was_anonymized is False

    def test_sensitive_model_anonymized(self) -> None:
        result = guarded_odoo_read(
            "hr.employee",
            [{"id": 1, "name": "John Doe", "email": "john@company.com", "salary": 4500.0}],
            ["id", "name", "email", "salary"],
        )
        assert result.was_anonymized is True
        assert result.records[0]["name"] == "J*** D***"
        assert "company.com" not in str(result.records[0]["email"])
        assert result.records[0]["salary"] == 4500.0  # ceil(4500/100)*100

    def test_open_model_not_anonymized(self) -> None:
        result = guarded_odoo_read(
            "product.product",
            [{"id": 1, "name": "Widget", "list_price": 99.99}],
            ["id", "name", "list_price"],
        )
        assert result.was_anonymized is False
        assert result.records[0]["list_price"] == 99.99

    def test_hidden_fields_removed(self) -> None:
        result = guarded_odoo_read(
            "sale.order",
            [{"id": 1, "name": "SO001", "password": "secret"}],
            ["id", "name", "password"],
        )
        assert "password" not in result.records[0]


class TestGuardedOdooWriteCheck:
    """Test Guardian wire for write operations."""

    def setup_method(self) -> None:
        ModelClassifier.clear_overrides()

    def test_blocked_model_rejected(self) -> None:
        with pytest.raises(BlockedModelError):
            guarded_odoo_write_check("res.users", "write")

    def test_blocked_method_rejected(self) -> None:
        with pytest.raises(BlockedMethodError):
            guarded_odoo_write_check("sale.order", "unlink")

    def test_sudo_rejected(self) -> None:
        with pytest.raises(BlockedMethodError):
            guarded_odoo_write_check("sale.order", "sudo")

    def test_malicious_domain_rejected(self) -> None:
        with pytest.raises(DomainInjectionError):
            guarded_odoo_write_check(
                "sale.order",
                "search_read",
                domain=[("name", "=", "test; DROP TABLE")],
            )

    def test_valid_write_passes(self) -> None:
        category = guarded_odoo_write_check("sale.order", "write")
        assert category == ModelCategory.STANDARD

    def test_valid_create_passes(self) -> None:
        category = guarded_odoo_write_check("sale.order", "create")
        assert category == ModelCategory.STANDARD

    def test_valid_domain_passes(self) -> None:
        category = guarded_odoo_write_check(
            "sale.order",
            "search_read",
            domain=[("state", "=", "draft")],
        )
        assert category == ModelCategory.STANDARD
