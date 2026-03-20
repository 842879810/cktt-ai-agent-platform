"""Message type definitions."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message roles."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class Message(BaseModel):
    """Message model."""

    role: MessageRole
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class Conversation(BaseModel):
    """Conversation model."""

    conversation_id: str
    messages: List[Message] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_message(self, role: MessageRole, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a message to the conversation."""
        self.messages.append(Message(role=role, content=content, metadata=metadata or {}))

    def get_messages(self) -> List[Message]:
        """Get all messages."""
        return self.messages.copy()
