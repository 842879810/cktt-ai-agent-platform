"""Task Scheduler Implementation."""

import asyncio

from .base import BaseScheduler, SchedulerConfig, Task


class TaskScheduler(BaseScheduler):
    """In-memory task scheduler."""

    def __init__(self, config: SchedulerConfig):
        super().__init__(config)
        self._running_tasks: dict = {}

    async def schedule(self, task: Task) -> str:
        """Schedule a task for execution."""
        self.tasks.append(task)
        task.status = "scheduled"

        # Run task asynchronously
        asyncio.create_task(self._execute_task(task))

        return task.task_id

    async def cancel(self, task_id: str) -> bool:
        """Cancel a task."""
        for task in self.tasks:
            if task.task_id == task_id and task.status in ["pending", "scheduled"]:
                task.status = "cancelled"
                return True
        return False

    async def _execute_task(self, task: Task) -> None:
        """Execute a task."""
        task.status = "running"
        self._running_tasks[task.task_id] = task

        try:
            # Simulate task execution
            await asyncio.sleep(0.1)
            task.status = "completed"
        except Exception:
            task.status = "failed"
        finally:
            if task.task_id in self._running_tasks:
                del self._running_tasks[task.task_id]

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def list_tasks(self, status: str | None = None) -> list[Task]:
        """List tasks, optionally filtered by status."""
        if status:
            return [t for t in self.tasks if t.status == status]
        return self.tasks.copy()
