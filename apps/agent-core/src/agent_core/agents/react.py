"""
ReAct智能体实现模块

本模块实现了ReAct（Reasoning + Acting）推理智能体，这是一种结合推理和行动的智能体模式。

ReAct模式的核心思想：
1. Thought（思考）- 分析当前状态，决定下一步行动
2. Action（行动）- 执行具体的工具调用或动作
3. Observation（观察）- 观察行动的结果，用于下一步推理

这种模式使智能体能够：
- 自主决定使用哪些工具
- 根据观察结果调整后续行动
- 通过多轮迭代解决复杂问题

使用示例：
    from agent_core.agents import ReactAgent, AgentConfig

    config = AgentConfig(name="react-agent", max_iterations=10)
    agent = ReactAgent(config, tools=[tool1, tool2])
    result = await agent.run("帮我查询今天的天气")
"""

from typing import Any, Dict, Optional

from .base import AgentConfig, AgentState, BaseAgent


class ReactAgent(BaseAgent):
    """
    ReAct（推理+行动）智能体

    ReAct是一种结合推理和行动的智能体架构。
    它通过多轮迭代的方式，每次循环包括思考、行动、观察三个步骤，
    直到任务完成或达到最大迭代次数。

    工作流程：
    1. 思考(Thought) - 分析当前状态和输入，决定下一步行动
    2. 行动(Action) - 执行工具调用或其他动作
    3. 观察(Observation) - 获取行动的结果
    4. 检查是否完成，如果没有则继续循环

    特点：
    - 支持工具调用，可以扩展各种能力
    - 通过观察结果动态调整策略
    - 适合处理需要多步推理的复杂任务

    使用方式：
    1. 创建智能体实例，可传入工具列表
    2. 调用run方法，传入任务描述
    3. 获取执行结果
    """

    def __init__(self, config: AgentConfig, tools: Optional[list] = None):
        """
        初始化ReAct智能体

        Args:
            config: 智能体配置对象
            tools: 可选的工具列表，用于扩展智能体能力
        """
        super().__init__(config)
        self.tools = tools or []  # 工具列表

    async def run(self, input_data: Any) -> Any:
        """
        运行ReAct智能体

        执行完整的多轮迭代流程，直到任务完成或达到最大迭代次数。

        Args:
            input_data: 输入数据，通常是任务描述或问题

        Returns:
            智能体的最终输出结果
        """
        self.reset()  # 重置状态
        self.state.context["input"] = input_data  # 存储输入

        # 迭代执行，直到完成或达到最大迭代次数
        # 每轮迭代执行一个完整的ReAct循环
        while not self.state.is_complete and self.state.iteration < self.config.max_iterations:
            await self.step()  # 执行单步

        # 返回最终的输出结果
        return self.state.context.get("output")

    async def step(self) -> Any:
        """
        执行单个ReAct步骤

        一个完整的ReAct循环包括：
        1. Thought - 思考当前状态
        2. Action - 执行动作
        3. Observation - 观察结果

        Returns:
            当前步骤的观察结果
        """
        self.state.iteration += 1  # 增加迭代计数

        # 第一步：思考（Thought）
        # 分析当前状态，决定下一步要做什么
        thought = self._reason()
        self.state.memory.append(f"Thought: {thought}")

        # 第二步：行动（Action）
        # 根据思考结果执行具体的动作
        action = self._act(thought)
        self.state.memory.append(f"Action: {action}")

        # 第三步：观察（Observation）
        # 获取动作执行后的结果
        observation = self._observe(action)
        self.state.memory.append(f"Observation: {observation}")

        # 检查是否完成
        # 如果观察结果中包含"complete"关键词，则认为任务完成
        if self._is_complete(observation):
            self.state.is_complete = True
            self.state.context["output"] = observation

        return observation

    def _reason(self) -> str:
        """
        推理过程

        分析当前状态，生成思考结果。
        在实际应用中，这里可以接入LLM进行更复杂的推理。

        Returns:
            思考结果字符串
        """
        return f"Reasoning about iteration {self.state.iteration}"

    def _act(self, thought: str) -> str:
        """
        行动过程

        根据思考结果决定并执行具体的动作。
        可以调用工具、API或其他资源。

        Args:
            thought: 思考结果

        Returns:
            执行的动作描述
        """
        return f"Action based on: {thought[:50]}"

    def _observe(self, action: str) -> str:
        """
        观察过程

        获取动作执行后的结果。
        在实际应用中，这里会获取工具的返回值。

        Args:
            action: 执行的动作

        Returns:
            观察结果
        """
        return f"Observation for: {action[:50]}"

    def _is_complete(self, observation: str) -> bool:
        """
        检查是否完成

        根据观察结果判断任务是否完成。
        在实际应用中，这里可以根据更复杂的条件判断。

        Args:
            observation: 观察结果

        Returns:
            是否完成
        """
        return "complete" in observation.lower()
