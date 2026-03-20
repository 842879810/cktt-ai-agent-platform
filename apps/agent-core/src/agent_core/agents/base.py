"""
智能体基类模块

本模块定义了所有智能体的基类和配置模型，提供了智能体的核心抽象接口。
智能体（Agent）是平台的核心执行单元，每个智能体都遵循"输入 -> 处理 -> 输出"的基本模式。

主要组件：
- AgentConfig: 智能体配置模型，定义智能体的基本参数
- AgentState: 智能体运行状态，跟踪执行过程中的状态信息
- BaseAgent: 抽象基类，定义智能体的核心接口
"""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """
    智能体配置模型

    用于配置智能体的基本参数，包括名称、描述、最大迭代次数和超时时间等。
    这些配置决定了智能体的行为特征和运行约束。

    属性说明：
    - name: 智能体名称，用于唯一标识智能体
    - description: 智能体描述，说明智能体的用途和功能
    - max_iterations: 最大迭代次数，限制智能体单次运行的最大循环次数
    - timeout: 超时时间（秒），限制智能体单次运行的最大时长
    """

    name: str  # 智能体名称
    description: str = ""  # 智能体描述
    max_iterations: int = 10  # 最大迭代次数，默认10次
    timeout: int = 300  # 超时时间，默认300秒


class AgentState(BaseModel):
    """
    智能体运行状态模型

    跟踪智能体在执行过程中的状态信息，包括当前迭代次数、记忆内容、上下文数据等。
    这些状态信息对于调试和监控智能体的运行过程非常重要。

    属性说明：
    - iteration: 当前迭代次数，从0开始计数
    - memory: 记忆列表，存储智能体运行过程中的关键信息
    - context: 上下文字典，存储智能体运行过程中的临时数据
    - is_complete: 是否完成，标识智能体是否已完成执行
    - error: 错误信息，当执行发生错误时存储错误描述
    """

    iteration: int = 0  # 当前迭代次数
    memory: list[str] = Field(default_factory=list)  # 记忆列表
    context: dict[str, Any] = Field(default_factory=dict)  # 上下文数据
    is_complete: bool = False  # 是否完成执行
    error: str | None = None  # 错误信息


class BaseAgent(ABC):
    """
    智能体抽象基类

    所有具体智能体实现的基类，定义了智能体的核心接口。
    任何继承自此类的智能体都必须实现run和step方法。

    使用方式：
    1. 创建子类继承BaseAgent
    2. 实现run方法定义智能体的主运行逻辑
    3. 实现step方法定义智能体的单步执行逻辑

    示例：
        class MyAgent(BaseAgent):
            async def run(self, input_data):
                # 实现主运行逻辑
                pass

            async def step(self):
                # 实现单步执行逻辑
                pass
    """

    def __init__(self, config: AgentConfig):
        """
        初始化智能体

        Args:
            config: 智能体配置对象，包含智能体的基本参数
        """
        self.config = config  # 保存配置
        self.state = AgentState()  # 初始化运行状态

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """
        运行智能体的主入口方法

        这是智能体的核心方法，定义了智能体的完整执行流程。
        子类必须实现此方法以定义自己的运行逻辑。

        Args:
            input_data: 输入数据，可以是任意类型，取决于智能体的需求

        Returns:
            Any: 智能体的执行结果，类型取决于智能体的实现
        """
        pass

    @abstractmethod
    async def step(self) -> Any:
        """
        执行智能体的单步操作

        此方法定义智能体的单次迭代行为，通常用于需要多轮交互的智能体。
        每次调用step方法应该推进智能体到一个新的状态。

        Returns:
            Any: 单步执行的结果
        """
        pass

    def reset(self) -> None:
        """
        重置智能体状态

        将智能体的运行状态重置为初始状态，清除所有记忆和上下文数据。
        这在需要复用智能体实例但希望重新开始时非常有用。
        """
        self.state = AgentState()

    @property
    def name(self) -> str:
        """
        获取智能体名称

        Returns:
            str: 智能体的名称
        """
        return self.config.name
