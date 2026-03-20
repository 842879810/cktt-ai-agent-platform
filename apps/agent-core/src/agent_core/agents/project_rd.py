"""
项目研发流程智能体模块

本模块实现了项目研发目录结构创建智能体，自动化创建项目的目录结构和基础代码模板。

主要功能：
1. 项目初始化 - 创建项目元数据
2. 目录创建 - 生成标准化的项目目录结构
3. 配置设置 - 生成配置文件（.gitignore, requirements.txt等）
4. 模板生成 - 生成基础的Python代码模板

工作流程：
    项目初始化 -> 目录创建 -> 配置设置 -> 模板生成

注意：
    此智能体仅创建目录结构和基础模板，不包含实际的业务代码实现。
    实际的代码开发需要由开发人员完成。

使用示例：
    from agent_core.agents import ProjectRDAgent, AgentConfig

    config = AgentConfig(name="project-rd", description="项目研发目录创建")
    agent = ProjectRDAgent(config, project_name="MyProject", base_path="./projects")
    result = await agent.run({"project_name": "MyProject", "base_path": "./projects"})
"""

from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from .base import AgentConfig, BaseAgent


class RDPhase(StrEnum):
    """
    项目研发阶段枚举

    定义项目研发的各个阶段，每个阶段对应不同的工作内容。

    阶段说明：
    - PROJECT_INIT: 项目初始化，创建项目元数据
    - DIRECTORY_CREATION: 目录创建，生成项目目录结构
    - CONFIG_SETUP: 配置设置，生成配置文件
    - TEMPLATE_GENERATION: 模板生成，生成代码模板
    - COMPLETED: 完成
    """

    PROJECT_INIT = "project_init"          # 项目初始化
    DIRECTORY_CREATION = "directory_creation"  # 目录创建
    CONFIG_SETUP = "config_setup"        # 配置设置
    TEMPLATE_GENERATION = "template_generation"  # 模板生成
    COMPLETED = "completed"             # 完成


class ProjectRDAgent(BaseAgent):
    """
    项目研发流程智能体

    自动化创建项目的目录结构和基础代码模板。
    生成的目录结构遵循Python项目的最佳实践。

    主要功能：
    1. 自动创建标准化的项目目录结构
    2. 生成常用的配置文件（.gitignore, requirements.txt等）
    3. 生成基础的Python代码模板
    4. 创建测试目录和文档目录

    创建的目录结构：
    - src/: 源代码目录
    - tests/: 测试文件目录
    - docs/: 文档目录
    - config/: 配置文件目录
    - scripts/: 脚本目录
    - logs/: 日志目录（可选）
    - data/: 数据目录（可选）

    使用方式：
    1. 创建智能体实例，指定项目名称和基础路径
    2. 调用run方法
    3. 获取创建的目录和文件列表
    """

    def __init__(self, config: AgentConfig, project_name: str = "", base_path: str = ""):
        """
        初始化项目研发智能体

        Args:
            config: 智能体配置对象
            project_name: 项目名称，用于创建目录和生成模板
            base_path: 基础路径，项目的创建位置，默认为当前目录
        """
        super().__init__(config)
        self.project_name = project_name  # 项目名称
        # 将基础路径转换为Path对象，便于后续处理
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.created_directories: list[str] = []  # 已创建的目录列表
        self.created_files: list[str] = []  # 已创建的文件列表

    async def run(self, input_data: Any) -> Any:
        """
        运行项目研发智能体的主入口

        执行完整的工作流程，按顺序执行各个阶段的任务。
        流程顺序：项目初始化 -> 目录创建 -> 配置设置 -> 模板生成

        Args:
            input_data: 输入数据字典，应包含：
                - project_name: 项目名称
                - base_path: 项目基础路径（可选）

        Returns:
            包含以下键的字典：
                - project_name: 项目名称
                - base_path: 基础路径
                - created_directories: 创建的目录列表
                - created_files: 创建的文件列表
                - workflow_results: 各阶段执行结果
                - status: 工作流状态
        """
        self.reset()  # 重置智能体状态

        # 初始化项目上下文
        # 从输入数据中提取项目名称和基础路径
        if isinstance(input_data, dict):
            self.project_name = input_data.get("project_name", "UntitledProject")
            # 解析基础路径，默认为当前目录
            self.base_path = Path(input_data.get("base_path", str(Path.cwd())))

        # 将项目信息存入上下文
        self.state.context["project_name"] = self.project_name
        self.state.context["base_path"] = str(self.base_path)

        # 定义工作流程的阶段顺序
        phases = [
            RDPhase.PROJECT_INIT,         # 1. 项目初始化
            RDPhase.DIRECTORY_CREATION,   # 2. 目录创建
            RDPhase.CONFIG_SETUP,         # 3. 配置设置
            RDPhase.TEMPLATE_GENERATION, # 4. 模板生成
        ]

        results = []  # 存储各阶段的执行结果
        for phase in phases:
            self.state.iteration = phases.index(phase)  # 设置迭代计数
            phase_result = await self.step(phase)  # 执行当前阶段
            results.append(phase_result)  # 记录执行结果

            # 如果发生错误，提前终止工作流程
            if self.state.error:
                break

        # 返回完整的工作流程结果
        return {
            "project_name": self.project_name,
            "base_path": str(self.base_path),
            "created_directories": self.created_directories,
            "created_files": self.created_files,
            "workflow_results": results,
            "status": "completed"
        }

    async def step(self, phase: RDPhase = None) -> Any:
        """
        执行单个工作流步骤

        根据当前所处的阶段，执行对应的任务。
        每次调用此方法会推进智能体到一个新的状态。

        Args:
            phase: 要执行的阶段，默认为项目初始化阶段

        Returns:
            当前阶段的执行结果字典
        """
        # 如果未指定阶段，默认使用项目初始化阶段
        phase = phase or RDPhase.PROJECT_INIT
        self.state.memory.append(f"Phase: {phase.value}")  # 记录当前阶段到记忆

        result = None  # 初始化结果

        # 根据当前阶段执行对应的任务
        if phase == RDPhase.PROJECT_INIT:
            # 阶段1：项目初始化
            result = await self._init_project()
        elif phase == RDPhase.DIRECTORY_CREATION:
            # 阶段2：创建目录结构
            result = await self._create_directories()
        elif phase == RDPhase.CONFIG_SETUP:
            # 阶段3：设置配置文件
            result = await self._setup_configs()
        elif phase == RDPhase.TEMPLATE_GENERATION:
            # 阶段4：生成代码模板
            result = await self._generate_templates()
            phase = RDPhase.COMPLETED  # 标记工作流完成

        # 将结果存入上下文，以便后续使用
        self.state.context["last_result"] = result
        return result

    async def _init_project(self) -> dict[str, Any]:
        """
        项目初始化

        创建项目的元数据信息，包括项目名称、创建时间、项目类型和初始版本号。
        这些信息将用于后续的文件生成。

        Returns:
            包含项目元数据的字典
        """
        # 构建项目信息字典
        project_info = {
            "project_name": self.project_name,  # 项目名称
            "created_at": datetime.now().isoformat(),  # 创建时间
            "project_type": "general",  # 项目类型
            "version": "0.1.0",  # 初始版本号
        }

        # 将项目信息存入上下文，供后续阶段使用
        self.state.context["project_info"] = project_info

        # 返回初始化结果
        return {
            "phase": "Project Initialization",
            "project_info": project_info,
            "status": "initialized"
        }

    async def _create_directories(self) -> dict[str, Any]:
        """
        创建项目目录结构

        基于Python项目的最佳实践，创建标准化的项目目录结构。
        目录结构遵循常见的项目布局约定。

        创建的目录：
        - src/: 源代码主目录
        - src/{project_name}/: 项目包目录
        - src/{project_name}/modules/: 功能模块目录
        - src/{project_name}/utils/: 工具类目录
        - src/{project_name}/models/: 数据模型目录
        - tests/: 测试目录
        - tests/unit/: 单元测试目录
        - tests/integration/: 集成测试目录
        - tests/fixtures/: 测试数据目录
        - docs/: 文档目录
        - docs/api/: API文档目录
        - docs/guide/: 用户指南目录
        - docs/dev/: 开发文档目录
        - config/: 配置目录
        - config/dev/: 开发环境配置
        - config/prod/: 生产环境配置
        - scripts/: 脚本目录
        - scripts/dev/: 开发脚本
        - scripts/deploy/: 部署脚本
        - logs/: 日志目录
        - data/: 数据目录
        - data/raw/: 原始数据
        - data/processed/: 处理后数据
        - notebooks/: Jupyter notebooks
        - .github/: GitHub配置
        - .github/workflows/: CI/CD工作流

        Returns:
            包含创建结果和目录列表的字典
        """
        # 计算项目根目录的完整路径
        project_root = self.base_path / self.project_name

        # 定义标准目录结构
        # 使用占位符{project_name}，后续会替换为实际的项目名
        directory_structure = [
            "src",                                        # 源代码目录
            "src/{project_name}",                        # 项目主包
            "src/{project_name}/modules",               # 功能模块
            "src/{project_name}/utils",                 # 工具类
            "src/{project_name}/models",                # 数据模型
            "tests",                                     # 测试目录
            "tests/unit",                               # 单元测试
            "tests/integration",                        # 集成测试
            "tests/fixtures",                           # 测试数据
            "docs",                                     # 文档目录
            "docs/api",                                # API文档
            "docs/guide",                              # 用户指南
            "docs/dev",                               # 开发文档
            "config",                                   # 配置目录
            "config/dev",                              # 开发配置
            "config/prod",                             # 生产配置
            "scripts",                                  # 脚本目录
            "scripts/dev",                             # 开发脚本
            "scripts/deploy",                          # 部署脚本
            "logs",                                     # 日志目录
            "data",                                     # 数据目录
            "data/raw",                                # 原始数据
            "data/processed",                          # 处理后数据
            "notebooks",                               # Jupyter notebooks
            ".github",                                 # GitHub配置
            ".github/workflows",                       # CI/CD工作流
        ]

        created = []  # 存储已创建的目录
        # 遍历目录结构，创建每个目录
        for dir_path in directory_structure:
            # 将占位符替换为实际的项目名称
            # 转换为小写并替换连字符为下划线，符合Python包命名规范
            full_path = project_root / dir_path.replace(
                "{project_name}",
                self.project_name.lower().replace("-", "_")
            )

            try:
                # 创建目录，parents=True表示创建所有父目录
                # exist_ok=True表示如果目录已存在不报错
                full_path.mkdir(parents=True, exist_ok=True)
                # 记录相对路径
                created.append(str(full_path.relative_to(project_root)))
                # 记录完整路径
                self.created_directories.append(str(full_path))
            except Exception as e:
                # 发生错误时记录到状态中
                self.state.error = str(e)

        # 返回目录创建结果
        return {
            "phase": "Directory Creation",
            "project_root": str(project_root),
            "directories_created": len(created),
            "directory_list": created,
            "status": "completed"
        }

    async def _setup_configs(self) -> dict[str, Any]:
        """
        设置配置文件

        生成项目所需的各种配置文件，包括版本控制、依赖管理、环境配置等。

        创建的配置文件：
        - .gitignore: Git忽略规则
        - README.md: 项目说明文档
        - requirements.txt: Python依赖列表
        - setup.py: Python包安装配置
        - config/dev.yaml: 开发环境配置
        - config/prod.yaml: 生产环境配置
        - .env.example: 环境变量模板

        Returns:
            包含创建结果和文件列表的字典
        """
        # 计算项目根目录
        project_root = self.base_path / self.project_name

        # 定义要创建的配置文件列表
        # 每个配置文件包含路径和内容
        config_files = [
            {
                "path": ".gitignore",  # Git忽略文件
                "content": self._get_gitignore_template(),
            },
            {
                "path": "README.md",  # 项目说明文档
                "content": self._get_readme_template(),
            },
            {
                "path": "requirements.txt",  # Python依赖
                "content": self._get_requirements_template(),
            },
            {
                "path": "setup.py",  # 包安装脚本
                "content": self._get_setup_template(),
            },
            {
                "path": "config/dev.yaml",  # 开发环境配置
                "content": self._get_config_template("dev"),
            },
            {
                "path": "config/prod.yaml",  # 生产环境配置
                "content": self._get_config_template("prod"),
            },
            {
                "path": ".env.example",  # 环境变量模板
                "content": self._get_env_template(),
            },
        ]

        created_files = []  # 存储已创建的文件
        # 遍历配置文件列表，创建每个文件
        for config_file in config_files:
            file_path = project_root / config_file["path"]

            try:
                # 确保父目录存在
                file_path.parent.mkdir(parents=True, exist_ok=True)
                # 写入文件内容
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(config_file["content"])
                # 记录已创建的文件
                created_files.append(config_file["path"])
                self.created_files.append(str(file_path))
            except Exception as e:
                # 发生错误时记录到状态中
                self.state.error = str(e)

        # 返回配置文件创建结果
        return {
            "phase": "Config Setup",
            "files_created": len(created_files),
            "file_list": created_files,
            "status": "completed"
        }

    async def _generate_templates(self) -> dict[str, Any]:
        """
        生成代码模板

        生成项目所需的基础Python代码模板，帮助开发者快速开始编码工作。

        创建的模板文件：
        - src/{project}/__init__.py: 包初始化文件
        - src/{project}/__main__.py: 程序入口文件
        - src/{project}/config.py: 配置类模板
        - tests/__init__.py: 测试包初始化
        - tests/unit/__init__.py: 单元测试包初始化
        - tests/integration/__init__.py: 集成测试包初始化
        - docs/index.md: 文档首页

        Returns:
            包含创建结果和模板列表的字典
        """
        # 计算项目根目录
        project_root = self.base_path / self.project_name
        # 处理项目名称，转换为Python包名（无连字符）
        project_name_safe = self.project_name.lower().replace("-", "_")

        # 定义要创建的代码模板列表
        templates = [
            {
                # 包初始化文件
                "path": f"src/{project_name_safe}/__init__.py",
                "content": f'""" {self.project_name} - Main package. """\n\n__version__ = "0.1.0"\n',
            },
            {
                # 程序入口文件
                "path": f"src/{project_name_safe}/__main__.py",
                "content": f'"""Main entry point for {self.project_name}. """\n\ndef main():\n    print("Hello from {self.project_name}!")\n\nif __name__ == "__main__":\n    main()\n',
            },
            {
                # 配置类模板
                "path": f"src/{project_name_safe}/config.py",
                "content": f'"""Configuration for {self.project_name}. """\n\nfrom pathlib import Path\n\nBASE_DIR = Path(__file__).parent\n\nclass Config:\n    """Application configuration."""\n\n    DEBUG = True\n    VERSION = "0.1.0"\n\n    # Add your config here\n',
            },
            # 测试包初始化文件
            {"path": "tests/__init__.py", "content": ""},
            {"path": "tests/unit/__init__.py", "content": ""},
            {"path": "tests/integration/__init__.py", "content": ""},
            # 文档首页
            {"path": "docs/index.md", "content": f"# {self.project_name}\n\nProject documentation.\n"},
        ]

        created_templates = []  # 存储已创建的模板
        # 遍历模板列表，创建每个文件
        for template in templates:
            file_path = project_root / template["path"]

            try:
                # 确保父目录存在
                file_path.parent.mkdir(parents=True, exist_ok=True)
                # 写入模板内容
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(template["content"])
                # 记录已创建的模板
                created_templates.append(template["path"])
                self.created_files.append(str(file_path))
            except Exception as e:
                # 发生错误时记录到状态中
                self.state.error = str(e)

        # 返回模板生成结果
        return {
            "phase": "Template Generation",
            "templates_created": len(created_templates),
            "template_list": created_templates,
            "status": "completed"
        }

    def _get_gitignore_template(self) -> str:
        """
        获取.gitignore模板内容

        Returns:
            .gitignore文件的标准内容
        """
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
.env.local

# Logs
*.log
logs/
"""

    def _get_readme_template(self) -> str:
        """
        获取README.md模板内容

        Returns:
            README.md文件的标准内容
        """
        return f"""# {self.project_name}

Project description goes here.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from {self.project_name.lower().replace('-', '_')} import main
main()
```

## License

MIT
"""

    def _get_requirements_template(self) -> str:
        """
        获取requirements.txt模板内容

        Returns:
            requirements.txt文件的标准内容
        """
        return """# Add your dependencies here
# e.g., requests>=2.28.0
# numpy>=1.21.0
"""

    def _get_setup_template(self) -> str:
        """
        获取setup.py模板内容

        Returns:
            setup.py文件的标准内容
        """
        return f"""from setuptools import setup, find_packages

setup(
    name="{self.project_name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
)
"""

    def _get_config_template(self, env: str) -> str:
        """
        获取配置文件模板内容

        Args:
            env: 环境名称，如"dev"或"prod"

        Returns:
            YAML配置文件的标准内容
        """
        return f"""app:
  debug: {"true" if env == "dev" else "false"}
  environment: {env}

database:
  host: localhost
  port: 5432
  name: {self.project_name.lower().replace("-", "_")}

redis:
  host: localhost
  port: 6379
"""

    def _get_env_template(self) -> str:
        """
        获取.env.example模板内容

        Returns:
            .env.example文件的标准内容
        """
        return f"""# {self.project_name} Configuration
DEBUG=true
ENVIRONMENT=development
"""

    def get_created_structure(self) -> dict[str, Any]:
        """
        获取创建的项目结构信息

        用于在项目创建完成后查看创建的所有目录和文件。

        Returns:
            包含项目名称、基础路径、目录列表和文件列表的字典
        """
        return {
            "project_name": self.project_name,
            "base_path": str(self.base_path),
            "directories": self.created_directories,
            "files": self.created_files,
        }
