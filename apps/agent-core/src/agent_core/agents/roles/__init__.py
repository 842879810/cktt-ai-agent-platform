"""
角色智能体模块

本模块包含各种角色的智能体实现：
- ProjectManagerAgent: 项目经理智能体，负责项目计划和任务分配

使用示例：
    from agent_core.agents.roles import ProjectManagerAgent, AgentConfig

    agent = ProjectManagerAgent(AgentConfig(name="pm"), project_name="ERP系统")
    result = await agent.run({"project_name": "ERP系统"})

或者直接从 roles 目录导入：
    from agent_core.agents.roles.project_manager import ProjectManagerAgent
"""

# 导入项目经理智能体
from .project_manager import PMPhase, ProjectManagerAgent, TaskStatus

__all__ = [
    # 项目经理智能体
    "ProjectManagerAgent",       # 项目经理智能体
    "PMPhase",                  # 项目经理阶段枚举
    "TaskStatus",               # 任务状态枚举
]
