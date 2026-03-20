# CKTT AI Agent Platform 使用说明书

> 企业级智能体平台，面向业务场景提供自主决策、任务编排与多模态交互能力。

## 目录

- [环境准备](#环境准备)
- [快速启动](#快速启动)
- [配置说明](#配置说明)
- [内置智能体](#内置智能体)
- [API 使用指南](#api-使用指南)
- [Python SDK 使用](#python-sdk-使用)
- [技能系统](#技能系统)
- [Docker 部署](#docker-部署)

---

## 环境准备

### 前置要求

| 依赖 | 版本要求 |
|------|---------|
| Python | 3.11+ |
| Poetry | 最新版 |
| Docker & Docker Compose | 可选 |

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/cktt/ai-agent-platform.git
cd cktt-ai-agent-platform

# 2. 安装依赖
poetry install

# 3. 复制环境配置文件
cp .env.example .env
```

---

## 快速启动

### 方式一：Docker 启动（推荐）

```bash
# 启动所有服务（Redis + PostgreSQL + API + Worker）
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 方式二：本地开发启动

```bash
# 1. 启动依赖服务（Redis + PostgreSQL）
docker-compose up -d redis postgres

# 2. 启动 API 服务
poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后，访问 http://localhost:8000 查看 API 文档（Swagger UI）。

---

## 配置说明

编辑 `.env` 文件：

```bash
# 应用配置
DEBUG=false
ENVIRONMENT=development

# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=agent_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# LLM 配置
LLM_PROVIDER=openai        # 可选: openai, anthropic, local
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4           # 如: gpt-4, gpt-3.5-turbo, claude-3
```

### 支持的 LLM 提供商

| 提供商 | 环境变量 LLM_PROVIDER | 模型示例 |
|--------|----------------------|---------|
| OpenAI | `openai` | gpt-4, gpt-3.5-turbo |
| Anthropic | `anthropic` | claude-3-opus, claude-3-sonnet |
| 本地 (Ollama) | `local` | llama2, mistral |

---

## 内置智能体

### 通用智能体

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| ConversationalAgent | 对话智能体 | 日常聊天、问答 |
| ReactAgent | ReAct 推理智能体 | 复杂推理、工具调用 |

### 领域专用智能体

#### ITProjectManagerAgent（IT 项目管理智能体）

自动化 IT 项目全生命周期文档管理：

1. **PRD 创建** - 生成产品需求文档
2. **PRD 评审** - 需求评审流程，记录评审意见
3. **HLD 设计** - 系统架构设计
4. **LLD 设计** - 详细设计
5. **任务分配** - 自动生成开发任务清单

#### ProjectRDAgent（项目研发智能体）

自动创建项目研发目录结构：

```
project-name/
├── src/project_name/       # 源代码
│   ├── modules/
│   ├── utils/
│   └── models/
├── tests/                  # 测试目录
├── docs/                   # 文档
├── config/                 # 配置文件
├── scripts/                # 脚本
├── logs/                   # 日志
├── data/                   # 数据
├── .github/workflows/      # CI/CD
├── README.md
├── requirements.txt
└── setup.py
```

---

## API 使用指南

### API 基础信息

- 基础 URL: `http://localhost:8000`
- API 文档: `http://localhost:8000/docs`
- 健康检查: `http://localhost:8000/health`

### 核心端点

#### 1. 创建智能体

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-agent",
    "type": "conversational",
    "description": "我的第一个智能体"
  }'
```

**响应示例：**
```json
{
  "id": "agent_123456",
  "name": "my-agent",
  "description": "我的第一个智能体",
  "type": "conversational",
  "status": "created"
}
```

#### 2. 列出所有智能体

```bash
curl -X GET http://localhost:8000/api/v1/agents
```

#### 3. 获取智能体详情

```bash
curl -X GET http://localhost:8000/api/v1/agents/agent_123456
```

#### 4. 运行智能体

```bash
curl -X POST http://localhost:8000/api/v1/agents/agent_123456/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": "你好，请介绍一下自己"
  }'
```

**响应示例：**
```json
{
  "agent_id": "agent_123456",
  "output": "你好！我是...",
  "status": "completed"
}
```

#### 5. 删除智能体

```bash
curl -X DELETE http://localhost:8000/api/v1/agents/agent_123456
```

---

## Python SDK 使用

### 创建对话智能体

```python
from agent_core.agents import ConversationalAgent, AgentConfig

# 创建智能体配置
config = AgentConfig(
    name="my-agent",
    description="一个有帮助的助手",
    max_iterations=10
)

# 创建智能体
agent = ConversationalAgent(config)

# 运行智能体
result = await agent.run("你好，世界！")
print(result)
```

### 使用 IT 项目管理智能体

```python
from agent_core.agents import ITProjectManagerAgent, AgentConfig

# 创建智能体配置
config = AgentConfig(
    name="it-project-manager",
    description="IT项目文档管理智能体",
    max_iterations=20
)

# 创建智能体
agent = ITProjectManagerAgent(config, project_name="ERP系统")

# 运行智能体
result = await agent.run({
    "project_name": "ERP系统",
    "project_info": {
        "background": "企业资源规划需求",
        "goals": "实现企业资源统一管理",
        "scope": "采购、销售、库存、财务模块",
        "user_roles": ["管理员", "采购员", "销售员", "仓管", "财务"],
        "core_features": ["用户管理", "权限管理", "采购", "销售", "库存", "财务"],
        "performance": "响应时间<2s，支持1000+并发"
    }
})

print(result["current_phase"])   # 当前阶段
print(result["documents"])       # 生成的文档
print(result["tasks"])          # 分配的任务
```

### 使用项目研发智能体

```python
from agent_core.agents import ProjectRDAgent, AgentConfig

# 创建智能体配置
config = AgentConfig(
    name="project-rd",
    description="项目研发目录创建智能体",
    max_iterations=5
)

# 创建智能体
agent = ProjectRDAgent(config, project_name="我的项目", base_path="./projects")

# 运行智能体
result = await agent.run({
    "project_name": "我的项目",
    "base_path": "./projects"
})

print(result["created_directories"])  # 创建的目录列表
print(result["created_files"])        # 创建的文件列表
```

---

## 技能系统

平台提供可扩展的技能（工具）系统：

| 技能 | 说明 |
|------|------|
| Web Search | 网页搜索 |
| Code Executor | 代码执行 |
| Data Analysis | 数据分析 |
| Document Processor | 文档处理 |

### 自定义技能

```python
from skills.base import Skill, SkillResult
from skills.registry import skill_registry

class MyCustomSkill(Skill):
    name = "my_custom_skill"
    description = "自定义技能描述"

    async def execute(self, **kwargs) -> SkillResult:
        # 实现你的逻辑
        return SkillResult(success=True, data={"result": "..."})

# 注册技能
skill_registry.register(MyCustomSkill())
```

---

## Docker 部署

### 开发环境

```bash
# 启动开发环境
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

### 生产环境

```bash
# 构建镜像
docker-compose build

# 启动生产服务
docker-compose -f docker-compose.yml up -d

# 扩展 Worker 数量
docker-compose up -d --scale worker=3
```

### 服务端口

| 服务 | 端口 |
|------|------|
| API | 8000 |
| Swagger UI | 8000/docs |
| Redis | 6379 |
| PostgreSQL | 5432 |
| Nginx | 80 |

---

## 常见问题

### 1. 连接 LLM 失败

检查 `.env` 文件中的 `LLM_API_KEY` 是否正确配置。

### 2. Redis 连接失败

确认 Redis 服务已启动：
```bash
docker-compose up -d redis
```

### 3. 数据库连接失败

确认 PostgreSQL 服务已启动：
```bash
docker-compose up -d postgres
```

---

## 开发命令

```bash
# 安装依赖
make install

# 运行开发服务器
make dev

# 运行测试
make test

# 代码检查
make lint

# 代码格式化
make format

# 构建 Docker 镜像
make docker-build
```

---

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    agent-api (API 服务)                  │
│                   FastAPI + REST API                     │
└─────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│agent-core   │   │agent-brain  │   │   skills    │
│  单体引擎   │   │   调度中心  │   │   技能系统   │
└─────────────┘   └─────────────┘   └─────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │    agent-worker (Worker) │
              │      Celery + Redis      │
              └─────────────────────────┘
```

---

如需更多信息，请参阅 [README.md](./README.md) 或访问项目文档。
