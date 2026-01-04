"""Data models for Claude Code sessions."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class ClaudeSession:
    """Represents a running Claude Code session."""

    window_id: int
    window_name: str
    project: str
    topic: Optional[str]
    language: Optional[str]
    pid: Optional[int]
    tty: Optional[str]
    start_time: Optional[datetime]

    @property
    def runtime(self) -> Optional[timedelta]:
        """Calculate how long the session has been running."""
        if self.start_time is None:
            return None
        return datetime.now() - self.start_time

    @property
    def runtime_display(self) -> str:
        """Format runtime for display."""
        runtime = self.runtime
        if runtime is None:
            return ""

        total_seconds = int(runtime.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60

        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    @property
    def display_name(self) -> str:
        """Get a display name for the session."""
        return self.project or "Unknown"

    @property
    def display_topic(self) -> str:
        """Get the topic for display."""
        return self.topic or "No topic"

    def __str__(self) -> str:
        runtime_str = f" ({self.runtime_display})" if self.runtime else ""
        topic_str = f" - {self.topic}" if self.topic else ""
        return f"{self.project}{topic_str}{runtime_str}"
