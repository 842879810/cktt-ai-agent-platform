"""Common exceptions."""


class AgentPlatformError(Exception):
    """Base exception for agent platform."""

    pass


class AgentError(AgentPlatformError):
    """Agent-related errors."""

    pass


class ToolError(AgentPlatformError):
    """Tool-related errors."""

    pass


class MemoryError(AgentPlatformError):
    """Memory-related errors."""

    pass


class RouterError(AgentPlatformError):
    """Router-related errors."""

    pass


class SchedulerError(AgentPlatformError):
    """Scheduler-related errors."""

    pass


class OrchestratorError(AgentPlatformError):
    """Orchestrator-related errors."""

    pass


class ConfigurationError(AgentPlatformError):
    """Configuration-related errors."""

    pass
