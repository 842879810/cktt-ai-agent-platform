"""
项目经理 Agent 默认工具

这些工具会在 ProjectManagerAgent 初始化时自动注册
"""

from ...tools import BaseTool, ToolConfig


class SearchDocTool(BaseTool):
    """搜索文档工具"""

    def __init__(self):
        super().__init__(ToolConfig(
            name="search_doc",
            description="搜索项目文档，返回相关文档内容",
            parameters={"query": "搜索关键词"}
        ))

    async def execute(self, query: str = "") -> dict:
        """执行搜索"""
        # TODO: 实现真正的文档搜索
        return {
            "results": [
                {"title": "需求文档.pdf", "content": f"关于 {query} 的需求文档..."},
            ],
            "total": 1
        }


class CreateJiraTaskTool(BaseTool):
    """创建 Jira 任务工具"""

    def __init__(self):
        super().__init__(ToolConfig(
            name="create_jira_task",
            description="在 Jira 创建任务",
            parameters={
                "title": "任务标题",
                "description": "任务描述",
                "assignee": "负责人"
            }
        ))

    async def execute(self, title: str = "", description: str = "", assignee: str = "") -> dict:
        """创建 Jira 任务"""
        # TODO: 调用 Jira API
        return {
            "task_id": "PROJ-001",
            "url": f"https://jira.example.com/browse/PROJ-001",
            "status": "created",
            "title": title,
            "assignee": assignee
        }


class SendNotificationTool(BaseTool):
    """发送通知工具"""

    def __init__(self):
        super().__init__(ToolConfig(
            name="send_notification",
            description="发送通知到钉钉/飞书/邮件",
            parameters={
                "channel": "dingtalk/feishu/email",
                "message": "通知内容"
            }
        ))

    async def execute(self, channel: str = "dingtalk", message: str = "") -> dict:
        """发送通知"""
        # TODO: 调用通知 API
        return {
            "status": "sent",
            "channel": channel,
            "message": message
        }


# 工具注册映射
DEFAULT_TOOL_CLASSES = {
    "search_doc": SearchDocTool,
    "create_jira_task": CreateJiraTaskTool,
    "send_notification": SendNotificationTool,
}


def get_default_tool(tool_name: str) -> BaseTool | None:
    """获取默认工具实例"""
    tool_class = DEFAULT_TOOL_CLASSES.get(tool_name)
    if tool_class:
        return tool_class()
    return None
