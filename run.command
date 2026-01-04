#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
PYTHONPATH=src python3 -m claude_window_manager.app_pystray
