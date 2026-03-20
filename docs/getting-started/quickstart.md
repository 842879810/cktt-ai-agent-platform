# Quickstart

## Create Your First Agent

```python
from agent_core.agents import ConversationalAgent, AgentConfig

# Create agent config
config = AgentConfig(
    name="my-agent",
    description="A helpful assistant"
)

# Create agent
agent = ConversationalAgent(config)

# Run agent
result = await agent.run("Hello, world!")
print(result)
```

## Run the API

```bash
poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload
```

## Make API Request

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "test-agent", "type": "conversational"}'
```
