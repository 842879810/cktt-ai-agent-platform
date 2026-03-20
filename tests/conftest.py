"""Pytest configuration."""

import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_agent_config():
    """Mock agent config for testing."""
    from agent_core.agents import AgentConfig

    return AgentConfig(
        name="test-agent",
        description="A test agent",
        max_iterations=5
    )


@pytest.fixture
def mock_task():
    """Mock task for testing."""
    from agent_brain.scheduler import Task

    return Task(
        task_id="test-task-1",
        name="Test Task",
        payload={"input": "test"}
    )
