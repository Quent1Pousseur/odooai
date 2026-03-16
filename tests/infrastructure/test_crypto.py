"""Tests for AES-256-GCM encryption."""

import base64
import os

import cryptography.exceptions
import pytest

from odooai.infrastructure.crypto import AESCrypto


def _make_key() -> str:
    """Generate a random base64-encoded 32-byte key."""
    return base64.b64encode(os.urandom(32)).decode()


class TestAESCrypto:
    """Test encryption round-trip and key rotation."""

    def test_encrypt_decrypt_roundtrip(self) -> None:
        key = _make_key()
        crypto = AESCrypto(key_b64=key)
        plaintext = "my-secret-api-key-12345"
        ciphertext = crypto.encrypt(plaintext)
        assert ciphertext.startswith("v1:")
        assert crypto.decrypt(ciphertext) == plaintext

    def test_different_ciphertext_each_time(self) -> None:
        key = _make_key()
        crypto = AESCrypto(key_b64=key)
        c1 = crypto.encrypt("same")
        c2 = crypto.encrypt("same")
        assert c1 != c2  # Non-deterministic (random nonce)

    def test_key_rotation(self) -> None:
        old_key = _make_key()
        new_key = _make_key()
        old_crypto = AESCrypto(key_b64=old_key)
        ciphertext = old_crypto.encrypt("secret")

        # New crypto with previous key can still decrypt
        new_crypto = AESCrypto(key_b64=new_key, previous_key_b64=old_key)
        assert new_crypto.decrypt(ciphertext) == "secret"

    def test_wrong_key_fails(self) -> None:
        key1 = _make_key()
        key2 = _make_key()
        crypto1 = AESCrypto(key_b64=key1)
        crypto2 = AESCrypto(key_b64=key2)
        ciphertext = crypto1.encrypt("secret")
        with pytest.raises(
            (ValueError, cryptography.exceptions.InvalidTag),
        ):
            crypto2.decrypt(ciphertext)

    def test_invalid_key_length(self) -> None:
        short_key = base64.b64encode(b"short").decode()
        with pytest.raises(ValueError, match="32 bytes"):
            AESCrypto(key_b64=short_key)
