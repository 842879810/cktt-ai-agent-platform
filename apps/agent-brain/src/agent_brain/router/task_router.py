"""Task Router - Routes tasks to appropriate agents."""

from typing import Any, Dict, List, Optional

from .base import BaseRouter, RouteConfig


class TaskRouter(BaseRouter):
    """Router for routing tasks to appropriate agents."""

    def __init__(self, config: RouteConfig, routes: Optional[Dict[str, str]] = None):
        super().__init__(config)
        self.routes = routes or {
            "conversation": "conversational_agent",
            "reasoning": "react_agent",
            "analysis": "analysis_agent",
        }

    async def route(self, input_data: Any) -> Any:
        """Route the task to the appropriate agent."""
        task_type = input_data.get("task_type", "conversation")

        agent = self.routes.get(task_type, "default_agent")

        return {
            "task_type": task_type,
            "agent": agent,
            "route": f"routed to {agent}"
        }

    def add_route(self, task_type: str, agent: str) -> None:
        """Add a new route."""
        self.routes[task_type] = agent

    def remove_route(self, task_type: str) -> None:
        """Remove a route."""
        if task_type in self.routes:
            del self.routes[task_type]
