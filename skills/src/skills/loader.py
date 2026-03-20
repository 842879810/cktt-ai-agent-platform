"""Skill loader for dynamic skill loading."""

import importlib
import inspect
from typing import Any, Dict, List, Type

from .base import BaseSkill, SkillConfig


class SkillLoader:
    """Loader for dynamically loading skills."""

    def __init__(self):
        self._loaded_skills: Dict[str, Type[BaseSkill]] = {}

    def load_from_module(self, module_name: str) -> List[Type[BaseSkill]]:
        """Load skills from a module."""
        try:
            module = importlib.import_module(module_name)
            skills = []

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseSkill) and obj != BaseSkill:
                    skills.append(obj)
                    self._loaded_skills[name] = obj

            return skills
        except ImportError as e:
            raise ImportError(f"Failed to load module {module_name}: {e}")

    def load_from_path(self, path: str) -> List[Type[BaseSkill]]:
        """Load skills from a file path."""
        # Import the module from the path
        module_name = path.replace("/", ".").replace("\\", ".").replace(".py", "")
        return self.load_from_module(module_name)

    def create_skill(self, skill_class: Type[BaseSkill], config: SkillConfig) -> BaseSkill:
        """Create a skill instance from a class."""
        return skill_class(config=config)
