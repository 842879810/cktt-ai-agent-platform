# 数据库初始化脚本

## 快速开始

### 1. 方式一：Docker 环境（推荐）

```bash
# 启动 PostgreSQL
docker-compose up -d postgres

# 进入 PostgreSQL 容器
docker exec -it cktt-postgres psql -U postgres

# 执行建表脚本
\i /docker-entrypoint-initdb.d/schema.sql
```

### 2. 方式二：本地 PostgreSQL

```bash
# 创建数据库
createdb agent_platform

# 执行建表脚本
psql -d agent_platform -f schema.sql
```

### 3. 方式三：使用 psql 命令行

```bash
# 连接数据库
psql -h localhost -U postgres -d agent_platform

# 执行 SQL
\i scripts/database/schema.sql
```

## 表结构说明

| 表名 | 说明 |
|------|------|
| `agents` | 智能体表 |
| `tasks` | 任务表 |
| `crews` | 智能体团队表 |
| `conversations` | 对话表 |
| `messages` | 消息表 |
| `memories` | 记忆表 |
| `tools` | 工具表 |
| `tool_executions` | 工具执行记录表 |
| `agent_sessions` | 智能体会话表 |
| `audit_logs` | 审计日志表 |

## 可选：向量搜索支持

如果需要向量相似度搜索，需要安装 `pgvector` 扩展：

```sql
-- 安装 pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- 向量维度根据实际使用的 embedding 模型调整
-- OpenAI ada-002: 1536
-- text-embedding-3-small: 1536
-- text-embedding-3-large: 3072

-- 修改 memories 表的 embedding 列类型
ALTER TABLE memories ALTER COLUMN embedding TYPE vector(1536);

-- 创建向量索引
CREATE INDEX idx_memories_embedding ON memories
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

## 用户权限

```sql
-- 创建专用用户
CREATE USER agent_user WITH PASSWORD 'your_password';

-- 授权
GRANT CONNECT ON DATABASE agent_platform TO agent_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO agent_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO agent_user;

-- 设置默认权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO agent_user;
```

## 环境变量配置

确保 `.env` 中的数据库配置正确：

```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=agent_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```
