"""S3 document storage."""

from typing import BinaryIO


class S3Storage:
    """S3-compatible document storage."""

    def __init__(self, bucket: str = "agent-platform", endpoint: str | None = None, access_key: str = "", secret_key: str = "", region: str = "us-east-1"):
        self.bucket = bucket
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    async def upload(self, key: str, data: BinaryIO, content_type: str = "application/octet-stream") -> None:
        """Upload a document to S3."""
        pass

    async def download(self, key: str) -> bytes | None:
        """Download a document from S3."""
        return None

    async def delete(self, key: str) -> None:
        """Delete a document from S3."""
        pass

    async def exists(self, key: str) -> bool:
        """Check if a document exists."""
        return False

    async def list(self, prefix: str = "") -> list:
        """List documents with a prefix."""
        return []
