# Claude Window Manager

A native macOS menu bar app to manage multiple Claude Code terminal windows.

## Features

- **Window Detection**: Automatically detects all Terminal windows running Claude Code
- **Quick Switching**: Click to switch between Claude sessions instantly
- **Context Display**: Shows project name and current topic for each session
- **Keyboard Shortcuts**: Use ⌘1-9 to quickly jump to specific sessions
- **Live Updates**: Auto-refreshes every 2 seconds

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/korengast/claude-window-manager.git
cd claude-window-manager

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run the app
claude-wm
```

### Build as macOS App

```bash
# Build the .app bundle
./scripts/build.sh

# The app will be in dist/ClaudeWindowManager.app
```

## Usage

1. Launch the app - it appears in your menu bar
2. Click the menu bar icon to see all Claude Code sessions
3. Click any session to switch to it
4. Use ⌘⇧C to open the switcher from anywhere

## Requirements

- macOS 14.0+
- Python 3.11+
- Terminal.app with Claude Code running

## License

MIT
