"""Tool type definitions."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ToolType(StrEnum):
    """Tool types."""

    FUNCTION = "function"
    API = "api"
    SEARCH = "search"
    CODE_EXECUTION = "code_execution"
    DOCUMENT = "document"


class Tool(BaseModel):
    """Tool model."""

    name: str
    description: str
    type: ToolType = ToolType.FUNCTION
    parameters: dict[str, Any] = Field(default_factory=dict)
    returns: dict[str, Any] = Field(default_factory=dict)
    is_async: bool = False


class ToolExecution(BaseModel):
    """Tool execution model."""

    tool_name: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    result: Any | None = None
    error: str | None = None
    duration: float = 0.0
