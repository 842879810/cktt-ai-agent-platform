"""Tool type definitions."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ToolType(str, Enum):
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
    parameters: Dict[str, Any] = Field(default_factory=dict)
    returns: Dict[str, Any] = Field(default_factory=dict)
    is_async: bool = False


class ToolExecution(BaseModel):
    """Tool execution model."""

    tool_name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None
    duration: float = 0.0
