#!/bin/bash
# Build script for Claude Window Manager

set -e

cd "$(dirname "$0")/.."

echo "==> Creating virtual environment..."
python3 -m venv build_env
source build_env/bin/activate

echo "==> Installing dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"

echo "==> Building app bundle..."
python setup.py py2app

echo "==> Done! App is at: dist/Claude Window Manager.app"
echo ""
echo "To install, drag the app to /Applications or run:"
echo "  cp -r 'dist/Claude Window Manager.app' /Applications/"

# Cleanup
deactivate
