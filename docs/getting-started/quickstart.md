# 快速开始

## 创建第一个智能体

### Python SDK 方式

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

config = AgentConfig(
    name="it-project-manager",
    description="IT项目文档管理智能体",
    max_iterations=20
)

agent = ITProjectManagerAgent(config, project_name="ERP系统")

result = await agent.run({
    "project_name": "ERP系统",
    "project_info": {
        "background": "企业资源规划需求",
        "goals": "实现企业资源统一管理",
        "scope": "采购、销售、库存、财务模块"
    }
})
```

### 使用项目研发智能体

```python
from agent_core.agents import ProjectRDAgent, AgentConfig

config = AgentConfig(
    name="project-rd",
    description="项目研发目录创建智能体",
    max_iterations=5
)

agent = ProjectRDAgent(config, project_name="我的项目", base_path="./projects")

result = await agent.run({
    "project_name": "我的项目",
    "base_path": "./projects"
})
```

## 启动 API 服务

```bash
poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload
```

## API 调用

### 创建智能体

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-agent",
    "type": "conversational",
    "description": "测试智能体"
  }'
```

### 运行智能体

```bash
curl -X POST http://localhost:8000/api/v1/agents/agent_xxx/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": "你好"
  }'
```

### 查看 API 文档

访问 http://localhost:8000/docs 使用 Swagger UI。

## 下一步

- [配置说明](configuration.md) - 了解更多配置选项
- [架构概览](../architecture/overview.md) - 了解系统架构
- [数据库初始化](../scripts/database/schema.sql) - 初始化数据库
