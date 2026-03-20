"""Message type definitions."""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
    """Message roles."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class Message(BaseModel):
    """Message model."""

    role: MessageRole
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class Conversation(BaseModel):
    """Conversation model."""

    conversation_id: str
    messages: list[Message] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def add_message(self, role: MessageRole, content: str, metadata: dict[str, Any] | None = None) -> None:
        """Add a message to the conversation."""
        self.messages.append(Message(role=role, content=content, metadata=metadata or {}))

    def get_messages(self) -> list[Message]:
        """Get all messages."""
        return self.messages.copy()
