"""Configuration loader."""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigLoader:
    """Load configuration from YAML files."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path("config")

    def load(self, filename: str) -> Dict[str, Any]:
        """Load a configuration file."""
        filepath = self.config_dir / filename

        if not filepath.exists():
            return {}

        with open(filepath, "r") as f:
            return yaml.safe_load(f) or {}

    def load_env(self, env: str) -> Dict[str, Any]:
        """Load configuration for a specific environment."""
        return self.load(f"{env}.yaml")

    def merge_configs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple configuration dictionaries."""
        result = {}
        for config in configs:
            result.update(config)
        return result
