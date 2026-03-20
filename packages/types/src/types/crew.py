"""Crew type definitions."""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from enum import Enum


class CrewStatus(str, Enum):
    """Crew status."""

    CREATED = "created"
    RUNNING = "running"
    IDLE = "idle"
    ERROR = "error"


class CrewStrategy(str, Enum):
    """Crew orchestration strategy."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"


class Crew(BaseModel):
    """Crew model."""

    crew_id: str
    name: str
    description: str = ""
    agent_ids: List[str] = []
    status: CrewStatus = CrewStatus.CREATED
    strategy: CrewStrategy = CrewStrategy.PARALLEL
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CrewResult(BaseModel):
    """Result from a crew execution."""

    crew_id: str
    results: List[Dict[str, Any]]
    status: str
    errors: List[str] = []
