"""Tests for edge cases — questions hors-sujet, inputs malformes, limites."""

from odooai.agents.orchestrator import detect_domain


class TestEdgeCasesDomainDetection:
    """Test that weird inputs don't crash the domain detector."""

    def test_empty_question(self) -> None:
        assert detect_domain("") is None

    def test_single_char(self) -> None:
        assert detect_domain("?") is None

    def test_numbers_only(self) -> None:
        assert detect_domain("12345") is None

    def test_weather_question(self) -> None:
        """Hors-sujet : meteo."""
        assert detect_domain("Quelle est la meteo aujourd'hui ?") is None

    def test_greeting(self) -> None:
        """Hors-sujet : salutation."""
        assert detect_domain("Bonjour, comment allez-vous ?") is None

    def test_insult(self) -> None:
        """Hors-sujet : input hostile."""
        assert detect_domain("Tu es nul, casse-toi") is None

    def test_sql_injection_attempt(self) -> None:
        """Input malicieux dans la question."""
        result = detect_domain("'; DROP TABLE users; --")
        # Should not crash, may return None or a domain
        assert result is None or isinstance(result, str)

    def test_very_long_question(self) -> None:
        """Question extremement longue."""
        long_q = "stock " * 10000
        result = detect_domain(long_q)
        assert result == "supply_chain"

    def test_unicode_question(self) -> None:
        """Question avec caracteres speciaux."""
        assert detect_domain("Comment gerer mes ventes en €?") is not None

    def test_mixed_domains(self) -> None:
        """Question multi-domaine."""
        result = detect_domain("Je veux voir mes factures de vente et mon stock")
        assert result is not None

    def test_english_question(self) -> None:
        """Question en anglais — keywords sont en francais."""
        result = detect_domain("How to manage my sales orders?")
        # "sale" is a keyword
        assert result == "sales_crm"

    def test_none_resilience(self) -> None:
        """Verify that None domain is handled gracefully."""
        result = detect_domain("xyz abc def")
        assert result is None
