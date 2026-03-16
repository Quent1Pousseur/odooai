"""Tests for anonymizer functions."""

from odooai.security.anonymizer import (
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
