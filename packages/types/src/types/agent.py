"""Agent type definitions."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class AgentType(str, Enum):
    """Agent types."""

    CONVERSATIONAL = "conversational"
    REACT = "react"
    PLANNING = "planning"
    TOOL_USE = "tool_use"


class AgentStatus(str, Enum):
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
    tools: List[str] = []


class Agent(BaseModel):
    """Agent model."""

    id: str
    name: str
    description: str = ""
    type: AgentType
    status: AgentStatus = AgentStatus.CREATED
    config: AgentConfig
    metadata: Dict[str, Any] = Field(default_factory=dict)
