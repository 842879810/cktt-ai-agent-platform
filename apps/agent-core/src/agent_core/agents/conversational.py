"""
对话型智能体实现模块

本模块实现了对话型智能体（Conversational Agent），用于处理日常对话和问答交互。

主要特点：
- 简单的请求-响应模式
- 支持系统提示词配置
- 适合构建聊天机器人和问答系统

使用示例：
    from agent_core.agents import ConversationalAgent, AgentConfig

    config = AgentConfig(name="chat-bot", description="客服机器人")
    agent = ConversationalAgent(config, system_prompt="你是一个友好的客服助手")
    response = await agent.run("你好")
"""

from typing import Any, Optional

from .base import AgentConfig, BaseAgent


class ConversationalAgent(BaseAgent):
    """
    对话型智能体

    用于处理基于对话的交互任务。
    采用简单的请求-响应模式，适合构建聊天机器人和问答系统。

    工作流程：
    1. 接收用户输入
    2. 生成响应内容
    3. 返回响应结果

    特点：
    - 简单直观，易于使用
    - 支持系统提示词配置
    - 适合简单的问答场景

    使用方式：
    1. 创建智能体实例，可传入系统提示词
    2. 调用run方法，传入用户输入
    3. 获取响应结果
    """

    def __init__(self, config: AgentConfig, system_prompt: Optional[str] = None):
        """
        初始化对话型智能体

        Args:
            config: 智能体配置对象
            system_prompt: 可选的系统提示词，用于设定智能体的角色和行为
        """
        super().__init__(config)
        # 设置系统提示词，默认为通用助手
        self.system_prompt = system_prompt or "You are a helpful AI assistant."

    async def run(self, input_data: Any) -> Any:
        """
        运行对话型智能体

        接收用户输入，生成响应并返回。
        这是最简单的智能体模式，适合简单的一问一答场景。

        Args:
            input_data: 用户输入，可以是文本或其他类型

        Returns:
            生成的响应内容
        """
        self.reset()  # 重置状态
        self.state.context["input"] = input_data  # 存储输入

        # 处理输入并生成响应
        # 在实际应用中，这里会调用LLM生成响应
        response = await self._generate_response(input_data)

        # 存储输出并标记完成
        self.state.context["output"] = response
        self.state.is_complete = True

        return response

    async def step(self) -> Any:
        """
        执行单步操作

        对话型智能体的step方法直接调用run方法，
        因为对话型智能体不需要多轮迭代。

        Returns:
            响应结果
        """
        return await self.run(self.state.context.get("input"))

    async def _generate_response(self, input_data: Any) -> str:
        """
        生成响应内容

        根据用户输入生成响应。
        在实际应用中，这里会接入LLM进行更智能的响应生成。

        Args:
            input_data: 用户输入

        Returns:
            生成的响应文本
        """
        # 占位实现，返回带输入前缀的响应
        # 实际应用中应接入LLM或对话系统
        return f"Response to: {input_data}"
