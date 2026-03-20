"""
智能体模块

本模块提供了平台内置的多种智能体实现，用于满足不同场景的需求。

智能体类型：

1. 通用智能体：
   - ConversationalAgent: 对话型智能体，适合简单的一问一答场景
   - ReactAgent: ReAct推理智能体，适合需要多步推理和工具调用的复杂任务

2. 垂直领域智能体：
   - ITProjectManagerAgent: IT项目管理智能体，自动化管理IT项目文档流程
   - ProjectRDAgent: 项目研发智能体，自动创建项目目录结构和代码模板

使用示例：
    from agent_core.agents import (
        ConversationalAgent,
        ReactAgent,
        ITProjectManagerAgent,
        ProjectRDAgent,
        AgentConfig
    )

    # 对话型智能体
    config = AgentConfig(name="chatbot")
    agent = ConversationalAgent(config)
    response = await agent.run("你好")

    # IT项目管理智能体
    config = AgentConfig(name="it-pm")
    agent = ITProjectManagerAgent(config, project_name="ERP系统")
    result = await agent.run({"project_name": "ERP系统"})

    # 项目研发智能体
    config = AgentConfig(name="rd")
    agent = ProjectRDAgent(config, project_name="MyProject")
    result = await agent.run({"project_name": "MyProject"})
"""

from .base import AgentConfig, AgentState, BaseAgent
from .react import ReactAgent
from .conversational import ConversationalAgent
from .it_project_manager import ITProjectManagerAgent, ProjectPhase, DocumentStatus
from .project_rd import ProjectRDAgent, RDPhase

__all__ = [
    "AgentConfig",                # 智能体配置模型
    "AgentState",                 # 智能体运行状态
    "BaseAgent",                 # 智能体抽象基类
    "ReactAgent",                # ReAct推理智能体
    "ConversationalAgent",       # 对话型智能体
    "ITProjectManagerAgent",     # IT项目管理智能体
    "ProjectPhase",              # IT项目阶段枚举
    "DocumentStatus",            # 文档状态枚举
    "ProjectRDAgent",           # 项目研发智能体
    "RDPhase",                  # 研发阶段枚举
]
