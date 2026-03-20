# 系统设计

## 架构模式

项目采用 **Monorepo** 架构和 **模块化** 设计：

```
cktt-ai-agent-platform/
├── apps/              # 核心应用
│   ├── agent-core/   # 单体智能体引擎
│   ├── agent-brain/  # 中枢大脑
│   ├── agent-api/   # API 服务
│   └── agent-worker/# 后台任务
├── packages/         # 共享库
│   ├── common/      # 通用工具
│   ├── types/       # 类型定义
│   └── config/     # 配置管理
├── skills/          # 技能插件
├── services/        # 外部集成
│   ├── llm/        # LLM 提供商
│   └── storage/    # 存储服务
└── infrastructure/  # 部署配置
```

## 数据流

```
1. API 接收请求
      │
      ▼
2. Router 确定智能体/任务
      │
      ▼
3. Brain 编排执行
      │
      ▼
4. Core 运行智能体（工具 + 记忆）
      │
      ▼
5. 结果返回（同步 API 或异步 Worker）
```

## 核心模块

### Agent Core

- **Agents**: ConversationalAgent, ReactAgent, ITProjectManagerAgent, ProjectRDAgent
- **Chains**: 链式任务执行
- **Tools**: 工具注册与执行
- **Memory**: Buffer 记忆（会话）、Vector 记忆（语义搜索）

### Agent Brain

- **Router**: LLM 路由、任务路由
- **Scheduler**: 任务调度
- **Orchestrator**: 多智能体编排（Crew）
- **Coordinator**: 协调器

### Skills

- **Web Search**: 网页搜索
- **Code Executor**: 代码执行
- **Data Analysis**: 数据分析
- **Document Processor**: 文档处理

## 可扩展性

- **水平扩展**: 多个 API 实例
- **异步处理**: Celery Worker
- **向量搜索**: 语义检索
- **缓存**: Redis 缓存和消息队列

## 数据库设计

详见 [数据库初始化脚本](../../scripts/database/schema.sql)

主要表：
- `agents` - 智能体表
- `tasks` - 任务表
- `crews` - 智能体团队表
- `conversations` - 对话表
- `messages` - 消息表
- `memories` - 记忆表
- `tools` - 工具表

## 安全设计

- API 认证（待实现）
- 请求限流
- 审计日志
- 输入验证（Pydantic）
