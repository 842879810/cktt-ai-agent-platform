"""Agents API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AgentCreateRequest(BaseModel):
    """Request to create an agent."""

    name: str
    description: str = ""
    type: str = "conversational"
    config: dict = {}


class AgentResponse(BaseModel):
    """Agent response."""

    id: str
    name: str
    description: str
    type: str
    status: str


class AgentRunRequest(BaseModel):
    """Request to run an agent."""

    input: str
    context: dict = {}


class AgentRunResponse(BaseModel):
    """Agent run response."""

    agent_id: str
    output: str
    status: str


@router.post("/", response_model=AgentResponse)
async def create_agent(request: AgentCreateRequest):
    """Create a new agent."""
    return AgentResponse(
        id=f"agent_{hash(request.name)}",
        name=request.name,
        description=request.description,
        type=request.type,
        status="created"
    )


@router.get("/", response_model=list[AgentResponse])
async def list_agents():
    """List all agents."""
    return []


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get an agent by ID."""
    return AgentResponse(
        id=agent_id,
        name="Sample Agent",
        description="A sample agent",
        type="conversational",
        status="active"
    )


@router.post("/{agent_id}/run", response_model=AgentRunResponse)
async def run_agent(agent_id: str, request: AgentRunRequest):
    """Run an agent with input."""
    return AgentRunResponse(
        agent_id=agent_id,
        output=f"Processed: {request.input}",
        status="completed"
    )


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent."""
    return {"message": f"Agent {agent_id} deleted"}
