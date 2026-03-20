"""Planning system."""

from typing import Any, List

from pydantic import BaseModel


class PlanStep(BaseModel):
    """A single step in a plan."""

    step_id: str
    description: str
    action: str
    depends_on: List[str] = []


class Plan(BaseModel):
    """A plan consisting of multiple steps."""

    plan_id: str
    goal: str
    steps: List[PlanStep]
    status: str = "pending"


class Planner:
    """Planner for creating and executing plans."""

    async def create_plan(self, goal: str, context: dict) -> Plan:
        """Create a plan to achieve a goal."""
        plan_id = f"plan_{hash(goal)}"
        steps = [
            PlanStep(
                step_id=f"{plan_id}_1",
                description=f"Execute first step for: {goal}",
                action="execute_first_step"
            )
        ]
        return Plan(plan_id=plan_id, goal=goal, steps=steps)

    async def execute_plan(self, plan: Plan) -> Any:
        """Execute a plan."""
        results = []
        for step in plan.steps:
            results.append(f"Executed: {step.description}")
        return results
