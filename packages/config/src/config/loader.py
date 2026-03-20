"""Configuration loader."""

from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    """Load configuration from YAML files."""

    def __init__(self, config_dir: Path | None = None):
        self.config_dir = config_dir or Path("config")

    def load(self, filename: str) -> dict[str, Any]:
        """Load a configuration file."""
        filepath = self.config_dir / filename

        if not filepath.exists():
            return {}

        with open(filepath) as f:
            return yaml.safe_load(f) or {}

    def load_env(self, env: str) -> dict[str, Any]:
        """Load configuration for a specific environment."""
        return self.load(f"{env}.yaml")

    def merge_configs(self, *configs: dict[str, Any]) -> dict[str, Any]:
        """Merge multiple configuration dictionaries."""
        result = {}
        for config in configs:
            result.update(config)
        return result
