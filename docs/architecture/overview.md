# Architecture Overview

## System Components

### Agent Core (`apps/agent-core`)
- Agent implementations (ReAct, Conversational)
- Chain orchestration
- Tool system
- Memory management

### Agent Brain (`apps/agent-brain`)
- Task routing
- LLM routing
- Task scheduling
- Multi-agent orchestration

### Agent API (`apps/agent-api`)
- FastAPI REST API
- Endpoints for agents, tasks, crews

### Agent Worker (`apps/agent-worker`)
- Celery worker for async tasks
- Background job processing

## Technology Stack

- **Framework**: FastAPI
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL
- **Cache**: Redis
- **Vector Store**: Qdrant/Milvus/Weaviate
