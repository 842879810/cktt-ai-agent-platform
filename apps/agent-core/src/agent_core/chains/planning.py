"""Planning Chain."""

from typing import Any

from .base import BaseChain


class PlanningChain(BaseChain):
    """Chain for planning agent actions."""

    async def run(self, input_data: Any) -> Any:
        """Execute the planning chain."""
        result = input_data

        for step in self.steps:
            result = await step(result)

        return result
