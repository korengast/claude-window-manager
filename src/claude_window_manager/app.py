"""Main menu bar application for Claude Window Manager."""

import rumps

from .window_detector import get_claude_sessions, switch_to_window, get_session_count
from .session import ClaudeSession


class ClaudeWindowManager(rumps.App):
    """Menu bar app for managing Claude Code windows."""

    def __init__(self):
        super().__init__(
            name="Claude Window Manager",
            title=self._get_title(0),
            quit_button=None,  # We'll add our own
        )
        self.sessions: list[ClaudeSession] = []
        self.refresh_sessions(None)

    def _get_title(self, count: int) -> str:
        """Get menu bar title with session count."""
        if count == 0:
            return "C"
        return f"C:{count}"

    def _build_menu(self) -> None:
        """Build the menu from current sessions."""
        self.menu.clear()

        if not self.sessions:
            self.menu.add(rumps.MenuItem("No Claude sessions", callback=None))
            self.menu.add(rumps.separator)
        else:
            for idx, session in enumerate(self.sessions, 1):
                # Create menu item with keyboard shortcut hint
                shortcut_hint = f"⌘{idx}" if idx <= 9 else "  "

                # Main item: project name
                title = f"{shortcut_hint}  {session.display_name}"
                item = rumps.MenuItem(title, callback=self._make_switch_callback(session))

                # Add submenu with details
                topic_item = rumps.MenuItem(f"    ✳ {session.display_topic}")
                topic_item.set_callback(None)

                if session.runtime_display:
                    runtime_item = rumps.MenuItem(f"    ⏱ {session.runtime_display}")
                    runtime_item.set_callback(None)

                self.menu.add(item)
                self.menu.add(topic_item)
                if session.runtime_display:
                    self.menu.add(runtime_item)
                self.menu.add(rumps.separator)

        # Add standard items
        self.menu.add(rumps.MenuItem("Refresh", callback=self.refresh_sessions, key="r"))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Quit", callback=self._quit, key="q"))

    def _make_switch_callback(self, session: ClaudeSession):
        """Create a callback function for switching to a session."""
        def callback(_):
            switch_to_window(session.window_id)
        return callback

    def _quit(self, _):
        """Quit the application."""
        rumps.quit_application()

    @rumps.timer(2)
    def refresh_sessions(self, _):
        """Refresh the list of Claude sessions."""
        self.sessions = get_claude_sessions()
        self.title = self._get_title(len(self.sessions))
        self._build_menu()


def main():
    """Entry point for the application."""
    app = ClaudeWindowManager()
    app.run()


if __name__ == "__main__":
    main()
