"""iTerm2 integration for Claude Code sessions."""

import subprocess
import os
from pathlib import Path
from typing import Optional


def run_applescript(script: str) -> str:
    """Execute AppleScript and return output."""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def launch_claude_session(
    project_path: Optional[str] = None,
    topic: str = "New Session",
    tab_color: Optional[tuple[int, int, int]] = None,
) -> bool:
    """
    Launch a new Claude Code session in iTerm2 with proper naming.

    Args:
        project_path: Path to the project directory (defaults to current dir)
        topic: Description of what you're working on
        tab_color: RGB tuple for tab color (e.g., (255, 100, 100))
    """
    if project_path is None:
        project_path = os.getcwd()

    project_name = Path(project_path).name
    tab_title = f"{project_name} — ✳ {topic}"

    # Default color scheme for Claude sessions (purple-ish)
    if tab_color is None:
        tab_color = (147, 112, 219)  # Medium purple

    r, g, b = tab_color

    # Convert RGB 0-255 to AppleScript 0-65535
    r_as = int(r * 257)
    g_as = int(g * 257)
    b_as = int(b * 257)

    script = f'''
tell application "iTerm2"
    activate

    if (count of windows) = 0 then
        create window with default profile
    end if

    tell current window
        create tab with default profile

        tell current session
            -- Set user variable to identify Claude sessions
            set variable named "user.claude_project" to "{project_name}"
            set variable named "user.claude_topic" to "{topic}"
            set variable named "user.claude_session" to "🤖 {tab_title}"

            write text "cd {project_path}"
            write text "claude"
        end tell
    end tell

    tell current session of current tab of current window
        set background color to {{{r_as}, {g_as}, {b_as}}}
    end tell
end tell
    '''

    try:
        run_applescript(script)
        return True
    except Exception as e:
        print(f"Error launching session: {e}")
        return False


def get_claude_iterm_sessions() -> list[dict]:
    """Get all iTerm2 sessions that are marked as Claude sessions."""
    script = '''
tell application "iTerm2"
    set sessionList to {}
    set windowIndex to 0
    repeat with w in windows
        set windowIndex to windowIndex + 1
        set tabIndex to 0
        repeat with t in tabs of w
            set tabIndex to tabIndex + 1
            tell current session of t
                set sessionId to id
                set sessionName to name
                try
                    set claudeSession to variable named "user.claude_session"
                    set claudeProject to variable named "user.claude_project"
                    set claudeTopic to variable named "user.claude_topic"
                on error
                    set claudeSession to ""
                    set claudeProject to ""
                    set claudeTopic to ""
                end try
                if claudeSession is not "" then
                    set end of sessionList to (windowIndex as text) & "|||" & (tabIndex as text) & "|||" & sessionId & "|||" & claudeSession & "|||" & claudeProject & "|||" & claudeTopic
                end if
            end tell
        end repeat
    end repeat
    return sessionList
end tell
    '''

    output = run_applescript(script)
    if not output:
        return []

    sessions = []
    for item in output.split(", "):
        parts = item.split("|||")
        if len(parts) >= 6:
            project = parts[4]
            topic = parts[5]
            # Skip sessions with missing values (old test sessions)
            if project == "missing value" or not project:
                continue
            sessions.append({
                "window": int(parts[0]),
                "tab": int(parts[1]),
                "id": parts[2],
                "name": parts[3],
                "project": project,
                "topic": topic if topic != "missing value" else "",
            })

    return sessions


def switch_to_session(window: int, tab: int) -> bool:
    """Switch to a specific iTerm2 tab."""
    script = f'''
    tell application "iTerm2"
        activate
        set targetWindow to window {window}
        select targetWindow
        tell targetWindow
            select tab {tab}
        end tell
    end tell
    '''

    try:
        run_applescript(script)
        return True
    except Exception:
        return False


def update_session_badge(window: int, tab: int, badge_text: str) -> bool:
    """Update the badge text for a session."""
    script = f'''
    tell application "iTerm2"
        tell window {window}
            tell tab {tab}
                tell current session
                    set badge text to "{badge_text}"
                end tell
            end tell
        end tell
    end tell
    '''

    try:
        run_applescript(script)
        return True
    except Exception:
        return False


def set_session_color(window: int, tab: int, r: int, g: int, b: int) -> bool:
    """Set the background color for a session."""
    script = f'''
    tell application "iTerm2"
        tell window {window}
            tell tab {tab}
                tell current session
                    set background color to {{{r * 257}, {g * 257}, {b * 257}}}
                end tell
            end tell
        end tell
    end tell
    '''

    try:
        run_applescript(script)
        return True
    except Exception:
        return False


# Predefined color schemes for different project types
COLORS = {
    "default": (147, 112, 219),   # Purple
    "frontend": (100, 149, 237),  # Cornflower blue
    "backend": (60, 179, 113),    # Medium sea green
    "devops": (255, 165, 0),      # Orange
    "urgent": (255, 99, 71),      # Tomato red
}
