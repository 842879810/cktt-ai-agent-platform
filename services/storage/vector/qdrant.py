"""Qdrant vector store."""

from typing import Any

from .base import VectorStore


class QdrantVectorStore(VectorStore):
    """Qdrant vector store implementation."""

    def __init__(self, host: str = "localhost", port: int = 6333, dimension: int = 768, collection: str = "default"):
        super().__init__(dimension)
        self.host = host
        self.port = port
        self.collection = collection

    async def add(self, id: str, vector: list[float], metadata: dict[str, Any]) -> None:
        """Add a vector to Qdrant."""
        pass

    async def search(self, query_vector: list[float], top_k: int = 5) -> list[tuple[str, float, dict[str, Any]]]:
        """Search in Qdrant."""
        return []

    async def delete(self, id: str) -> None:
        """Delete a vector from Qdrant."""
        pass

    async def get(self, id: str) -> tuple[list[float], dict[str, Any]]:
        """Get a vector from Qdrant."""
        return [], {}
