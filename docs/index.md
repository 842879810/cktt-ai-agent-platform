# CKTT AI Agent Platform

> 企业级智能体平台，面向业务场景提供自主决策、任务编排与多模态交互能力。

## 特性

- **多智能体支持**: 支持通用智能体（对话、ReAct）和领域专用智能体（IT项目管理、项目研发）
- **IT项目管理智能体**: 自动化IT项目全生命周期文档管理
- **项目研发智能体**: 自动创建项目研发目录结构
- **工具系统**: 可扩展的工具框架，支持网页搜索、代码执行、数据分析、文档处理等
- **记忆系统**: Buffer 记忆 + Vector 记忆，支持语义搜索
- **任务调度**: 基于 Celery + Redis 的异步任务处理
- **REST API**: 高性能 FastAPI RESTful 接口
- **多LLM支持**: 支持 OpenAI、Anthropic、本地（Ollama）
- **向量存储**: 支持 Qdrant、Milvus、Weaviate 向量数据库
- **容器部署**: Docker + Kubernetes 支持

## 快速链接

- [快速开始](getting-started/quickstart.md)
- [安装指南](getting-started/installation.md)
- [配置说明](getting-started/configuration.md)
- [架构概览](architecture/overview.md)
- [系统设计](architecture/system-design.md)
- [数据库初始化](../scripts/database/schema.sql)
- [中文使用说明](../USAGE.md)
