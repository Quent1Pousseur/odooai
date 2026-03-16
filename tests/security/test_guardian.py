"""Tests for Security Guardian."""

import pytest

from odooai.domain.value_objects.model_category import ModelCategory, ModelClassifier
from odooai.exceptions import BlockedModelError
from odooai.security.guardian import guard_model_access


class TestGuardModelAccess:
    """Test the security gate for model access."""

    def setup_method(self) -> None:
        ModelClassifier.clear_overrides()

    def test_blocked_raises(self) -> None:
        with pytest.raises(BlockedModelError) as exc_info:
            guard_model_access("ir.rule")
        assert "permanently blocked" in exc_info.value.user_message

    def test_standard_passes(self) -> None:
        category = guard_model_access("sale.order")
        assert category == ModelCategory.STANDARD

    def test_open_passes(self) -> None:
        category = guard_model_access("product.product")
        assert category == ModelCategory.OPEN

    def test_sensitive_passes(self) -> None:
        category = guard_model_access("account.move")
        assert category == ModelCategory.SENSITIVE

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
