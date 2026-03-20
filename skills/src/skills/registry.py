"""Skill registry for managing available skills."""

from typing import Dict, List, Optional

from .base import BaseSkill


class SkillRegistry:
    """Registry for managing skills."""

    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}

    def register(self, skill: BaseSkill) -> None:
        """Register a skill."""
        self._skills[skill.name] = skill

    def unregister(self, name: str) -> None:
        """Unregister a skill."""
        if name in self._skills:
            del self._skills[name]

    def get(self, name: str) -> Optional[BaseSkill]:
        """Get a skill by name."""
        return self._skills.get(name)

    def list_skills(self) -> List[str]:
        """List all registered skill names."""
        return list(self._skills.keys())

    def clear(self) -> None:
        """Clear all registered skills."""
        self._skills.clear()
