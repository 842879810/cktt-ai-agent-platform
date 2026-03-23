"""
项目经理智能体模块

本模块实现了项目经理智能体，专注于项目计划制定和任务分配。

主要功能：
1. 项目计划制定 - 制定项目里程碑和时间表
2. 任务分解 - 将工作分解为可执行的任务
3. 资源规划 - 分配人力和时间资源
4. 任务分配 - 将任务分配给团队成员

工作流程：
    项目计划制定 -> 任务分解 -> 资源规划 -> 任务分配

使用示例：
    from agent_core.agents import ProjectManagerAgent, AgentConfig

    # 方式1: 自动使用环境变量的 LLM 配置
    # 环境变量: OPENAI_API_KEY 或 MINIMAX_API_KEY
    config = AgentConfig(name="pm", description="项目经理智能体")
    agent = ProjectManagerAgent(config, project_name="ERP系统")
    result = await agent.run({"project_name": "ERP系统"})

    # 方式2: 手动传入 LLM 客户端
    from agent_core.agents import create_llm_client
    llm = create_llm_client(api_key="sk-xxx")
    agent = ProjectManagerAgent(config, project_name="ERP系统", llm_client=llm)
    result = await agent.run({"project_name": "ERP系统"})
"""
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from ..base import AgentConfig, BaseAgent


class StrEnum(str, Enum):
    """StrEnum兼容 Python 3.10及以下版本"""
    pass


class PMPhase(StrEnum):
    """
    项目经理工作阶段枚举

    定义项目经理工作的各个阶段。
    """

    PROJECT_PLANNING = "project_planning"  # 项目计划制定
    TASK_BREAKDOWN = "task_breakdown"  # 任务分解
    RESOURCE_PLANNING = "resource_planning"  # 资源规划
    TASK_ASSIGNMENT = "task_assignment"  # 任务分配
    COMPLETED = "completed"  # 完成


class TaskStatus(StrEnum):
    """任务状态枚举"""
    PENDING = "pending"  # 待开始
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    BLOCKED = "blocked"  # 阻塞
    CANCELLED = "cancelled"  # 已取消


class ProjectManagerAgent(BaseAgent):
    """
    项目经理智能体

    专注于项目计划和任务管理的智能体，帮助完成从项目规划到任务分配的完整流程。

    主要功能：
    1. 项目计划制定 - 制定项目里程碑、阶段计划、时间表
    2. 任务分解 - 将项目分解为可执行的任务清单
    3. 资源规划 - 估算工时、分配资源
    4. 任务分配 - 分配任务给团队成员、设置优先级

    文档产出：
    - 项目计划书
    - 任务清单
    - 资源分配表
    - 项目时间表

    使用方式：
        config = AgentConfig(name="project_manager")
        agent = ProjectManagerAgent(config, project_name="MyProject")
        result = await agent.run({
            "project_name": "MyProject",
            "features": [...],
            "architecture": {...}
        })
    """

    # LLM 默认配置（写死）
    DEFAULT_LLM_API_KEY = "sk-cp-stgG1X1C7dN0e2oDkMa-hMkoVDTlXfVTyGsjFUU7SwsrENGeuYJ4aRwb2CxbdRRm-oaq9-EIoKPKpIIgzOob5aV6o6Dy4Nxg0utJpHaABuh1Ai-xP6VtXSo"
    DEFAULT_LLM_MODEL = "MiniMax-M2.5"
    DEFAULT_LLM_BASE_URL = "https://api.minimaxi.com/v1"

    # 默认工具列表（写死在这里）
    DEFAULT_TOOLS: list = [
        {"name": "search_doc", "description": "搜索项目文档，返回相关文档内容"},
        {"name": "create_jira_task", "description": "在 Jira 创建任务"},
    ]

    def __init__(
        self,
        config: AgentConfig,
        project_name: str = "",
        llm_client=None,
        llm_api_key: str | None = None,
        llm_model: str | None = None,
        llm_base_url: str | None = None,
        tool_registry=None,
        max_react_iterations: int = 5
    ):
        """
        初始化项目经理智能体

        Args:
            config: 智能体配置对象
            project_name: 项目名称
            llm_client: LLM 客户端（可选）
            llm_api_key: API Key（可选，默认使用内置配置）
            llm_model: 模型名称（可选，默认 MiniMax-M2.5）
            llm_base_url: API 地址（可选）
            tool_registry: 工具注册表（可选，支持 ReAct 工具调用）
            max_react_iterations: ReAct 最大迭代次数
        """
        super().__init__(config)
        self.project_name = project_name

        # 如果没有传入 llm_client，自动创建
        if llm_client is not None:
            self.llm_client = llm_client
        else:
            # 使用内置配置或传入的配置
            api_key = llm_api_key or self.DEFAULT_LLM_API_KEY
            model = llm_model or self.DEFAULT_LLM_MODEL
            base_url = llm_base_url or self.DEFAULT_LLM_BASE_URL

            from ..llm_agent import create_llm_client
            self.llm_client = create_llm_client(
                api_key=api_key,
                model=model,
                base_url=base_url
            )

        # 工具注册表（支持 ReAct）
        from ...tools import ToolRegistry
        self.tool_registry = tool_registry or ToolRegistry()

        # 自动注册默认工具（如果注册表为空）
        if tool_registry is None and self.DEFAULT_TOOLS:
            self._register_default_tools()

        self.max_react_iterations = max_react_iterations

        self.current_phase = PMPhase.PROJECT_PLANNING
        self.documents: dict[str, Any] = {}
        self.project_plan: dict[str, Any] = {}
        self.tasks: list[dict[str, Any]] = []
        self.resources: dict[str, Any] = {}

    async def run(self, input_data: Any) -> Any:
        """
        运行项目经理智能体的主入口

        执行完整的工作流程：项目计划制定 -> 任务分解 -> 资源规划 -> 任务分配

        Args:
            input_data: 输入数据字典，应包含：
                - project_name: 项目名称
                - features: 功能列表（可选）
                - architecture: 架构设计（可选）

        Returns:
            包含以下键的字典：
                - project_name: 项目名称
                - current_phase: 当前阶段
                - project_plan: 项目计划
                - tasks: 任务清单
                - resources: 资源分配
                - workflow_results: 各阶段执行结果
        """
        self.reset()

        if isinstance(input_data, dict):
            self.project_name = input_data.get("project_name", "Untitled Project")
            self.state.context["project_name"] = self.project_name
            self.state.context["features"] = input_data.get("features", [])
            self.state.context["architecture"] = input_data.get("architecture", {})
            self.state.context["modules"] = input_data.get("modules", [])

        phases = [
            PMPhase.PROJECT_PLANNING,
            PMPhase.TASK_BREAKDOWN,
            PMPhase.RESOURCE_PLANNING,
            PMPhase.TASK_ASSIGNMENT,
        ]

        results = []
        for phase in phases:
            self.current_phase = phase
            phase_result = await self.step()
            results.append(phase_result)

            if self.state.error:
                break

        return {
            "project_name": self.project_name,
            "current_phase": self.current_phase.value,
            "project_plan": self.project_plan,
            "tasks": self.tasks,
            "resources": self.resources,
            "documents": self.documents,
            "workflow_results": results,
            "status": "completed" if self.current_phase == PMPhase.COMPLETED else "in_progress"
        }

    async def step(self) -> Any:
        """
        执行单个工作流步骤

        根据当前所处的阶段，执行对应的项目经理任务。
        """
        self.state.iteration += 1
        self.state.memory.append(f"Phase: {self.current_phase.value}")

        result = None

        if self.current_phase == PMPhase.PROJECT_PLANNING:
            result = await self._create_project_plan()
        elif self.current_phase == PMPhase.TASK_BREAKDOWN:
            result = await self._breakdown_tasks()
        elif self.current_phase == PMPhase.RESOURCE_PLANNING:
            result = await self._plan_resources()
        elif self.current_phase == PMPhase.TASK_ASSIGNMENT:
            result = await self._assign_tasks()
            self.current_phase = PMPhase.COMPLETED

        self.state.context["last_result"] = result
        return result

    # ==================== 工具注册 ====================

    def _register_default_tools(self) -> None:
        """自动注册默认工具"""
        # 导入默认工具模块
        from .default_tools import get_default_tool

        for tool_config in self.DEFAULT_TOOLS:
            tool_name = tool_config.get("name")

            # 如果工具不存在，则注册
            if tool_name and not self.tool_registry.get(tool_name):
                tool = get_default_tool(tool_name)
                if tool:
                    self.tool_registry.register(tool)

    # ==================== ReAct 工具调用 ====================

    async def _react_complete(self, prompt: str) -> str:
        """
        使用 ReAct 模式调用 LLM（可选择调用工具）

        思想：Thought → Action → Observe → Thought → ...

        Args:
            prompt: 提示词

        Returns:
            LLM 的回答
        """
        # 检查是否有可用工具
        has_tools = len(self.tool_registry.list_tools()) > 0

        if not has_tools:
            # 没有工具，直接调用 LLM
            return await self.llm_client.complete(prompt)

        # 有工具：使用 ReAct 循环
        messages = []

        system_prompt = f"""你是一个的项目经理助手，可以用工具来完成任务。

可用工具：
{self._format_tools()}

请按以下格式回复：
Thought: 你对情况的分析
Action: 要使用的工具名 (如果没有可用工具，使用 "llm")
Action Input: 工具输入
Observation: 工具返回结果

重复直到任务完成。"""

        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for i in range(self.max_react_iterations):
            # 调用 LLM
            response = await self.llm_client.complete_with_messages(messages)

            # 解析响应
            thought, action, action_input = self._parse_react_response(response)

            messages.append({"role": "assistant", "content": response})

            # 执行行动
            if action == "llm":
                return action_input
            else:
                observation = await self._execute_tool(action, action_input)
                messages.append({"role": "user", "content": f"Observation: {observation}"})

        # 达到最大迭代次数
        return "已达到最大迭代次数"

    def _format_tools(self) -> str:
        """格式化工具列表"""
        tool_names = self.tool_registry.list_tools()
        if not tool_names:
            return "无"

        lines = []
        for name in tool_names:
            tool = self.tool_registry.get(name)
            if tool:
                lines.append(f"- {tool.name}: {tool.description}")
        return "\n".join(lines)

    def _parse_react_response(self, response: str) -> tuple[str, str, str]:
        """解析 ReAct 响应"""
        thought = ""
        action = "llm"
        action_input = ""

        for line in response.split("\n"):
            if line.startswith("Thought:"):
                thought = line[8:].strip()
            elif line.startswith("Action:"):
                action = line[7:].strip().lower()
            elif line.startswith("Action Input:"):
                action_input = line[13:].strip()

        return thought, action, action_input

    async def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """执行工具"""
        tool = self.tool_registry.get(tool_name)
        if not tool:
            return f"错误: 工具 {tool_name} 不存在"

        try:
            import json
            try:
                params = json.loads(tool_input) if tool_input else {}
            except json.JSONDecodeError:
                params = {"input": tool_input}

            result = await tool.execute(**params)
            return str(result)
        except Exception as e:
            return f"工具执行错误: {str(e)}"

    # ==================== 项目管理方法 ====================

    async def _create_project_plan(self) -> dict[str, Any]:
        """
        创建项目计划

        制定项目里程碑、阶段计划和时间表。
        如果有 LLM 客户端，则调用 LLM 生成更智能的计划。
        """
        features = self.state.context.get("features", [])
        modules = self.state.context.get("modules", [])

        # 如果有 LLM，调用 LLM 生成项目计划
        if self.llm_client:
            prompt = f"""你是一个专业的项目经理。请为项目「{self.project_name}」制定详细的项目计划。

项目信息：
- 功能列表：{features}
- 模块列表：{modules}

请返回 JSON 格式的项目计划，包含：
1. overview: 项目概述，包含 project_name, estimated_duration, start_date, end_date
2. milestones: 里程碑数组，每个包含 id, name, description, target_date
3. phases: 阶段数组，每个包含 name, duration, start, end
4. risks: 风险数组，每个包含 name, impact, mitigation

重要：只返回纯 JSON，不要有任何解释、markdown 标记或思考过程。"""
            try:
                # 检查是否有可用工具
                if self.tool_registry.list_tools():
                    # 使用 ReAct 模式（可调用工具）
                    llm_result_str = await self._react_complete(prompt)
                    import json
                    try:
                        llm_result = json.loads(llm_result_str)
                    except json.JSONDecodeError:
                        # ReAct 模式返回的不是 JSON，降级到普通模式
                        llm_result = await self.llm_client.complete_json(prompt)
                else:
                    llm_result = await self.llm_client.complete_json(prompt)

                self.project_plan = llm_result
                return {
                    "phase": "Project Planning",
                    "document": "Project Plan",
                    "content": llm_result,
                    "source": "llm",
                    "next": "Task Breakdown"
                }
            except Exception as e:
                # LLM 调用失败，降级到模板
                logging.error(f"LLM 调用失败: {e}")
                pass

        # 模板模式：基于功能数量估算项目周期
        feature_count = len(features) if features else 5
        estimated_duration = max(4, feature_count * 2)  # 每周一个功能

        # 创建里程碑
        milestones = []
        milestone_names = ["需求确认", "设计完成", "开发完成", "测试完成", "上线发布"]
        start_date = datetime.now()

        for i, name in enumerate(milestone_names):
            milestone = {
                "id": f"MS-{i + 1:02d}",
                "name": name,
                "target_date": (start_date + timedelta(
                    weeks=estimated_duration * (i + 1) // len(milestone_names))).isoformat(),
                "status": "pending" if i > 0 else "completed",
                "description": f"项目{name}",
            }
            milestones.append(milestone)

        # 项目计划
        project_plan = {
            "title": f"{self.project_name} - 项目计划书",
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "overview": {
                "project_name": self.project_name,
                "estimated_duration": f"{estimated_duration}周",
                "start_date": start_date.isoformat(),
                "end_date": (start_date + timedelta(weeks=estimated_duration)).isoformat(),
            },
            "milestones": milestones,
            "phases": [
                {"name": "需求阶段", "duration": "1周", "start": 0, "end": 1},
                {"name": "设计阶段", "duration": "1周", "start": 1, "end": 2},
                {"name": "开发阶段", "duration": f"{estimated_duration - 3}周", "start": 2,
                 "end": estimated_duration - 1},
                {"name": "测试阶段", "duration": "1周", "start": estimated_duration - 1, "end": estimated_duration},
                {"name": "上线阶段", "duration": "1周", "start": estimated_duration, "end": estimated_duration + 1},
            ],
            "risks": [
                {"name": "需求变更", "impact": "高", "mitigation": "建立需求变更流程"},
                {"name": "技术难点", "impact": "中", "mitigation": "预留技术预研时间"},
                {"name": "人员流动", "impact": "中", "mitigation": "做好知识文档管理"},
            ],
        }

        self.project_plan = project_plan

        return {
            "phase": "Project Planning",
            "document": "Project Plan",
            "content": project_plan,
            "source": "template",
            "next": "Task Breakdown"
        }

    async def _breakdown_tasks(self) -> dict[str, Any]:
        """
        任务分解

        将项目分解为可执行的任务清单。
        如果有 LLM 客户端，则调用 LLM 生成更合理的任务分解。
        """
        features = self.state.context.get("features", [])
        modules = self.state.context.get("modules", ["用户模块", "业务模块", "报表模块"])

        # 如果有 LLM，调用 LLM 生成任务分解
        if self.llm_client:
            prompt = f"""你是一个专业的项目经理。请为项目「{self.project_name}」分解任务。

项目信息：
- 功能列表：{features}
- 模块列表：{modules}

请返回 JSON 格式，包含：
- tasks: 任务数组，每个包含 id, name, module, type, estimated_hours, priority, dependencies, status

重要：只返回纯 JSON，不要有任何解释、markdown 标记或思考过程。"""
            try:
                # 检查是否有可用工具
                if self.tool_registry.list_tools():
                    # 使用 ReAct 模式
                    llm_result_str = await self._react_complete(prompt)
                    import json
                    try:
                        llm_result = json.loads(llm_result_str)
                    except json.JSONDecodeError:
                        # 降级到普通模式
                        llm_result = await self.llm_client.complete_json(prompt)
                else:
                    llm_result = await self.llm_client.complete_json(prompt)

                tasks = llm_result.get("tasks", llm_result.get("task_list", []))

                # 添加状态字段
                for task in tasks:
                    task.setdefault("status", TaskStatus.PENDING.value)
                    task.setdefault("dependencies", [])
                    task.setdefault("assignee", "")
                    task.setdefault("created_at", datetime.now().isoformat())

                self.tasks = tasks
                return {
                    "phase": "Task Breakdown",
                    "total_tasks": len(tasks),
                    "tasks": tasks,
                    "source": "llm",
                    "next": "Resource Planning"
                }
            except Exception:
                pass

        # 模板模式：基于功能创建任务
        tasks = []
        task_id = 1

        # 基础设施任务
        tasks.extend([
            {"id": f"TASK-{task_id:03d}", "name": "开发环境搭建", "module": "基础设施", "type": "devops",
             "estimated_hours": 8, "priority": "high"},
            {"id": f"TASK-{task_id + 1:03d}", "name": "代码仓库初始化", "module": "基础设施", "type": "devops",
             "estimated_hours": 4, "priority": "high"},
            {"id": f"TASK-{task_id + 2:03d}", "name": "CI/CD流水线配置", "module": "基础设施", "type": "devops",
             "estimated_hours": 16, "priority": "medium"},
        ])
        task_id += 3

        # 后端任务
        tasks.extend([
            {"id": f"TASK-{task_id:03d}", "name": "数据库设计实现", "module": "后端", "type": "backend",
             "estimated_hours": 16, "priority": "high"},
            {"id": f"TASK-{task_id + 1:03d}", "name": "API框架搭建", "module": "后端", "type": "backend",
             "estimated_hours": 24, "priority": "high"},
        ])
        task_id += 2

        # 功能任务
        for i, feature in enumerate(features):
            tasks.append({
                "id": f"TASK-{task_id:03d}",
                "name": f"功能开发: {feature.get('name', f'功能{i + 1}')}",
                "module": feature.get("modules", ["业务模块"])[0] if feature.get("modules") else "业务模块",
                "type": "backend",
                "estimated_hours": feature.get("estimated_hours", 40),
                "priority": feature.get("priority", "medium"),
                "feature_id": feature.get("id", ""),
            })
            task_id += 1

        # 前端任务
        tasks.extend([
            {"id": f"TASK-{task_id:03d}", "name": "前端框架搭建", "module": "前端", "type": "frontend",
             "estimated_hours": 16, "priority": "high"},
            {"id": f"TASK-{task_id + 1:03d}", "name": "UI组件开发", "module": "前端", "type": "frontend",
             "estimated_hours": 40, "priority": "high"},
            {"id": f"TASK-{task_id + 2:03d}", "name": "页面集成", "module": "前端", "type": "frontend",
             "estimated_hours": 24, "priority": "medium"},
        ])
        task_id += 3

        # 测试任务
        tasks.extend([
            {"id": f"TASK-{task_id:03d}", "name": "单元测试编写", "module": "测试", "type": "testing",
             "estimated_hours": 24, "priority": "medium"},
            {"id": f"TASK-{task_id + 1:03d}", "name": "集成测试", "module": "测试", "type": "testing",
             "estimated_hours": 16, "priority": "medium"},
            {"id": f"TASK-{task_id + 2:03d}", "name": "性能测试", "module": "测试", "type": "testing",
             "estimated_hours": 8, "priority": "low"},
        ])

        # 添加状态
        for task in tasks:
            task["status"] = TaskStatus.PENDING.value
            task["dependencies"] = []
            task["assignee"] = ""
            task["created_at"] = datetime.now().isoformat()

        self.tasks = tasks

        return {
            "phase": "Task Breakdown",
            "total_tasks": len(tasks),
            "tasks": tasks,
            "source": "template",
            "next": "Resource Planning"
        }

    async def _plan_resources(self) -> dict[str, Any]:
        """
        资源规划

        估算工时、分配资源。
        """
        tasks = self.tasks

        # 计算总工时
        total_hours = sum(task.get("estimated_hours", 0) for task in tasks)

        # 按模块统计
        module_hours = {}
        for task in tasks:
            module = task.get("module", "其他")
            module_hours[module] = module_hours.get(module, 0) + task.get("estimated_hours", 0)

        # 按类型统计
        type_hours = {}
        for task in tasks:
            task_type = task.get("type", "其他")
            type_hours[task_type] = type_hours.get(task_type, 0) + task.get("estimated_hours", 0)

        # 资源分配
        resources = {
            "human_resources": [
                {"role": "后端开发", "count": 2, "hours": module_hours.get("后端", 80)},
                {"role": "前端开发", "count": 1, "hours": module_hours.get("前端", 80)},
                {"role": "测试工程师", "count": 1, "hours": module_hours.get("测试", 48)},
                {"role": "DevOps工程师", "count": 1, "hours": module_hours.get("基础设施", 28)},
            ],
            "infrastructure": {
                "开发服务器": "2核4G",
                "测试服务器": "2核4G",
                "数据库": "PostgreSQL 4核8G",
            },
            "budget": {
                "人力成本": total_hours * 100,  # 假设每小时100元
                "服务器成本": 2000,  # 月
                "其他成本": 5000,
            },
            "statistics": {
                "total_hours": total_hours,
                "total_days": total_hours // 8,
                "module_hours": module_hours,
                "type_hours": type_hours,
            }
        }

        self.resources = resources

        return {
            "phase": "Resource Planning",
            "document": "Resource Plan",
            "content": resources,
            "next": "Task Assignment"
        }

    async def _assign_tasks(self) -> dict[str, Any]:
        """
        任务分配

        将任务分配给团队成员，设置优先级和截止日期。
        """
        tasks = self.tasks

        # 默认团队成员
        team_members = [
            {"name": "张三", "role": "后端开发", "capacity": 40},
            {"name": "李四", "role": "后端开发", "capacity": 40},
            {"name": "王五", "role": "前端开发", "capacity": 40},
            {"name": "赵六", "role": "测试工程师", "capacity": 40},
        ]

        # 简单分配策略：按角色分配
        role_assignments = {
            "后端": "张三",
            "前端": "王五",
            "测试": "赵六",
            "基础设施": "李四",
            "其他": "张三",
        }

        # 设置任务分配
        start_date = datetime.now()
        for i, task in enumerate(tasks):
            module = task.get("module", "其他")
            task["assignee"] = role_assignments.get(module, "张三")
            # 简单设置截止日期：按任务顺序
            task["due_date"] = (start_date + timedelta(days=i + 1)).isoformat()

        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks.sort(key=lambda t: priority_order.get(t.get("priority", "medium"), 1))

        self.tasks = tasks

        assignment_doc = {
            "title": f"{self.project_name} - 任务分配表",
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "team_members": team_members,
            "assignments": tasks,
            "summary": {
                "total_tasks": len(tasks),
                "assigned_tasks": len([t for t in tasks if t.get("assignee")]),
                "high_priority": len([t for t in tasks if t.get("priority") == "high"]),
                "by_assignee": {
                    member["name"]: len([t for t in tasks if t.get("assignee") == member["name"]])
                    for member in team_members
                }
            }
        }

        self.documents["task_assignment"] = assignment_doc

        return {
            "phase": "Task Assignment",
            "document": "Task Assignment",
            "content": assignment_doc,
            "workflow_status": "completed"
        }

    def get_current_phase(self) -> str:
        """获取当前工作流阶段"""
        return self.current_phase.value

    def get_project_plan(self) -> dict[str, Any]:
        """获取项目计划"""
        return self.project_plan.copy()

    def get_tasks(self) -> list[dict[str, Any]]:
        """获取任务列表"""
        return self.tasks.copy()

    def get_resources(self) -> dict[str, Any]:
        """获取资源分配"""
        return self.resources.copy()

    def get_task_by_id(self, task_id: str) -> dict[str, Any] | None:
        """根据ID获取任务"""
        for task in self.tasks:
            if task.get("id") == task_id:
                return task
        return None

    def update_task_status(self, task_id: str, status: str) -> bool:
        """更新任务状态"""
        task = self.get_task_by_id(task_id)
        if task:
            task["status"] = status
            task["updated_at"] = datetime.now().isoformat()
            return True
        return False
