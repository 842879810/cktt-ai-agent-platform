"""Common utilities."""

import hashlib
import uuid
from typing import Any, Dict


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID."""
    unique_id = str(uuid.uuid4())
    if prefix:
        return f"{prefix}_{unique_id}"
    return unique_id


def hash_string(text: str) -> str:
    """Hash a string."""
    return hashlib.sha256(text.encode()).hexdigest()


def merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries."""
    result = base.copy()
    result.update(override)
    return result


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary."""
    return data.get(key, default)
