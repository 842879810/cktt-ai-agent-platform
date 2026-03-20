"""Vector store base classes."""

from abc import ABC, abstractmethod
from typing import Any


class VectorStore(ABC):
    """Base class for vector stores."""

    def __init__(self, dimension: int = 768):
        self.dimension = dimension

    @abstractmethod
    async def add(self, id: str, vector: list[float], metadata: dict[str, Any]) -> None:
        """Add a vector to the store."""
        pass

    @abstractmethod
    async def search(self, query_vector: list[float], top_k: int = 5) -> list[tuple[str, float, dict[str, Any]]]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete a vector from the store."""
        pass

    @abstractmethod
    async def get(self, id: str) -> tuple[list[float], dict[str, Any]]:
        """Get a vector by ID."""
        pass
