# 配置说明

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|-------|
| DEBUG | 调试模式 | false |
| ENVIRONMENT | 环境名称 | development |
| API_HOST | API 主机 | 0.0.0.0 |
| API_PORT | API 端口 | 8000 |
| DATABASE_HOST | PostgreSQL 主机 | localhost |
| DATABASE_PORT | PostgreSQL 端口 | 5432 |
| DATABASE_NAME | 数据库名称 | agent_platform |
| DATABASE_USER | 数据库用户 | postgres |
| DATABASE_PASSWORD | 数据库密码 | postgres |
| REDIS_HOST | Redis 主机 | localhost |
| REDIS_PORT | Redis 端口 | 6379 |
| REDIS_DB | Redis 数据库编号 | 0 |
| LLM_PROVIDER | LLM 提供商 | openai |
| LLM_API_KEY | LLM API 密钥 | - |
| LLM_MODEL | LLM 模型 | gpt-4 |

## LLM 提供商配置

### OpenAI

```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-xxx
LLM_MODEL=gpt-4
```

### Anthropic

```bash
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-xxx
LLM_MODEL=claude-3-opus-20240229
```

### 本地（Ollama）

```bash
LLM_PROVIDER=local
LLM_API_KEY=ollama
LLM_MODEL=llama2
```

## 配置文件

配置文件位于 `config/` 目录：

| 文件 | 说明 |
|------|------|
| `config/base.yaml` | 基础配置 |
| `config/development.yaml` | 开发环境配置 |
| `config/staging.yaml` | 预发布环境配置 |
| `config/production.yaml` | 生产环境配置 |

## 向量数据库配置

### Qdrant

```bash
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### Milvus

```bash
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### Weaviate

```bash
WEAVIATE_URL=http://localhost:8080
```

## Docker 环境变量

在 `docker-compose.yml` 中配置：

```yaml
services:
  api:
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - DATABASE_HOST=postgres
      - DATABASE_PORT=5432
      - LLM_PROVIDER=openai
      - LLM_API_KEY=${LLM_API_KEY}
```
