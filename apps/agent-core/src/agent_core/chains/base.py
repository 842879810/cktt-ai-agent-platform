"""Chain base classes."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pydantic import BaseModel


class ChainConfig(BaseModel):
    """Chain configuration."""

    name: str
    description: str = ""


class BaseChain(ABC):
    """Base class for all chains."""

    def __init__(self, config: ChainConfig):
        self.config = config
        self.steps: List[Any] = []

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """Run the chain."""
        pass

    def add_step(self, step: Any) -> None:
        """Add a step to the chain."""
        self.steps.append(step)

    def clear_steps(self) -> None:
        """Clear all steps."""
        self.steps.clear()
