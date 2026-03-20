# 架构概览

## 系统组件

### Agent Core (`apps/agent-core`)
- **智能体实现**: ReAct、Conversational、ITProjectManager、ProjectRD
- **Chain 编排**: 链式任务执行
- **工具系统**: 可扩展的工具框架
- **记忆管理**: Buffer 记忆 + Vector 记忆

### Agent Brain (`apps/agent-brain`)
- **任务路由**: 智能任务分发
- **LLM 路由**: 多模型路由选择
- **任务调度**: 异步任务调度
- **多智能体编排**: Crew 编排器

### Agent API (`apps/agent-api`)
- **FastAPI REST API**: 高性能接口
- **端点**: Agents、Tasks、Crews
- **中间件**: 认证、限流、日志

### Agent Worker (`apps/agent-worker`)
- **Celery Worker**: 异步任务处理
- **后台任务**: 长时任务执行

## 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI |
| 任务队列 | Celery + Redis |
| 数据库 | PostgreSQL |
| 缓存 | Redis |
| 向量存储 | Qdrant / Milvus / Weaviate |
| LLM | OpenAI / Anthropic / Ollama |
| 测试 | pytest + pytest-asyncio |

## 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    agent-api (API 服务)                  │
│                   FastAPI + REST API                     │
│                     :8000/docs                           │
└─────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ agent-core  │   │ agent-brain  │   │   skills    │
│  单体引擎   │   │   调度中心   │   │   技能系统   │
│             │   │             │   │             │
│ • Agents    │   │ • Router    │   │ • web_search│
│ • Chains    │   │ • Scheduler │   │ • code_exec │
│ • Tools     │   │ • Orchestrat│   │ • data_anal │
│ • Memory    │   │ • Coordinatr │   │ • doc_proc  │
└─────────────┘   └─────────────┘   └─────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │    agent-worker (Worker) │
              │      Celery + Redis      │
              └─────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
        ┌──────────┐             ┌──────────┐
        │PostgreSQL│             │  Redis   │
        │  :5432   │             │  :6379   │
        └──────────┘             └──────────┘
              │                         │
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │    Vector Databases     │
              │ Qdrant/Milvus/Weaviate  │
              └─────────────────────────┘
```

## 子项目职责

| 子项目 | 职责 | 独立部署 |
|--------|------|---------|
| agent-core | 单体智能体引擎（含IT项目管理、项目研发Agent） | 是 |
| agent-brain | 任务调度、路由、多智能体编排 | 是 |
| agent-api | RESTful API 服务 | 是 |
| agent-worker | 异步任务处理 | 是 |
| skills | 插件化技能系统 | 运行时加载 |
