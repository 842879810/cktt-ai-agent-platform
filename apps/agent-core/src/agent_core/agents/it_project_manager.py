"""
IT项目管理智能体模块

本模块实现了IT项目全生命周期文档管理智能体，自动化管理IT项目从需求到任务下发的完整流程。

主要功能：
1. PRD（产品需求文档）创建 - 生成结构化的需求文档
2. PRD评审 - 模拟需求评审流程，记录评审意见
3. HLD（概要设计文档） - 系统架构、模块、数据库、接口设计
4. LLD（详细设计文档） - 模块详细设计、算法设计、错误处理
5. 任务下发 - 根据设计文档自动生成开发任务清单

工作流程：
    PRD创建 -> PRD评审 -> 概要设计 -> 详细设计 -> 任务下发

使用示例：
    from agent_core.agents import ITProjectManagerAgent, AgentConfig

    config = AgentConfig(name="it-pm", description="IT项目文档管理")
    agent = ITProjectManagerAgent(config, project_name="ERP系统")
    result = await agent.run({"project_name": "ERP系统", "project_info": {...}})
"""

from datetime import datetime
from enum import StrEnum
from typing import Any

from .base import AgentConfig, BaseAgent


class ProjectPhase(StrEnum):
    """
    IT项目阶段枚举

    定义IT项目管理的各个阶段，每个阶段对应不同的文档产出。
    智能体会按顺序执行各个阶段的任务。

    阶段说明：
    - PRD: 产品需求文档阶段，收集和分析用户需求
    - PRD_REVIEW: PRD评审阶段，组织需求评审会议
    - HLD: 概要设计阶段，进行系统架构设计
    - LLD: 详细设计阶段，进行具体的模块设计
    - TASK_ASSIGNMENT: 任务下发阶段，分解任务并分配
    - COMPLETED: 工作流程完成
    """

    PRD = "prd"                    # 产品需求文档 (Product Requirements Document)
    PRD_REVIEW = "prd_review"      # PRD评审阶段
    HLD = "hld"                    # 概要设计 (High-Level Design)
    LLD = "lld"                    # 详细设计 (Low-Level Design)
    TASK_ASSIGNMENT = "task_assignment"  # 任务下发
    COMPLETED = "completed"         # 完成


class DocumentStatus(StrEnum):
    """
    文档状态枚举

    定义文档在不同生命周期阶段的状态。
    用于追踪每个文档的当前状态。

    状态说明：
    - DRAFT: 草稿状态，文档正在编写中
    - REVIEWING: 评审中，文档正在接受评审
    - APPROVED: 已通过，文档通过评审
    - REJECTED: 已驳回，文档未通过评审需要修改
    """

    DRAFT = "draft"        # 草稿
    REVIEWING = "reviewing"  # 评审中
    APPROVED = "approved"    # 已通过
    REJECTED = "rejected"   # 已驳回


class ITProjectManagerAgent(BaseAgent):
    """
    IT项目管理智能体

    自动化管理IT项目全生命周期的文档工作流程。
    从需求收集开始，经过设计阶段，最终生成可执行的任务清单。

    主要功能：
    1. 自动生成结构化的PRD文档
    2. 模拟需求评审流程并记录评审意见
    3. 生成系统概要设计文档(HLD)
    4. 生成详细设计文档(LLD)
    5. 根据设计文档自动生成开发任务清单

    文档产出：
    - PRD: 产品需求文档，包含项目概述、用户需求、功能需求、非功能需求
    - HLD: 概要设计文档，包含系统架构、模块设计、数据库设计、接口设计
    - LLD: 详细设计文档，包含模块详细设计、算法设计、错误处理
    - 任务清单: 包含任务名称、模块、预估工时、状态等信息

    使用方式：
    1. 创建智能体实例，指定项目名称
    2. 调用run方法，传入项目相关信息
    3. 获取生成的文档和任务清单
    """

    def __init__(self, config: AgentConfig, project_name: str = ""):
        """
        初始化IT项目管理智能体

        Args:
            config: 智能体配置对象
            project_name: 项目名称，用于生成文档标题和任务ID
        """
        super().__init__(config)
        self.project_name = project_name  # 项目名称
        self.current_phase = ProjectPhase.PRD  # 当前阶段，默认从PRD开始
        self.documents: dict[str, Any] = {}  # 文档存储字典
        self.tasks: list[dict[str, Any]] = []  # 任务列表

    async def run(self, input_data: Any) -> Any:
        """
        运行IT项目管理智能体的主入口

        执行完整的工作流程，按顺序执行各个阶段的文档生成任务。
        流程顺序：PRD创建 -> PRD评审 -> 概要设计 -> 详细设计 -> 任务下发

        Args:
            input_data: 输入数据字典，应包含：
                - project_name: 项目名称
                - project_info: 项目信息字典（可选）

        Returns:
            包含以下键的字典：
                - project_name: 项目名称
                - current_phase: 当前阶段
                - documents: 生成的文档字典
                - tasks: 生成的任务列表
                - workflow_results: 各阶段执行结果
                - status: 工作流状态
        """
        self.reset()  # 重置智能体状态

        # 初始化项目上下文
        # 从输入数据中提取项目名称，存储到状态上下文中
        if isinstance(input_data, dict):
            self.project_name = input_data.get("project_name", "Untitled Project")
            # 将项目信息也存入上下文，供各阶段使用
            self.state.context["project_name"] = self.project_name
            self.state.context["project_info"] = input_data.get("project_info", {})

        # 定义工作流程的阶段顺序
        # IT项目管理遵循标准的瀑布流开发模式
        phases = [
            ProjectPhase.PRD,              # 1. 产品需求文档
            ProjectPhase.PRD_REVIEW,       # 2. PRD评审
            ProjectPhase.HLD,              # 3. 概要设计
            ProjectPhase.LLD,              # 4. 详细设计
            ProjectPhase.TASK_ASSIGNMENT, # 5. 任务下发
        ]

        results = []  # 存储各阶段的执行结果
        for phase in phases:
            self.current_phase = phase  # 设置当前阶段
            phase_result = await self.step()  # 执行当前阶段
            results.append(phase_result)  # 记录执行结果

            # 如果发生错误，提前终止工作流程
            if self.state.error:
                break

        # 返回完整的工作流程结果
        return {
            "project_name": self.project_name,
            "current_phase": self.current_phase.value,
            "documents": self.documents,
            "tasks": self.tasks,
            "workflow_results": results,
            "status": "completed" if self.current_phase == ProjectPhase.COMPLETED else "in_progress"
        }

    async def step(self) -> Any:
        """
        执行单个工作流步骤

        根据当前所处的阶段，执行对应的文档生成任务。
        每次调用此方法会推进智能体到一个新的状态。

        Returns:
            当前阶段的执行结果字典，包含阶段名称、文档内容、下一步等信息
        """
        self.state.iteration += 1  # 增加迭代计数
        self.state.memory.append(f"Phase: {self.current_phase.value}")  # 记录当前阶段到记忆

        result = None  # 初始化结果

        # 根据当前阶段执行对应的任务
        if self.current_phase == ProjectPhase.PRD:
            # 阶段1：创建产品需求文档
            result = await self._create_prd()
        elif self.current_phase == ProjectPhase.PRD_REVIEW:
            # 阶段2：评审产品需求文档
            result = await self._review_prd()
        elif self.current_phase == ProjectPhase.HLD:
            # 阶段3：创建概要设计文档
            result = await self._create_hld()
        elif self.current_phase == ProjectPhase.LLD:
            # 阶段4：创建详细设计文档
            result = await self._create_lld()
        elif self.current_phase == ProjectPhase.TASK_ASSIGNMENT:
            # 阶段5：生成并下发开发任务
            result = await self._assign_tasks()
            self.current_phase = ProjectPhase.COMPLETED  # 标记工作流完成

        # 将结果存入上下文，以便后续阶段使用
        self.state.context["last_result"] = result
        return result

    async def _create_prd(self) -> dict[str, Any]:
        """
        创建产品需求文档（PRD）

        根据项目信息生成结构化的产品需求文档。
        PRD是整个项目的基础，定义了项目要做什么。

        文档结构：
        1. 项目概述 - 项目背景、目标、适用范围
        2. 用户需求 - 用户角色、用户故事
        3. 功能需求 - 核心功能、扩展功能
        4. 非功能需求 - 性能、安全、兼容性
        5. 验收标准 - 如何判断项目完成

        Returns:
            包含PRD内容的字典，包括版本、创建时间、各章节内容等
        """
        # 从上下文中获取项目信息
        project_info = self.state.context.get("project_info", {})

        # 构建PRD文档内容
        # 使用项目信息填充各章节，如果没有则使用默认值"待填写"
        prd_content = {
            "title": f"{self.project_name} - 产品需求文档",  # 文档标题
            "version": "1.0.0",  # 初始版本号
            "created_at": datetime.now().isoformat(),  # 创建时间
            "author": project_info.get("author", "System"),  # 文档作者
            "sections": {
                # 第一章：项目概述
                "1. 项目概述": {
                    "1.1 项目背景": project_info.get("background", "待填写"),
                    "1.2 项目目标": project_info.get("goals", "待填写"),
                    "1.3 适用范围": project_info.get("scope", "待填写"),
                },
                # 第二章：用户需求
                "2. 用户需求": {
                    "2.1 用户角色": project_info.get("user_roles", []),
                    "2.2 用户故事": project_info.get("user_stories", []),
                },
                # 第三章：功能需求
                "3. 功能需求": {
                    "3.1 核心功能": project_info.get("core_features", []),
                    "3.2 扩展功能": project_info.get("extended_features", []),
                },
                # 第四章：非功能需求
                "4. 非功能需求": {
                    "4.1 性能要求": project_info.get("performance", "待填写"),
                    "4.2 安全要求": project_info.get("security", "待填写"),
                    "4.3 兼容性要求": project_info.get("compatibility", "待填写"),
                },
                # 第五章：验收标准
                "5. 验收标准": project_info.get("acceptance_criteria", "待填写"),
            },
            "status": DocumentStatus.DRAFT.value,  # 初始状态为草稿
        }

        # 将PRD存入文档字典
        self.documents["prd"] = prd_content

        # 返回执行结果
        return {
            "phase": "PRD Creation",
            "document": "Product Requirements Document",
            "content": prd_content,
            "next": "PRD Review"
        }

    async def _review_prd(self) -> dict[str, Any]:
        """
        评审产品需求文档（PRD Review）

        模拟需求评审流程，对PRD进行评审并记录评审意见。
        评审是保证需求质量的重要环节。

        评审内容包括：
        - 需求描述的清晰度和完整性
        - 功能边界的明确性
        - 性能指标的量化程度

        Returns:
            包含评审结果的字典，包括评审人、评审时间、意见、决策等
        """
        # 获取之前创建的PRD文档
        prd = self.documents.get("prd", {})
        # 更新文档状态为评审中
        prd["status"] = DocumentStatus.REVIEWING.value

        # 模拟评审过程
        # 在实际应用中，这里可以接入LLM进行自动化评审
        review_result = {
            "reviewer": "Review Committee",  # 评审委员会
            "reviewed_at": datetime.now().isoformat(),  # 评审时间
            "comments": [
                "需求描述清晰",  # 正面意见
                "功能边界需要进一步明确",  # 改进建议
                "性能指标需要量化"  # 改进建议
            ],
            "decision": DocumentStatus.APPROVED.value,  # 评审决策：通过
        }

        # 将评审结果关联到PRD文档
        prd["review"] = review_result

        # 返回评审结果
        return {
            "phase": "PRD Review",
            "document": "Product Requirements Document",
            "review_result": review_result,
            "next": "High-Level Design"
        }

    async def _create_hld(self) -> dict[str, Any]:
        """
        创建概要设计文档（HLD）

        基于PRD生成系统概要设计文档。
        HLD定义系统的整体架构和技术选型。

        文档结构：
        1. 系统架构 - 架构概述、技术栈
        2. 模块设计 - 模块划分、模块职责
        3. 数据库设计 - ER图、表结构
        4. 接口设计 - API列表、接口规范
        5. 安全设计 - 认证、授权

        Returns:
            包含HLD内容的字典
        """
        # 构建HLD文档内容
        hld_content = {
            "title": f"{self.project_name} - 概要设计文档",
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "based_on": "PRD v1.0.0",  # 基于的PRD版本
            "sections": {
                "1. 系统架构": {
                    "1.1 架构概述": "采用微服务/单体架构",
                    "1.2 技术栈": {
                        "前端": "待确定",
                        "后端": "待确定",
                        "数据库": "待确定",
                    },
                },
                "2. 模块设计": {
                    "2.1 模块划分": [],  # 待填充
                    "2.2 模块职责": {},  # 待填充
                },
                "3. 数据库设计": {
                    "3.1 ER图": "待绘制",
                    "3.2 表结构": [],  # 待填充
                },
                "4. 接口设计": {
                    "4.1 API列表": [],  # 待填充
                    "4.2 接口规范": "RESTful API",
                },
                "5. 安全设计": {
                    "5.1 认证": "JWT/Session",
                    "5.2 授权": "RBAC",
                },
            },
            "status": DocumentStatus.DRAFT.value,
        }

        self.documents["hld"] = hld_content

        return {
            "phase": "High-Level Design",
            "document": "High-Level Design Document",
            "content": hld_content,
            "next": "Low-Level Design"
        }

    async def _create_lld(self) -> dict[str, Any]:
        """
        创建详细设计文档（LLD）

        基于HLD生成详细的实现设计文档。
        LLD指导具体的编码实现工作。

        文档结构：
        1. 模块详细设计 - 类图、时序图、核心方法
        2. 数据库详细设计 - 表结构详情、索引、优化策略
        3. 接口详细设计 - 接口详情、请求响应示例
        4. 算法设计 - 核心算法、复杂度分析
        5. 错误处理 - 异常类型、错误码定义

        Returns:
            包含LLD内容的字典
        """
        lld_content = {
            "title": f"{self.project_name} - 详细设计文档",
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "based_on": "HLD v1.0.0",  # 基于的HLD版本
            "sections": {
                "1. 模块详细设计": {
                    "1.1 模块A": {
                        "类图": "待绘制",
                        "时序图": "待绘制",
                        "核心方法": [],  # 待填充
                    },
                },
                "2. 数据库详细设计": {
                    "2.1 表结构详情": [],  # 待填充
                    "2.2 索引设计": [],  # 待填充
                    "2.3 优化策略": "",  # 待填充
                },
                "3. 接口详细设计": {
                    "3.1 接口详情": [],  # 待填充
                    "3.2 请求/响应示例": {},  # 待填充
                },
                "4. 算法设计": {
                    "4.1 核心算法": [],  # 待填充
                    "4.2 复杂度分析": "",  # 待填充
                },
                "5. 错误处理": {
                    "5.1 异常类型": [],  # 待填充
                    "5.2 错误码定义": {},  # 待填充
                },
            },
            "status": DocumentStatus.DRAFT.value,
        }

        self.documents["lld"] = lld_content

        return {
            "phase": "Low-Level Design",
            "document": "Low-Level Design Document",
            "content": lld_content,
            "next": "Task Assignment"
        }

    async def _assign_tasks(self) -> dict[str, Any]:
        """
        生成并下发开发任务

        基于详细设计文档，生成可执行的开发任务清单。
        每个任务包含任务ID、名称、模块、预估工时等信息。

        生成的任务类型：
        - 数据库相关：表创建、索引优化
        - 后端开发：API开发、业务逻辑实现
        - 前端开发：页面开发、组件实现
        - 测试：单元测试、集成测试
        - 文档：用户手册、开发文档

        Returns:
            包含任务列表和统计信息的字典
        """
        # 定义标准开发任务模板
        # 这些任务覆盖了软件开发的主要环节
        task_templates = [
            {"name": "数据库表创建", "estimated_hours": 8, "module": "Database"},
            {"name": "后端API开发", "estimated_hours": 40, "module": "Backend"},
            {"name": "前端页面开发", "estimated_hours": 40, "module": "Frontend"},
            {"name": "单元测试编写", "estimated_hours": 16, "module": "Testing"},
            {"name": "集成测试", "estimated_hours": 16, "module": "Testing"},
            {"name": "文档编写", "estimated_hours": 8, "module": "Documentation"},
        ]

        # 遍历模板生成具体任务
        for i, task_template in enumerate(task_templates):
            task = {
                # 任务ID格式：TASK-{项目简称}-{序号}
                "task_id": f"TASK-{self.project_name[:3].upper()}-{i+1:03d}",
                "name": task_template["name"],  # 任务名称
                "module": task_template["module"],  # 所属模块
                "estimated_hours": task_template["estimated_hours"],  # 预估工时
                "status": "pending",  # 初始状态为待开始
                "assignee": "",  # 暂未分配
                "dependencies": [],  # 暂无依赖
                "created_at": datetime.now().isoformat(),  # 创建时间
            }
            self.tasks.append(task)

        # 返回任务生成结果
        return {
            "phase": "Task Assignment",
            "total_tasks": len(self.tasks),  # 总任务数
            "tasks": self.tasks,  # 任务列表
            "workflow_status": "completed"  # 工作流完成
        }

    def get_current_phase(self) -> str:
        """
        获取当前工作流阶段

        Returns:
            当前阶段的字符串标识
        """
        return self.current_phase.value

    def get_document(self, doc_type: str) -> dict[str, Any] | None:
        """
        获取指定类型的文档

        Args:
            doc_type: 文档类型，如"prd"、"hld"、"lld"

        Returns:
            文档内容字典，如果不存在则返回None
        """
        return self.documents.get(doc_type)

    def get_tasks(self) -> list[dict[str, Any]]:
        """
        获取所有生成的任务

        Returns:
            任务列表的副本
        """
        return self.tasks.copy()
