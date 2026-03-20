"""LLM base classes."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class Message(BaseModel):
    """Chat message."""

    role: str
    content: str


class LLMResponse(BaseModel):
    """LLM response."""

    content: str
    model: str
    usage: dict[str, int] = {}


class BaseLLM(ABC):
    """Base class for all LLM providers."""

    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        """Send a chat request."""
        pass

    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Send a completion request."""
        pass
