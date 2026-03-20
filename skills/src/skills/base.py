"""Skill base classes."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SkillConfig(BaseModel):
    """Skill configuration."""

    name: str
    description: str
    version: str = "1.0.0"
    parameters: Dict[str, Any] = Field(default_factory=dict)


class SkillResult(BaseModel):
    """Result from skill execution."""

    success: bool
    output: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseSkill(ABC):
    """Base class for all skills."""

    def __init__(self, config: SkillConfig):
        self.config = config

    @abstractmethod
    async def execute(self, **kwargs) -> SkillResult:
        """Execute the skill."""
        pass

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def description(self) -> str:
        return self.config.description
