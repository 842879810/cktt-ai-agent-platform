# 安装指南

## 前置要求

| 依赖 | 版本要求 |
|------|---------|
| Python | 3.11+ |
| Poetry | 最新版 |
| Docker & Docker Compose | 可选 |

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/cktt/ai-agent-platform.git
cd cktt-ai-agent-platform
```

### 2. 安装依赖

```bash
poetry install
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的参数
```

### 4. 启动服务

#### 方式一：Docker 启动（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 或仅启动依赖服务
docker-compose up -d redis postgres
```

#### 方式二：本地启动

```bash
# 启动 API 服务
poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 初始化数据库

```bash
# 执行建表脚本
psql -d agent_platform -f scripts/database/schema.sql
```

或使用 Docker：

```bash
docker exec -it cktt-postgres psql -U postgres -d agent_platform -f /path/to/schema.sql
```

## 验证安装

1. 访问 http://localhost:8000 查看 API 文档
2. 访问 http://localhost:8000/docs 查看 Swagger UI
3. 访问 http://localhost:8000/health 检查服务健康状态

## 常见问题

### Poetry 安装失败

```bash
# 安装 poetry
pip install poetry

# 或使用官方脚本
curl -sSL https://install.python-poetry.org | python3 -
```

### Docker 服务启动失败

```bash
# 检查 Docker 状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 端口占用

如果 8000 端口被占用，可以指定其他端口：

```bash
poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload --port 8001
```
