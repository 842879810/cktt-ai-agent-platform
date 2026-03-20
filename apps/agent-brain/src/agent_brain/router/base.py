"""Router base classes."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RouteConfig(BaseModel):
    """Route configuration."""

    name: str
    description: str = ""


class BaseRouter(ABC):
    """Base class for all routers."""

    def __init__(self, config: RouteConfig):
        self.config = config

    @abstractmethod
    async def route(self, input_data: Any) -> Any:
        """Route the input data."""
        pass
