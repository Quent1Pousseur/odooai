"""
Module: domain/ports/i_crypto.py
Role: Abstract interface for symmetric encryption of secrets at rest.
Dependencies: none
"""

from abc import ABC, abstractmethod


class ICrypto(ABC):
    """Port for encrypting/decrypting sensitive data (Odoo API keys)."""

    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        """Encrypt a plaintext string. Returns an opaque ciphertext string."""

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt a ciphertext string. Returns the original plaintext."""
