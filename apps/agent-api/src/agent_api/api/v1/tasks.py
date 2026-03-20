"""Tasks API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class TaskCreateRequest(BaseModel):
    """Request to create a task."""

    name: str
    description: str = ""
    payload: dict = {}
    priority: int = 0


class TaskResponse(BaseModel):
    """Task response."""

    task_id: str
    name: str
    description: str
    status: str
    priority: int


@router.post("/", response_model=TaskResponse)
async def create_task(request: TaskCreateRequest):
    """Create a new task."""
    return TaskResponse(
        task_id=f"task_{hash(request.name)}",
        name=request.name,
        description=request.description,
        status="pending",
        priority=request.priority
    )


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(status: Optional[str] = None):
    """List all tasks."""
    return []


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a task by ID."""
    return TaskResponse(
        task_id=task_id,
        name="Sample Task",
        description="A sample task",
        status="completed",
        priority=0
    )


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    return {"message": f"Task {task_id} deleted"}
