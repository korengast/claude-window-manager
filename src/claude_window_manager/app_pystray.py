"""Menu bar app using pystray (more reliable on modern macOS)."""

import threading
import time
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

from .window_detector import get_claude_sessions, switch_to_window
from .session import ClaudeSession


def create_icon_image(count: int) -> Image.Image:
    """Create a simple icon with session count."""
    # Create a 22x22 image (standard menu bar size)
    size = 22
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a circle
    draw.ellipse([2, 2, size-2, size-2], fill=(100, 100, 100, 255))

    # Draw the count
    text = str(count) if count < 10 else "+"
    # Center the text (approximate)
    draw.text((8, 4), text, fill=(255, 255, 255, 255))

    return img


class ClaudeWindowManagerTray:
    """Pystray-based menu bar app."""

    def __init__(self):
        self.sessions: list[ClaudeSession] = []
        self.icon = None
        self.running = True

    def refresh_sessions(self):
        """Refresh session list."""
        self.sessions = get_claude_sessions()

    def build_menu(self):
        """Build the menu dynamically."""
        self.refresh_sessions()

        menu_items = []

        if not self.sessions:
            menu_items.append(item("No Claude sessions", None, enabled=False))
        else:
            for idx, session in enumerate(self.sessions):
                # Create a closure to capture the session
                def make_callback(s):
                    return lambda: switch_to_window(s.window_id)

                label = f"{session.display_name}: {session.display_topic}"
                menu_items.append(item(label, make_callback(session)))

        menu_items.append(pystray.Menu.SEPARATOR)
        menu_items.append(item("Refresh", self.on_refresh))
        menu_items.append(item("Quit", self.on_quit))

        return menu_items

    def on_refresh(self):
        """Refresh menu."""
        self.update_menu()

    def on_quit(self):
        """Quit the app."""
        self.running = False
        if self.icon:
            self.icon.stop()

    def update_menu(self):
        """Update the icon and menu."""
        self.refresh_sessions()
        if self.icon:
            self.icon.icon = create_icon_image(len(self.sessions))
            self.icon.menu = pystray.Menu(*self.build_menu())

    def refresh_loop(self):
        """Background thread to refresh periodically."""
        while self.running:
            time.sleep(3)
            if self.running:
                self.update_menu()

    def run(self):
        """Run the app."""
        self.refresh_sessions()

        self.icon = pystray.Icon(
            "claude-wm",
            create_icon_image(len(self.sessions)),
            "Claude Window Manager",
            pystray.Menu(*self.build_menu())
        )

        # Start refresh thread
        refresh_thread = threading.Thread(target=self.refresh_loop, daemon=True)
        refresh_thread.start()

        # Run the icon (blocks)
        self.icon.run()


def main():
    """Entry point."""
    app = ClaudeWindowManagerTray()
    app.run()


if __name__ == "__main__":
    main()
