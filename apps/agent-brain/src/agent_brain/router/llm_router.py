"""LLM Router - Routes requests to appropriate LLM providers."""

from typing import Any

from .base import BaseRouter, RouteConfig


class LLMRouter(BaseRouter):
    """Router for selecting appropriate LLM provider."""

    def __init__(self, config: RouteConfig, providers: dict[str, Any] | None = None):
        super().__init__(config)
        self.providers = providers or {}

    async def route(self, input_data: Any) -> Any:
        """Route to the appropriate LLM provider."""
        # Simple routing based on model name
        model = input_data.get("model", "gpt-4")

        if "claude" in model.lower():
            return {"provider": "anthropic", "model": model}
        elif "gpt" in model.lower() or "openai" in model.lower():
            return {"provider": "openai", "model": model}
        else:
            return {"provider": "local", "model": model}

    def register_provider(self, name: str, config: dict[str, Any]) -> None:
        """Register a new LLM provider."""
        self.providers[name] = config

    def list_providers(self) -> list[str]:
        """List all registered providers."""
        return list(self.providers.keys())
