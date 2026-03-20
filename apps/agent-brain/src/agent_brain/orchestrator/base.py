"""Orchestrator base classes."""

from abc import ABC, abstractmethod
from typing import Any, List

from pydantic import BaseModel


class OrchestratorConfig(BaseModel):
    """Orchestrator configuration."""

    name: str
    max_agents: int = 10


class BaseOrchestrator(ABC):
    """Base class for all orchestrators."""

    def __init__(self, config: OrchestratorConfig):
        self.config = config

    @abstractmethod
    async def orchestrate(self, task: Any) -> Any:
        """Orchestrate a task across multiple agents."""
        pass
