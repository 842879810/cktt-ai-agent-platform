# System Design

## Architecture Pattern

The platform follows a **monorepo** architecture with **modular** design:

```
apps/           # Core applications
packages/       # Shared libraries
skills/         # Plugin skills
services/       # External integrations
infrastructure/ # Deployment configs
```

## Data Flow

1. API receives request
2. Router determines agent/task
3. Brain orchestrates execution
4. Core runs agent with tools/memory
5. Result returned via API or async via Worker

## Scalability

- Horizontal scaling via multiple API instances
- Async task processing with Celery workers
- Vector storage for semantic search
- Redis for caching and message queue
