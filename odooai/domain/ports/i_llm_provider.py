"""
Module: domain/ports/i_llm_provider.py
Role: Abstract interface for LLM providers (Claude, OpenAI, Mistral, etc.).
Dependencies: none
"""

from abc import ABC, abstractmethod


class ILLMProvider(ABC):
    """Port for LLM API calls. Enables provider-agnostic architecture."""

    @abstractmethod
    async def complete(
        self,
        messages: list[dict[str, str]],
        model: str,
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> str:
        """
        Send a completion request to the LLM.

        Args:
            messages: List of {role, content} message dicts.
            model: Model identifier (e.g. 'claude-sonnet-4-20250514').
            system_prompt: Optional system prompt.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature (0.0 = deterministic).

        Returns:
            The LLM response text.
        """
