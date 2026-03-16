"""Tests for Odoo domain filter anti-injection validation."""

import pytest

from odooai.exceptions import DomainInjectionError
from odooai.security.domain_validator import validate_domain


class TestValidDomains:
    """Test that valid Odoo domains pass validation."""

    def test_empty_domain(self) -> None:
        validate_domain([])

    def test_simple_condition(self) -> None:
        validate_domain([("state", "=", "draft")])

    def test_multiple_conditions(self) -> None:
        validate_domain([("state", "=", "draft"), ("partner_id", "!=", False)])

    def test_logical_operators(self) -> None:
        validate_domain(["|", ("state", "=", "draft"), ("state", "=", "sent")])

    def test_in_operator(self) -> None:
        validate_domain([("id", "in", [1, 2, 3])])

    def test_ilike_operator(self) -> None:
        validate_domain([("name", "ilike", "test")])

    def test_child_of(self) -> None:
        validate_domain([("category_id", "child_of", 5)])

    def test_list_conditions(self) -> None:
        validate_domain([["state", "=", "draft"]])

    def test_not_operator(self) -> None:
        validate_domain(["!", ("active", "=", False)])


class TestBlockedDomains:
    """Test that malicious/malformed domains are rejected."""

    def test_not_a_list(self) -> None:
        with pytest.raises(DomainInjectionError):
            validate_domain("not a list")  # type: ignore[arg-type]

    def test_invalid_element_type(self) -> None:
        with pytest.raises(DomainInjectionError):
            validate_domain([42])  # type: ignore[list-item]

    def test_wrong_condition_length(self) -> None:
        with pytest.raises(DomainInjectionError):
            validate_domain([("state", "=")])

    def test_invalid_operator(self) -> None:
        with pytest.raises(DomainInjectionError, match="Invalid operator"):
            validate_domain([("state", "DROP TABLE", "users")])

    def test_invalid_logical_operator(self) -> None:
        with pytest.raises(DomainInjectionError, match="Invalid logical"):
            validate_domain(["AND", ("state", "=", "draft")])

    def test_private_field(self) -> None:
        with pytest.raises(DomainInjectionError, match="Forbidden field"):
            validate_domain([("_compute_amount", "=", 0)])

    def test_sudo_field(self) -> None:
        with pytest.raises(DomainInjectionError, match="Forbidden field"):
            validate_domain([("sudo", "=", True)])

    def test_sql_injection_comment(self) -> None:
        with pytest.raises(DomainInjectionError, match="Suspicious pattern"):
            validate_domain([("name", "=", "test -- DROP TABLE")])

    def test_sql_injection_semicolon(self) -> None:
        with pytest.raises(DomainInjectionError, match="Suspicious pattern"):
            validate_domain([("name", "=", "test; DELETE FROM")])

    def test_sql_injection_union(self) -> None:
        with pytest.raises(DomainInjectionError, match="Suspicious pattern"):
            validate_domain([("name", "=", "x' UNION SELECT * FROM")])

    def test_sql_injection_in_list(self) -> None:
        with pytest.raises(DomainInjectionError, match="Suspicious pattern"):
            validate_domain([("name", "in", ["ok", "test; DROP TABLE"])])

    def test_non_string_field(self) -> None:
        with pytest.raises(DomainInjectionError, match="Field name must be"):
            validate_domain([(123, "=", "test")])  # type: ignore[list-item]

    def test_non_string_operator(self) -> None:
        with pytest.raises(DomainInjectionError, match="Operator must be"):
            validate_domain([("name", 42, "test")])  # type: ignore[list-item]
