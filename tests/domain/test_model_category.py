"""Tests for ModelCategory and ModelClassifier."""

from odooai.domain.value_objects.model_category import ModelCategory, ModelClassifier


class TestModelClassifier:
    """Test model classification into security categories."""

    def setup_method(self) -> None:
        ModelClassifier.clear_overrides()

    def test_blocked_models(self) -> None:
        """BLOCKED models must always return BLOCKED."""
        for model in (
            "ir.rule",
            "ir.model.access",
            "res.users",
            "res.groups",
            "ir.config_parameter",
            "ir.cron",
            "ir.mail_server",
        ):
            assert ModelClassifier.classify(model) == ModelCategory.BLOCKED

    def test_sensitive_exact(self) -> None:
        """Exact SENSITIVE models."""
        assert ModelClassifier.classify("account.move") == ModelCategory.SENSITIVE
        assert ModelClassifier.classify("hr.payslip") == ModelCategory.SENSITIVE

    def test_sensitive_prefix(self) -> None:
        """Models with sensitive prefixes."""
        assert ModelClassifier.classify("account.tax") == ModelCategory.SENSITIVE
        assert ModelClassifier.classify("hr.leave") == ModelCategory.SENSITIVE

    def test_open_models(self) -> None:
        """OPEN models (reference data)."""
        assert ModelClassifier.classify("product.product") == ModelCategory.OPEN
        assert ModelClassifier.classify("res.currency") == ModelCategory.OPEN

    def test_standard_default(self) -> None:
        """Unknown models default to STANDARD."""
        assert ModelClassifier.classify("sale.order") == ModelCategory.STANDARD
        assert ModelClassifier.classify("stock.picking") == ModelCategory.STANDARD

    def test_overrides_applied(self) -> None:
        """Overrides change classification for non-BLOCKED models."""
        ModelClassifier.load_overrides([("sale.order", ModelCategory.SENSITIVE)])
        assert ModelClassifier.classify("sale.order") == ModelCategory.SENSITIVE

    def test_overrides_cannot_unblock(self) -> None:
        """Overrides CANNOT change BLOCKED models."""
        ModelClassifier.load_overrides([("ir.rule", ModelCategory.OPEN)])
        assert ModelClassifier.classify("ir.rule") == ModelCategory.BLOCKED

    def test_clear_overrides(self) -> None:
        """Clearing overrides reverts to default classification."""
        ModelClassifier.load_overrides([("sale.order", ModelCategory.SENSITIVE)])
        ModelClassifier.clear_overrides()
        assert ModelClassifier.classify("sale.order") == ModelCategory.STANDARD


class TestModelCategoryEnum:
    """Test ModelCategory enum values."""

    def test_values(self) -> None:
        assert ModelCategory.BLOCKED == "blocked"
        assert ModelCategory.SENSITIVE == "sensitive"
        assert ModelCategory.STANDARD == "standard"
        assert ModelCategory.OPEN == "open"

    def test_is_str(self) -> None:
        assert isinstance(ModelCategory.BLOCKED, str)
