"""Vector store base classes."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class VectorStore(ABC):
    """Base class for vector stores."""

    def __init__(self, dimension: int = 768):
        self.dimension = dimension

    @abstractmethod
    async def add(self, id: str, vector: List[float], metadata: Dict[str, Any]) -> None:
        """Add a vector to the store."""
        pass

    @abstractmethod
    async def search(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete a vector from the store."""
        pass

    @abstractmethod
    async def get(self, id: str) -> Tuple[List[float], Dict[str, Any]]:
        """Get a vector by ID."""
        pass
