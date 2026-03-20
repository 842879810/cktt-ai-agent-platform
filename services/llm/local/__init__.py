"""Local LLM provider."""

from ..base import BaseLLM, LLMResponse, Message


class LocalLLM(BaseLLM):
    """Local LLM provider (e.g., Ollama, llama.cpp)."""

    def __init__(self, api_key: str = "", model: str = "llama2", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(api_key, model)
        self.base_url = base_url

    async def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        """Send a chat request to local LLM."""
        # Placeholder for actual local LLM API call
        return LLMResponse(
            content="Local LLM response",
            model=self.model,
            usage={"prompt_tokens": 0, "completion_tokens": 0}
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Send a completion request to local LLM."""
        # Placeholder for actual local LLM API call
        return LLMResponse(
            content="Local LLM completion",
            model=self.model,
            usage={"prompt_tokens": 0, "completion_tokens": 0}
        )
