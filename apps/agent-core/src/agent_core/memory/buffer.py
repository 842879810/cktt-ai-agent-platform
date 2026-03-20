"""Buffer memory for storing conversation history."""


from pydantic import BaseModel


class MemoryItem(BaseModel):
    """Memory item."""

    role: str
    content: str
    metadata: dict = {}


class BufferMemory:
    """Simple buffer memory for storing messages."""

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.messages: list[MemoryItem] = []

    def add(self, role: str, content: str, metadata: dict | None = None) -> None:
        """Add a message to memory."""
        item = MemoryItem(role=role, content=content, metadata=metadata or {})
        self.messages.append(item)

        # Trim if exceeds max size
        if len(self.messages) > self.max_size:
            self.messages = self.messages[-self.max_size:]

    def get_messages(self) -> list[MemoryItem]:
        """Get all messages."""
        return self.messages.copy()

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()

    def __len__(self) -> int:
        return len(self.messages)
