"""
Module: infrastructure/crypto.py
Role: AES-256-GCM symmetric encryption for Odoo API keys at rest.

Encryption format (versioned):
    v1:<base64(nonce(12) || ciphertext || tag(16))>

Security properties:
    - AES-256-GCM: authenticated encryption (confidentiality + integrity)
    - 96-bit random nonce per encryption (os.urandom — CSPRNG)
    - 128-bit authentication tag (tamper-evident)
    - Non-deterministic: same plaintext produces different ciphertext each time

Dependencies: cryptography, domain/ports/i_crypto
"""

import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from odooai.domain.ports.i_crypto import ICrypto

_NONCE_SIZE = 12  # 96-bit nonce — NIST recommended for AES-GCM
_VERSION_PREFIX = "v1:"


def _decode_key(key_b64: str) -> bytes:
    """Decode a base64-encoded AES-256 key and validate its length."""
    key = base64.b64decode(key_b64)
    if len(key) != 32:
        msg = f"Encryption key must decode to exactly 32 bytes, got {len(key)}"
        raise ValueError(msg)
    return key


class AESCrypto(ICrypto):
    """AES-256-GCM encryption with key rotation support."""

    def __init__(self, key_b64: str, previous_key_b64: str = "") -> None:
        self._key = _decode_key(key_b64)
        self._previous_key: bytes | None = None
        if previous_key_b64:
            try:
                self._previous_key = _decode_key(previous_key_b64)
            except (ValueError, Exception):
                self._previous_key = None

    def encrypt(self, plaintext: str) -> str:
        """Encrypt with the current key. Returns 'v1:<base64>'."""
        aesgcm = AESGCM(self._key)
        nonce = os.urandom(_NONCE_SIZE)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        encoded = base64.b64encode(nonce + ciphertext).decode("utf-8")
        return f"{_VERSION_PREFIX}{encoded}"

    def decrypt(self, ciphertext_b64: str) -> str:
        """Decrypt, trying current key first, then previous key for rotation."""
        if ciphertext_b64.startswith(_VERSION_PREFIX):
            raw_b64 = ciphertext_b64[len(_VERSION_PREFIX) :]
        else:
            raw_b64 = ciphertext_b64

        data = base64.b64decode(raw_b64)
        nonce = data[:_NONCE_SIZE]
        ciphertext = data[_NONCE_SIZE:]

        # Try current key
        try:
            aesgcm = AESGCM(self._key)
            return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")
        except Exception:
            pass

        # Fall back to previous key (rotation support)
        if self._previous_key:
            aesgcm = AESGCM(self._previous_key)
            return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")

        # Neither key works — re-raise with current key
        aesgcm = AESGCM(self._key)
        return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")
