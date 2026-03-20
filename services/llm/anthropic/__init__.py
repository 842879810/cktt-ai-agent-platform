"""Anthropic LLM provider."""

from typing import Any, Dict, List

from ..base import BaseLLM, LLMResponse, Message


class AnthropicLLM(BaseLLM):
    """Anthropic Claude LLM provider."""

    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229", **kwargs):
        super().__init__(api_key, model)

    async def chat(self, messages: List[Message], **kwargs) -> LLMResponse:
        """Send a chat request to Anthropic."""
        # Placeholder for actual Anthropic API call
        return LLMResponse(
            content="Anthropic response",
            model=self.model,
            usage={"input_tokens": 0, "output_tokens": 0}
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Send a completion request to Anthropic."""
        # Placeholder for actual Anthropic API call
        return LLMResponse(
            content="Anthropic completion",
            model=self.model,
            usage={"input_tokens": 0, "output_tokens": 0}
        )
