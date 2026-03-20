"""Crew Orchestrator - Multi-agent orchestration."""

import asyncio
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseOrchestrator, OrchestratorConfig


class AgentInfo(BaseModel):
    """Information about an agent in the crew."""

    name: str
    role: str
    capabilities: List[str]


class CrewOrchestrator(BaseOrchestrator):
    """Orchestrator for managing multiple agents (crew)."""

    def __init__(self, config: OrchestratorConfig):
        super().__init__(config)
        self.agents: Dict[str, Any] = {}

    def register_agent(self, name: str, agent: Any) -> None:
        """Register an agent with the orchestrator."""
        self.agents[name] = agent

    def unregister_agent(self, name: str) -> None:
        """Unregister an agent."""
        if name in self.agents:
            del self.agents[name]

    async def orchestrate(self, task: Any) -> Any:
        """Orchestrate a task across multiple agents."""
        results = []

        # Execute task with all registered agents in parallel
        tasks = []
        for name, agent in self.agents.items():
            tasks.append(self._execute_with_agent(agent, task))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            "task": task,
            "results": results,
            "agents_used": list(self.agents.keys())
        }

    async def _execute_with_agent(self, agent: Any, task: Any) -> Any:
        """Execute a task with a specific agent."""
        try:
            if hasattr(agent, "run"):
                return await agent.run(task)
            return f"Agent executed: {task}"
        except Exception as e:
            return {"error": str(e)}

    def list_agents(self) -> List[str]:
        """List all registered agents."""
        return list(self.agents.keys())
