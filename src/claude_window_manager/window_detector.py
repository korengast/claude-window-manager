"""Detect Terminal windows running Claude Code using AppleScript."""

import re
import subprocess
from datetime import datetime, timedelta
from typing import Optional

from .session import ClaudeSession


def run_applescript(script: str) -> str:
    """Execute AppleScript and return output."""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def get_terminal_windows() -> list[tuple[int, str]]:
    """Get all Terminal.app windows with their IDs and names."""
    script = '''
    tell application "Terminal"
        set windowList to {}
        repeat with w in windows
            set end of windowList to (id of w as text) & "|||" & (name of w as text)
        end repeat
        return windowList
    end tell
    '''
    output = run_applescript(script)
    if not output:
        return []

    windows = []
    # Output format: "id|||name, id|||name, ..."
    for item in output.split(", "):
        if "|||" in item:
            parts = item.split("|||", 1)
            try:
                window_id = int(parts[0])
                window_name = parts[1]
                windows.append((window_id, window_name))
            except (ValueError, IndexError):
                continue

    return windows


def parse_window_name(name: str) -> tuple[str, Optional[str], Optional[str]]:
    """
    Parse Terminal window name to extract project, topic, and language.

    Expected format: "project — ✳ topic — language ◂ claude"
    Example: "ai-app-builder — ✳ Evaluations Package — Python ◂ claude"
    """
    project = name
    topic = None
    language = None

    # Check if this is a Claude window
    if "claude" not in name.lower():
        return project, topic, language

    # Try to parse the structured format
    # Pattern: project — ✳ topic — language ◂ claude
    match = re.match(
        r'^(.+?)\s*[—-]\s*✳\s*(.+?)\s*[—-]\s*(\w+)\s*◂\s*claude',
        name,
        re.IGNORECASE
    )
    if match:
        project = match.group(1).strip()
        topic = match.group(2).strip()
        language = match.group(3).strip()
        return project, topic, language

    # Try simpler pattern: project — ✳ topic
    match = re.match(r'^(.+?)\s*[—-]\s*✳\s*(.+?)(?:\s*[—-]|$)', name)
    if match:
        project = match.group(1).strip()
        topic = match.group(2).strip()
        return project, topic, language

    # Fall back to just using the first part before any separator
    parts = re.split(r'\s*[—-]\s*', name)
    if parts:
        project = parts[0].strip()

    return project, topic, language


def get_claude_processes() -> dict[str, tuple[int, datetime]]:
    """
    Get running Claude processes with their TTY and start time.
    Returns: {tty: (pid, start_time)}
    """
    result = subprocess.run(
        ["ps", "-eo", "pid,tty,lstart,comm"],
        capture_output=True,
        text=True,
    )

    processes = {}
    for line in result.stdout.strip().split("\n")[1:]:  # Skip header
        if "claude" in line.lower():
            parts = line.split()
            if len(parts) >= 8:
                try:
                    pid = int(parts[0])
                    tty = parts[1]
                    # lstart format: "Mon Jan  4 14:30:00 2025"
                    time_str = " ".join(parts[2:7])
                    start_time = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
                    processes[tty] = (pid, start_time)
                except (ValueError, IndexError):
                    continue

    return processes


def get_claude_sessions() -> list[ClaudeSession]:
    """Get all Claude Code sessions from Terminal windows."""
    windows = get_terminal_windows()
    processes = get_claude_processes()

    sessions = []
    for window_id, window_name in windows:
        # Check if this window is running Claude
        if "claude" not in window_name.lower():
            continue

        project, topic, language = parse_window_name(window_name)

        # Try to match with a process (best effort)
        pid = None
        start_time = None
        tty = None

        # We can't directly map window to TTY, so we just use process info as available
        # For now, we'll show processes but can't guarantee mapping

        session = ClaudeSession(
            window_id=window_id,
            window_name=window_name,
            project=project,
            topic=topic,
            language=language,
            pid=pid,
            tty=tty,
            start_time=start_time,
        )
        sessions.append(session)

    return sessions


def switch_to_window(window_id: int) -> bool:
    """Bring a Terminal window to the front."""
    script = f'''
    tell application "Terminal"
        set targetWindow to window id {window_id}
        set index of targetWindow to 1
        activate
    end tell
    '''
    try:
        run_applescript(script)
        return True
    except Exception:
        return False


def get_session_count() -> int:
    """Quick count of Claude sessions without full parsing."""
    windows = get_terminal_windows()
    return sum(1 for _, name in windows if "claude" in name.lower())
