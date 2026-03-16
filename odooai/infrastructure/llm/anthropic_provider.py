"""
Module: infrastructure/llm/anthropic_provider.py
Role: Stub Anthropic Claude provider. Full implementation in agent framework spec.
Dependencies: domain/ports/i_llm_provider
"""

from odooai.domain.ports.i_llm_provider import ILLMProvider


class AnthropicProvider(ILLMProvider):
    """Stub LLM provider — raises NotImplementedError."""

    async def complete(
        self,
        messages: list[dict[str, str]],
        model: str,
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> str:
        raise NotImplementedError("AnthropicProvider: implement in agent spec")
