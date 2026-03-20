"""Crew type definitions."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CrewStatus(StrEnum):
    """Crew status."""

    CREATED = "created"
    RUNNING = "running"
    IDLE = "idle"
    ERROR = "error"


class CrewStrategy(StrEnum):
    """Crew orchestration strategy."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"


class Crew(BaseModel):
    """Crew model."""

    crew_id: str
    name: str
    description: str = ""
    agent_ids: list[str] = []
    status: CrewStatus = CrewStatus.CREATED
    strategy: CrewStrategy = CrewStrategy.PARALLEL
    metadata: dict[str, Any] = Field(default_factory=dict)


class CrewResult(BaseModel):
    """Result from a crew execution."""

    crew_id: str
    results: list[dict[str, Any]]
    status: str
    errors: list[str] = []
