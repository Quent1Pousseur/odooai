"""Tests for anonymizer functions."""

from odooai.security.anonymizer import (
    anonymize_field_value,
    anonymize_record,
    mask_email,
    mask_name,
    mask_phone,
    redact,
    round_amount,
)


class TestMaskEmail:
    def test_normal_email(self) -> None:
        assert mask_email("john@example.com") == "j***@example.com"

    def test_single_char_local(self) -> None:
        assert mask_email("j@example.com") == "*@example.com"

    def test_not_email(self) -> None:
        assert mask_email("not-an-email") == "not-an-email"


class TestMaskName:
    def test_full_name(self) -> None:
        assert mask_name("John Doe") == "J*** D***"

    def test_single_name(self) -> None:
        assert mask_name("John") == "J***"

    def test_empty(self) -> None:
        assert mask_name("") == ""

    def test_single_char(self) -> None:
        assert mask_name("J") == "J"


class TestRoundAmount:
    def test_round_up(self) -> None:
        assert round_amount(45780.50) == 45800.0

    def test_exact_hundred(self) -> None:
        assert round_amount(100.0) == 100.0

    def test_small_amount(self) -> None:
        assert round_amount(42.0) == 100.0

    def test_custom_precision(self) -> None:
        assert round_amount(1234.0, precision=1000) == 2000.0


class TestMaskPhone:
    def test_normal_phone(self) -> None:
        assert mask_phone("+33 6 12 34 56 78") == "***78"

    def test_short_phone(self) -> None:
        assert mask_phone("12") == "***"


class TestRedact:
    def test_redacts_anything(self) -> None:
        assert redact("secret") == "[REDACTED]"
        assert redact(12345) == "[REDACTED]"


class TestAnonymizeFieldValue:
    """Test pattern-based field anonymization."""

    def test_amount_field(self) -> None:
        assert anonymize_field_value("amount_total", 45780.50) == 45800.0

    def test_price_field(self) -> None:
        assert anonymize_field_value("list_price", 99.0) == 100.0

    def test_salary_field(self) -> None:
        assert anonymize_field_value("salary", 3500.0) == 3500.0  # ceil(3500/100)*100

    def test_email_field(self) -> None:
        assert anonymize_field_value("email", "john@co.com") == "j***@co.com"

    def test_phone_field(self) -> None:
        assert anonymize_field_value("phone", "+33612345678") == "***78"

    def test_mobile_field(self) -> None:
        assert anonymize_field_value("mobile", "+33612345678") == "***78"

    def test_hr_name_masked(self) -> None:
        result = anonymize_field_value("name", "John Doe", model="hr.employee")
        assert result == "J*** D***"

    def test_non_hr_name_not_masked(self) -> None:
        result = anonymize_field_value("name", "Invoice 001", model="account.move")
        assert result == "Invoice 001"

    def test_unmatched_field_unchanged(self) -> None:
        assert anonymize_field_value("state", "draft") == "draft"

    def test_non_numeric_amount_unchanged(self) -> None:
        assert anonymize_field_value("amount_total", "N/A") == "N/A"


class TestAnonymizeRecord:
    """Test full record anonymization."""

    def test_hr_record(self) -> None:
        record: dict[str, object] = {
            "id": 1,
            "name": "Jane Smith",
            "email": "jane@company.com",
            "salary": 4200.0,
            "phone": "+33612345678",
        }
        result = anonymize_record(record, "hr.employee")
        assert result["name"] == "J*** S***"
        assert result["email"] == "j***@company.com"
        assert result["salary"] == 4200.0  # ceil(4200/100)*100
        assert result["phone"] == "***78"
        assert result["id"] == 1  # ID unchanged

    def test_account_record(self) -> None:
        record: dict[str, object] = {
            "id": 1,
            "name": "INV/2026/001",
            "amount_total": 15780.50,
            "partner_id": "Acme Corp",
        }
        result = anonymize_record(record, "account.move")
        assert result["name"] == "INV/2026/001"  # Not HR, name unchanged
        assert result["amount_total"] == 15800.0  # Rounded
        assert result["partner_id"] == "Acme Corp"  # No pattern match
