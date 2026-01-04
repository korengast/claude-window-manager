"""Setup script for py2app bundling."""

from setuptools import setup

APP = ["src/claude_window_manager/app.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "Claude Window Manager",
        "CFBundleDisplayName": "Claude Window Manager",
        "CFBundleIdentifier": "com.korengast.claude-window-manager",
        "CFBundleVersion": "0.1.0",
        "CFBundleShortVersionString": "0.1.0",
        "LSUIElement": True,  # Makes it a menu bar only app (no dock icon)
        "NSAppleEventsUsageDescription": "Claude Window Manager needs to control Terminal to switch windows.",
        "NSSystemAdministrationUsageDescription": "Claude Window Manager needs accessibility access to detect windows.",
    },
    "packages": ["rumps", "pynput"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
