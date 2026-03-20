"""Agent Coordinator - Coordinates multiple agents."""

from typing import Any

from pydantic import BaseModel


class CoordinationResult(BaseModel):
    """Result of coordination."""

    success: bool
    agent: str
    result: Any
    error: str | None = None


class AgentCoordinator:
    """Coordinator for managing agent interactions."""

    def __init__(self):
        self.agents: dict[str, Any] = {}
        self.execution_history: list[CoordinationResult] = []

    def register(self, name: str, agent: Any) -> None:
        """Register an agent."""
        self.agents[name] = agent

    def unregister(self, name: str) -> None:
        """Unregister an agent."""
        if name in self.agents:
            del self.agents[name]

    async def coordinate(self, task: Any, agent_name: str | None = None) -> CoordinationResult:
        """Coordinate task execution."""
        if agent_name:
            # Execute with specific agent
            if agent_name not in self.agents:
                return CoordinationResult(
                    success=False,
                    agent=agent_name,
                    result=None,
                    error=f"Agent {agent_name} not found"
                )

            agent = self.agents[agent_name]
            try:
                result = await agent.run(task)
                coord_result = CoordinationResult(success=True, agent=agent_name, result=result)
                self.execution_history.append(coord_result)
                return coord_result
            except Exception as e:
                coord_result = CoordinationResult(
                    success=False,
                    agent=agent_name,
                    result=None,
                    error=str(e)
                )
                self.execution_history.append(coord_result)
                return coord_result
        else:
            # Execute with first available agent
            if not self.agents:
                return CoordinationResult(
                    success=False,
                    agent="none",
                    result=None,
                    error="No agents available"
                )

            first_agent_name = next(iter(self.agents))
            return await self.coordinate(task, first_agent_name)

    def get_history(self) -> list[CoordinationResult]:
        """Get execution history."""
        return self.execution_history.copy()

    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
