"""Agent type definitions."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AgentType(StrEnum):
    """Agent types."""

    CONVERSATIONAL = "conversational"
    REACT = "react"
    PLANNING = "planning"
    TOOL_USE = "tool_use"


class AgentStatus(StrEnum):
    """Agent status."""

    CREATED = "created"
    RUNNING = "running"
    IDLE = "idle"
    ERROR = "error"


class AgentConfig(BaseModel):
    """Agent configuration."""

    name: str
    description: str = ""
    type: AgentType = AgentType.CONVERSATIONAL
    max_iterations: int = 10
    timeout: int = 300
    tools: list[str] = []


class Agent(BaseModel):
    """Agent model."""

    id: str
    name: str
    description: str = ""
    type: AgentType
    status: AgentStatus = AgentStatus.CREATED
    config: AgentConfig
    metadata: dict[str, Any] = Field(default_factory=dict)
