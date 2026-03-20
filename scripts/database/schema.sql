-- CKTT AI Agent Platform Database Schema
-- PostgreSQL 15+

-- ============================================================
-- 枚举类型定义
-- ============================================================

-- Agent 类型
CREATE TYPE agent_type AS ENUM (
    'conversational',
    'react',
    'planning',
    'tool_use',
    'it_project_manager',
    'project_rd'
);

-- Agent 状态
CREATE TYPE agent_status AS ENUM (
    'created',
    'running',
    'idle',
    'error',
    'stopped'
);

-- Task 状态
CREATE TYPE task_status AS ENUM (
    'pending',
    'scheduled',
    'running',
    'completed',
    'failed',
    'cancelled'
);

-- Task 优先级
CREATE TYPE task_priority AS ENUM (
    'low',
    'normal',
    'high',
    'critical'
);

-- Crew 状态
CREATE TYPE crew_status AS ENUM (
    'created',
    'running',
    'idle',
    'error'
);

-- Crew 策略
CREATE TYPE crew_strategy AS ENUM (
    'sequential',
    'parallel',
    'hybrid'
);

-- 消息角色
CREATE TYPE message_role AS ENUM (
    'user',
    'assistant',
    'system',
    'tool'
);

-- 记忆类型
CREATE TYPE memory_type AS ENUM (
    'buffer',
    'vector',
    'session'
);

-- 工具类型
CREATE TYPE tool_type AS ENUM (
    'function',
    'api',
    'search',
    'code_execution',
    'document'
);

-- ============================================================
-- Agent 智能体表
-- ============================================================
CREATE TABLE agents (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    type agent_type NOT NULL DEFAULT 'conversational',
    status agent_status NOT NULL DEFAULT 'created',
    config JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_created_at ON agents(created_at DESC);

-- ============================================================
-- Task 任务表
-- ============================================================
CREATE TABLE tasks (
    task_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    payload JSONB DEFAULT '{}',
    status task_status NOT NULL DEFAULT 'pending',
    priority task_priority NOT NULL DEFAULT 'normal',
    agent_id VARCHAR(255) REFERENCES agents(id) ON DELETE SET NULL,
    result JSONB,
    error TEXT,
    scheduled_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX idx_tasks_scheduled_at ON tasks(scheduled_at);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- ============================================================
-- Crew 智能体团队表
-- ============================================================
CREATE TABLE crews (
    crew_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    agent_ids JSONB DEFAULT '[]',
    status crew_status NOT NULL DEFAULT 'created',
    strategy crew_strategy NOT NULL DEFAULT 'parallel',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crews_status ON crews(status);
CREATE INDEX idx_crews_strategy ON crews(strategy);
CREATE INDEX idx_crews_created_at ON crews(created_at DESC);

-- ============================================================
-- Conversation 对话表
-- ============================================================
CREATE TABLE conversations (
    conversation_id VARCHAR(255) PRIMARY KEY,
    agent_id VARCHAR(255) REFERENCES agents(id) ON DELETE CASCADE,
    crew_id VARCHAR(255) REFERENCES crews(crew_id) ON DELETE SET NULL,
    title VARCHAR(500) DEFAULT '',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_conversations_agent_id ON conversations(agent_id);
CREATE INDEX idx_conversations_crew_id ON conversations(crew_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- ============================================================
-- Message 消息表
-- ============================================================
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    role message_role NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    token_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at DESC);
CREATE INDEX idx_messages_role ON messages(role);

-- ============================================================
-- Memory 记忆表
-- ============================================================
CREATE TABLE memories (
    id VARCHAR(255) PRIMARY KEY,
    agent_id VARCHAR(255) REFERENCES agents(id) ON DELETE CASCADE,
    session_id VARCHAR(255),
    conversation_id VARCHAR(255) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    memory_type memory_type NOT NULL DEFAULT 'buffer',
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),  -- OpenAI ada-002 dimension, 可根据实际模型调整
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_memories_agent_id ON memories(agent_id);
CREATE INDEX idx_memories_session_id ON memories(session_id);
CREATE INDEX idx_memories_conversation_id ON memories(conversation_id);
CREATE INDEX idx_memories_memory_type ON memories(memory_type);
CREATE INDEX idx_memories_created_at ON memories(created_at DESC);
CREATE INDEX idx_memories_expires_at ON memories(expires_at) WHERE expires_at IS NOT NULL;

-- 向量相似度搜索（需要 pgvector 扩展）
-- CREATE INDEX idx_memories_embedding ON memories USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================================
-- Tool 工具表
-- ============================================================
CREATE TABLE tools (
    name VARCHAR(255) PRIMARY KEY,
    description TEXT NOT NULL,
    type tool_type NOT NULL DEFAULT 'function',
    parameters JSONB DEFAULT '{}',
    returns JSONB DEFAULT '{}',
    is_async BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tools_type ON tools(type);
CREATE INDEX idx_tools_enabled ON tools(enabled);

-- ============================================================
-- Tool Execution 工具执行记录表
-- ============================================================
CREATE TABLE tool_executions (
    id BIGSERIAL PRIMARY KEY,
    task_id VARCHAR(255) REFERENCES tasks(task_id) ON DELETE SET NULL,
    agent_id VARCHAR(255) REFERENCES agents(id) ON DELETE SET NULL,
    tool_name VARCHAR(255) NOT NULL,
    parameters JSONB DEFAULT '{}',
    result JSONB,
    error TEXT,
    duration DECIMAL(10, 3) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'success',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tool_executions_task_id ON tool_executions(task_id);
CREATE INDEX idx_tool_executions_agent_id ON tool_executions(agent_id);
CREATE INDEX idx_tool_executions_tool_name ON tool_executions(tool_name);
CREATE INDEX idx_tool_executions_created_at ON tool_executions(created_at DESC);

-- ============================================================
-- Agent Session 智能体会话表
-- ============================================================
CREATE TABLE agent_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    agent_id VARCHAR(255) REFERENCES agents(id) ON DELETE CASCADE,
    conversation_id VARCHAR(255) REFERENCES conversations(conversation_id) ON DELETE SET NULL,
    context JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_agent_sessions_agent_id ON agent_sessions(agent_id);
CREATE INDEX idx_agent_sessions_conversation_id ON agent_sessions(conversation_id);
CREATE INDEX idx_agent_sessions_created_at ON agent_sessions(created_at DESC);

-- ============================================================
-- Audit Log 审计日志表
-- ============================================================
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    user_id VARCHAR(255),
    details JSONB DEFAULT '{}',
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- ============================================================
-- 触发器：自动更新 updated_at
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Agent 更新触发器
CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Task 更新触发器
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Crew 更新触发器
CREATE TRIGGER update_crews_updated_at
    BEFORE UPDATE ON crews
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Conversation 更新触发器
CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Tool 更新触发器
CREATE TRIGGER update_tools_updated_at
    BEFORE UPDATE ON tools
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Agent Session 更新触发器
CREATE TRIGGER update_agent_sessions_updated_at
    BEFORE UPDATE ON agent_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- 视图：任务统计
-- ============================================================
CREATE VIEW task_statistics AS
SELECT
    agent_id,
    status,
    priority,
    COUNT(*) as count,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_duration_seconds
FROM tasks
WHERE completed_at IS NOT NULL
GROUP BY agent_id, status, priority;

-- ============================================================
-- 视图：Agent 统计
-- ============================================================
CREATE VIEW agent_statistics AS
SELECT
    a.id,
    a.name,
    a.type,
    a.status,
    COUNT(DISTINCT t.task_id) as total_tasks,
    COUNT(DISTINCT t.task_id) FILTER (WHERE t.status = 'completed') as completed_tasks,
    COUNT(DISTINCT t.task_id) FILTER (WHERE t.status = 'failed') as failed_tasks,
    COUNT(DISTINCT c.conversation_id) as total_conversations,
    a.created_at,
    a.updated_at
FROM agents a
LEFT JOIN tasks t ON t.agent_id = a.id
LEFT JOIN conversations c ON c.agent_id = a.id
GROUP BY a.id, a.name, a.type, a.status, a.created_at, a.updated_at;

-- ============================================================
-- 初始数据：内置工具
-- ============================================================
INSERT INTO tools (name, description, type, parameters, returns, is_async, enabled) VALUES
('web_search', 'Search the web for information', 'search', '{"type": "object", "properties": {"query": {"type": "string", "description": "Search query"}}, "required": ["query"]}', '{"type": "object", "properties": {"results": {"type": "array"}}}', true, true),
('code_executor', 'Execute code in a sandboxed environment', 'code_execution', '{"type": "object", "properties": {"code": {"type": "string"}, "language": {"type": "string", "enum": ["python", "javascript", "bash"]}}, "required": ["code"]}', '{"type": "object", "properties": {"output": {"type": "string"}, "error": {"type": "string"}}}', true, true),
('data_analysis', 'Analyze data and generate insights', 'function', '{"type": "object", "properties": {"data": {"type": "object"}, "analysis_type": {"type": "string"}}, "required": ["data"]}', '{"type": "object", "properties": {"insights": {"type": "array"}, "summary": {"type": "string"}}}', true, true),
('document_processor', 'Process and analyze documents', 'document', '{"type": "object", "properties": {"document_path": {"type": "string"}, "operation": {"type": "string", "enum": ["extract", "summarize", "analyze"]}}, "required": ["document_path"]}', '{"type": "object", "properties": {"content": {"type": "string"}, "metadata": {"type": "object"}}}', true, true);

-- ============================================================
-- 权限设置（根据实际情况调整）
-- ============================================================
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO agent_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO agent_user;
