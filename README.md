# CKTT AI Agent Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/FastAPI-0.109+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

> 企业级智能体平台，面向业务场景提供自主决策、任务编排与多模态交互能力，支持高可用、可扩展、安全可控的企业级 AI 应用落地。

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Start Services](#start-services)
- [Built-in Agents](#built-in-agents)
  - [General Agents](#general-agents)
  - [Domain-specific Agents V1](#domain-specific-agents-v1)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
  - [Tech Stack](#tech-stack)
  - [Sub-project Responsibilities](#sub-project-responsibilities)
- [Usage Examples](#usage-examples)
  - [Create Agent](#create-agent)
  - [Use IT Project Manager Agent](#use-it-project-manager-agent)
  - [Use Project R&D Agent](#use-project-rd-agent)
  - [API Requests](#api-requests)
- [Development Commands](#development-commands)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Multi-Agent Support**: Supports multiple built-in agent types including general and domain-specific agents
- **IT Project Manager Agent**: Automates IT project lifecycle document workflow
- **Project R&D Agent**: Automatically creates project directory structure and code templates
- **Tool System**: Extensible tool framework supporting Web Search, Code Executor, Data Analysis, etc.
- **Memory System**: Buffer memory + Vector memory with semantic search support
- **Task Scheduling**: Async task processing based on Celery + Redis
- **REST API**: High-performance FastAPI RESTful interface
- **Multi-LLM Support**: Multiple LLM providers including OpenAI, Anthropic, Local (Ollama)
- **Vector Storage**: Supports Qdrant, Milvus, Weaviate vector databases
- **Container Deployment**: Docker + Kubernetes support

---

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry (package manager)
- Docker & Docker Compose (optional)

### Installation

```bash
# Clone the project
git clone https://github.com/cktt/ai-agent-platform.git
cd ai-agent-platform

# Install dependencies
poetry install

# Configure environment variables
cp .env.example .env
# Edit .env with your settings
```

### Start Services

```bash
# Start Docker services (Redis + PostgreSQL)
docker-compose up -d

# Start API service
poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload
```

Visit http://localhost:8000 for API documentation.

### Initialize Database

```bash
# Execute database schema
psql -d agent_platform -f scripts/database/schema.sql
```

### Chinese Documentation

For Chinese users, see [USAGE.md](./USAGE.md) for detailed usage instructions.

---

## Built-in Agents

The platform provides multiple built-in agents to meet different scenario requirements:

### General Agents

| Agent Type | Description | Use Case |
|------------|-------------|----------|
| ConversationalAgent | Conversational agent | Daily chat, Q&A |
| ReactAgent | ReAct reasoning agent | Complex reasoning, tool calling |

### Domain-specific Agents V1

| Agent Type | Description | Workflow |
|------------|-------------|----------|
| ITProjectManagerAgent | IT project file management | PRD Creation -> PRD Review -> HLD -> LLD -> Task Assignment |
| ProjectRDAgent | Project R&D process | Project Init -> Directory Creation -> Config Setup -> Template Generation |

#### ITProjectManagerAgent

Automates IT project lifecycle document management with the following main stages:

1. **PRD Creation** - Generate Product Requirements Document including project overview, user requirements, functional requirements, non-functional requirements, acceptance criteria
2. **PRD Review** - Requirements review process, record review comments, final decision approve/reject
3. **HLD (High-Level Design)** - System architecture design, module design, database design, interface design, security design
4. **LLD (Low-Level Design)** - Module detailed design, database detailed design, interface detailed design, algorithm design
5. **Task Assignment** - Automatically generate development task list based on design documents

#### ProjectRDAgent

Automatically creates project R&D directory structure (without actual development code). Created directories:

```
project-name/
├── src/
│   └── project_name/
│       ├── modules/
│       ├── utils/
│       └── models/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
│   ├── api/
│   ├── guide/
│   └── dev/
├── config/
│   ├── dev/
│   └── prod/
├── scripts/
│   ├── dev/
│   └── deploy/
├── logs/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── .github/
│   └── workflows/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
└── config/*.yaml
```

---

## Project Structure

```
cktt-ai-agent-platform/                    # 项目根目录
├── apps/                                   # 应用子项目 (核心业务)
│   ├── agent-core/                        # 单体智能体引擎
│   │   ├── src/agent_core/
│   │   │   ├── agents/                   # Agent 实现 (含IT项目管理、项目研发Agent)
│   │   │   ├── chains/                  # Chain 编排
│   │   │   ├── tools/                    # 工具系统
│   │   │   ├── memory/                   # 记忆系统
│   │   │   └── planning/                 # 规划系统
│   │   └── tests/
│   │
│   ├── agent-brain/                       # 中枢大脑 (调度/路由/控制)
│   │   ├── src/agent_brain/
│   │   │   ├── router/                   # 路由层 (LLM路由/任务路由)
│   │   │   ├── scheduler/                # 调度器
│   │   │   ├── orchestrator/            # 编排器 (多Agent编排)
│   │   │   └── coordinator/              # 协调器
│   │   └── tests/
│   │
│   ├── agent-api/                         # API 服务
│   │   ├── src/agent_api/
│   │   │   ├── main.py                   # FastAPI 入口
│   │   │   ├── api/v1/                   # API 端点
│   │   │   ├── schemas/                 # Pydantic 模型
│   │   │   └── middleware/               # 中间件
│   │   └── tests/
│   │
│   └── agent-worker/                      # 后台任务 Worker
│       ├── src/agent_worker/
│       │   ├── worker.py                 # Celery Worker
│       │   └── tasks/                    # 任务定义
│       └── tests/
│
├── packages/                              # 共享包 (内部库)
│   ├── common/                            # 通用工具库
│   │   └── src/common/
│   │       ├── logging/                 # 日志工具
│   │       ├── metrics/                 # 指标收集
│   │       ├── exceptions/              # 异常定义
│   │       └── utils/                  # 通用工具
│   │
│   ├── types/                            # 类型定义
│   │   └── src/types/
│   │       ├── agent.py                  # Agent 类型
│   │       ├── task.py                   # Task 类型
│   │       ├── crew.py                   # Crew 类型
│   │       ├── tool.py                   # Tool 类型
│   │       └── message.py                # Message 类型
│   │
│   └── config/                           # 配置管理
│       └── src/config/
│           ├── loader.py                  # 配置加载器
│           ├── schema.py                  # 配置模式
│           └── settings.py                # 设置管理
│
├── skills/                               # Skill 技能系统 (插件化)
│   ├── src/skills/
│   │   ├── base.py                      # Skill 基类
│   │   ├── registry.py                  # 技能注册表
│   │   └── loader.py                    # 动态加载器
│   │
│   └── implementations/                  # 技能实现
│       ├── web_search.py                # Web 搜索
│       ├── code_executor.py              # 代码执行
│       ├── data_analysis.py              # 数据分析
│       └── document_processor.py          # 文档处理
│
├── services/                             # 外部服务集成
│   ├── llm/                              # LLM 提供商
│   │   ├── openai/                       # OpenAI
│   │   ├── anthropic/                    # Anthropic
│   │   └── local/                        # 本地 LLM
│   │
│   └── storage/                         # 存储服务
│       ├── vector/                       # 向量数据库
│       │   ├── qdrant.py
│       │   ├── milvus.py
│       │   └── weaviate.py
│       ├── memory/                       # 记忆存储
│       │   ├── redis_memory.py
│       │   └── postgres_memory.py
│       └── document/                     # 文档存储
│           └── s3_storage.py
│
├── infrastructure/                       # 基础设施配置
│   ├── docker/                          # Docker 配置
│   ├── kubernetes/                       # K8s 配置
│   ├── terraform/                       # IaC 配置
│   └── monitoring/                       # 监控配置
│
├── tests/                                # 跨项目测试
│   ├── conftest.py                      # pytest 全局配置
│   ├── fixtures/                        # 测试数据
│   ├── integration/                    # 集成测试
│   ├── e2e/                            # 端到端测试
│   └── performance/                    # 性能测试
│
├── docs/                                 # 官方文档
│   ├── getting-started/                 # 入门指南
│   ├── architecture/                    # 架构文档
│   ├── api/                            # API 参考
│   └── guides/                          # 开发指南
│
├── scripts/                             # 工具脚本
│   ├── dev/                            # 开发脚本
│   ├── deploy/                          # 部署脚本
│   └── maintenance/                     # 维护脚本
│
├── config/                              # 配置文件
│   ├── base.yaml                        # 基础配置
│   ├── development.yaml                  # 开发环境
│   ├── staging.yaml                     # 预发布环境
│   └── production.yaml                   # 生产环境
│
├── pyproject.toml                      # Poetry 根配置
├── docker-compose.yml                   # Docker Compose
├── Makefile                             # 构建命令
├── pytest.ini                           # pytest 配置
├── mypy.ini                           # 类型检查配置
└── ruff.toml                           # 代码规范
```

---

## Architecture

### Tech Stack

| Category | Technology |
|----------|------------|
| Web Framework | FastAPI |
| Task Queue | Celery + Redis |
| Database | PostgreSQL |
| Cache | Redis |
| Vector Store | Qdrant / Milvus / Weaviate |
| Testing | pytest + pytest-asyncio |
| Documentation | MkDocs + Material |

### Sub-project Responsibilities

| Sub-project | Responsibility | Independent Deployment |
|-------------|----------------|----------------------|
| agent-core | Single agent engine (including IT Project Manager, Project R&D Agent) | Yes |
| agent-brain | Task scheduling, routing, multi-agent orchestration | Yes |
| agent-api | RESTful API service | Yes |
| agent-worker | Async task processing | Yes |
| skills | Plugin-based skill system | Runtime loading |

---

## Usage Examples

### Create Agent

```python
from agent_core.agents import ConversationalAgent, AgentConfig

# Create agent config
config = AgentConfig(
    name="my-agent",
    description="A helpful assistant",
    max_iterations=10
)

# Create agent
agent = ConversationalAgent(config)

# Run agent
result = await agent.run("Hello, world!")
print(result)
```

### Use IT Project Manager Agent

```python
from agent_core.agents import ITProjectManagerAgent, AgentConfig

# Create agent config
config = AgentConfig(
    name="it-project-manager",
    description="IT project document management agent",
    max_iterations=10
)

# Create agent
agent = ITProjectManagerAgent(config, project_name="ERP System")

# Run agent
result = await agent.run({
    "project_name": "ERP System",
    "project_info": {
        "background": "Enterprise resource planning requirements",
        "goals": "Achieve unified enterprise resource management",
        "scope": "Procurement, sales, inventory, finance modules",
        "user_roles": ["Admin", "Purchaser", "Salesperson", "Warehouse", "Finance"],
        "core_features": ["User Management", "Permission Management", "Procurement", "Sales", "Inventory", "Finance"],
        "performance": "Response time <2s, support 1000+ concurrent",
    }
})

print(result["current_phase"])  # Current phase
print(result["documents"])       # Generated documents
print(result["tasks"])          # Assigned tasks
```

### Use Project R&D Agent

```python
from agent_core.agents import ProjectRDAgent, AgentConfig

# Create agent config
config = AgentConfig(
    name="project-rd",
    description="Project R&D directory creation agent",
    max_iterations=5
)

# Create agent
agent = ProjectRDAgent(config, project_name="MyProject", base_path="./projects")

# Run agent
result = await agent.run({
    "project_name": "MyProject",
    "base_path": "./projects"
})

print(result["created_directories"])  # Created directory list
print(result["created_files"])        # Created file list
```

### API Requests

```bash
# Create agent
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-agent",
    "type": "conversational",
    "description": "Test agent"
  }'

# Run agent
curl -X POST http://localhost:8000/api/v1/agents/agent_xxx/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hello"
  }'
```

---

## Development Commands

```bash
# Install dependencies
make install

# Run development server
make dev

# Run tests
make test

# Lint code
make lint

# Format code
make format

# Build Docker images
make docker-build

# Start Docker services
make docker-up

# Stop Docker services
make docker-down
```

---

## Contributing

Contributions are welcome! Please read the [Contributing Guide](docs/contributing/) for details.

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Contact

- Website: https://cktt.ai
- Email: team@cktt.ai
