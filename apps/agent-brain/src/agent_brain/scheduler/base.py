"""Scheduler base classes."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class Task(BaseModel):
    """Task model."""

    task_id: str
    name: str
    payload: dict
    status: str = "pending"
    priority: int = 0


class SchedulerConfig(BaseModel):
    """Scheduler configuration."""

    name: str
    max_concurrent: int = 10


class BaseScheduler(ABC):
    """Base class for all schedulers."""

    def __init__(self, config: SchedulerConfig):
        self.config = config
        self.tasks: list[Task] = []

    @abstractmethod
    async def schedule(self, task: Task) -> str:
        """Schedule a task."""
        pass

    @abstractmethod
    async def cancel(self, task_id: str) -> bool:
        """Cancel a task."""
        pass
