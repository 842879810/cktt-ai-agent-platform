"""OpenAI LLM provider."""

from ..base import BaseLLM, LLMResponse, Message


class OpenAILLM(BaseLLM):
    """OpenAI LLM provider."""

    async def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        """Send a chat request to OpenAI."""
        # Placeholder for actual OpenAI API call
        return LLMResponse(
            content="OpenAI response",
            model=self.model,
            usage={"prompt_tokens": 0, "completion_tokens": 0}
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Send a completion request to OpenAI."""
        # Placeholder for actual OpenAI API call
        return LLMResponse(
            content="OpenAI completion",
            model=self.model,
            usage={"prompt_tokens": 0, "completion_tokens": 0}
        )
