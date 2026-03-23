"""
LLM 客户端 - 基于 LangChain 调用 MiniMax

使用方式：
    from agent_core.agents.llm_agent import create_llm_client

    llm = create_llm_client(
        model="MiniMax-M2.5",
        api_key="sk-xxx",
        temperature=0.5
    )

    result = await llm.complete("你好")
"""

from typing import Any
from langchain_openai import ChatOpenAI


def create_llm_client(
    model: str = "MiniMax-M2.5",
    api_key: str = "",
    temperature: float = 0.5,
    base_url: str = "https://api.minimaxi.com/v1",
    **kwargs
) -> "MiniMaxClient":
    """
    创建 LLM 客户端

    Args:
        model: 模型名称，如 MiniMax-M2.5
        api_key: API Key
        temperature: 温度参数
        base_url: API 地址

    Returns:
        LLM 客户端实例
    """
    return MiniMaxClient(
        model=model,
        api_key=api_key,
        temperature=temperature,
        base_url=base_url,
        **kwargs
    )


class MiniMaxClient:
    """MiniMax LLM 客户端"""

    def __init__(
        self,
        model: str = "MiniMax-M2.5",
        api_key: str = "",
        temperature: float = 0.5,
        base_url: str = "https://api.minimaxi.com/v1",
        **kwargs
    ):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = base_url

        # 创建 LangChain ChatOpenAI 实例
        self._client = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )

    async def complete(self, prompt: str, **kwargs) -> str:
        """
        调用 LLM 生成文本

        Args:
            prompt: 提示词

        Returns:
            生成的文本
        """
        # LangChain 的 ChatOpenAI 是同步的，需要用 asyncio.run 或同步调用
        response = self._client.invoke(prompt)
        return response.content

    async def complete_json(self, prompt: str, **kwargs) -> dict:
        """
        调用 LLM 生成 JSON

        Args:
            prompt: 提示词（需要说明返回 JSON）

        Returns:
            解析后的 JSON 对象
        """
        import json
        import re

        # 添加 JSON 格式要求
        json_prompt = prompt + "\n\n请直接返回 JSON，不要有任何解释、思考过程或 markdown 标记。"

        response = await self.complete(json_prompt)

        # 清理响应：移除 thinking 标签
        cleaned = re.sub(r'<think>[\s\S]*?</think>', '', response)
        cleaned = cleaned.strip()

        # 提取 JSON
        try:
            # 尝试直接解析
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # 尝试提取 ```json ``` 块
            match = re.search(r'```json\s*([\s\S]*?)\s*```', cleaned)
            if match:
                return json.loads(match.group(1))
            # 尝试提取 { }
            match = re.search(r'\{[\s\S]*\}', cleaned)
            if match:
                return json.loads(match.group(0))
            raise ValueError(f"无法解析 JSON: {cleaned[:200]}")

    async def complete_with_messages(self, messages: list[dict], **kwargs) -> str:
        """
        使用消息列表调用 LLM

        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]

        Returns:
            生成的文本
        """
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

        langchain_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            elif role == "system":
                langchain_messages.append(SystemMessage(content=content))

        response = self._client.invoke(langchain_messages)
        return response.content


# 便捷函数
def get_minimax_client(api_key: str, model: str = "MiniMax-M2.5") -> MiniMaxClient:
    """快速创建 MiniMax 客户端"""
    return create_llm_client(model=model, api_key=api_key)
