"""Tests for JWT authentication — signup, login, token validation."""

import pytest

from odooai.api.routers.auth import (
    _create_token,
    _hash_password,
    _verify_password,
    decode_token,
)


class TestPasswordHashing:
    """Test bcrypt password hashing."""

    def test_hash_and_verify(self) -> None:
        password = "testpassword123"
        hashed = _hash_password(password)
        assert _verify_password(password, hashed)

    def test_wrong_password_fails(self) -> None:
        hashed = _hash_password("correct")
        assert not _verify_password("wrong", hashed)

    def test_hash_is_different_each_time(self) -> None:
        h1 = _hash_password("same")
        h2 = _hash_password("same")
        assert h1 != h2  # bcrypt salt makes them different

    def test_hash_is_not_plaintext(self) -> None:
        hashed = _hash_password("mypassword")
        assert "mypassword" not in hashed


class TestJWTToken:
    """Test JWT token creation and validation."""

    def test_create_and_decode(self) -> None:
        token = _create_token("user-123", "test@example.com")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["email"] == "test@example.com"

    def test_invalid_token_raises(self) -> None:
        from fastapi import HTTPException

        with pytest.raises(HTTPException):
            decode_token("invalid.token.here")

    def test_token_contains_expiry(self) -> None:
        token = _create_token("user-123", "test@example.com")
        payload = decode_token(token)
        assert "exp" in payload
        assert "iat" in payload
