"""Crews API endpoints."""

from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CrewCreateRequest(BaseModel):
    """Request to create a crew."""

    name: str
    description: str = ""
    agent_ids: List[str] = []


class CrewResponse(BaseModel):
    """Crew response."""

    crew_id: str
    name: str
    description: str
    agent_ids: List[str]
    status: str


class CrewRunRequest(BaseModel):
    """Request to run a crew."""

    input: str
    strategy: str = "parallel"


class CrewRunResponse(BaseModel):
    """Crew run response."""

    crew_id: str
    results: List[dict]
    status: str


@router.post("/", response_model=CrewResponse)
async def create_crew(request: CrewCreateRequest):
    """Create a new crew."""
    return CrewResponse(
        crew_id=f"crew_{hash(request.name)}",
        name=request.name,
        description=request.description,
        agent_ids=request.agent_ids,
        status="created"
    )


@router.get("/", response_model=List[CrewResponse])
async def list_crews():
    """List all crews."""
    return []


@router.get("/{crew_id}", response_model=CrewResponse)
async def get_crew(crew_id: str):
    """Get a crew by ID."""
    return CrewResponse(
        crew_id=crew_id,
        name="Sample Crew",
        description="A sample crew",
        agent_ids=[],
        status="active"
    )


@router.post("/{crew_id}/run", response_model=CrewRunResponse)
async def run_crew(crew_id: str, request: CrewRunRequest):
    """Run a crew with input."""
    return CrewRunResponse(
        crew_id=crew_id,
        results=[],
        status="completed"
    )


@router.delete("/{crew_id}")
async def delete_crew(crew_id: str):
    """Delete a crew."""
    return {"message": f"Crew {crew_id} deleted"}
