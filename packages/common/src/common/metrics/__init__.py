"""Metrics utilities."""

from typing import Any


class MetricsCollector:
    """Simple metrics collector."""

    def __init__(self):
        self._metrics: dict[str, Any] = {}

    def increment(self, name: str, value: int = 1) -> None:
        """Increment a counter."""
        self._metrics[name] = self._metrics.get(name, 0) + value

    def gauge(self, name: str, value: float) -> None:
        """Set a gauge value."""
        self._metrics[name] = value

    def timing(self, name: str, duration: float) -> None:
        """Record timing."""
        self._metrics[name] = duration

    def get(self, name: str) -> Any:
        """Get a metric value."""
        return self._metrics.get(name)

    def all(self) -> dict[str, Any]:
        """Get all metrics."""
        return self._metrics.copy()

    def clear(self) -> None:
        """Clear all metrics."""
        self._metrics.clear()


# Global metrics collector
metrics = MetricsCollector()
