#!/usr/bin/env python3
"""CLI for Claude Window Manager - iTerm2 integration."""

import argparse
import os
import sys
from pathlib import Path

from .iterm2_integration import (
    launch_claude_session,
    get_claude_iterm_sessions,
    switch_to_session,
    COLORS,
)


def cmd_new(args):
    """Launch a new Claude session."""
    project_path = args.path or os.getcwd()
    topic = args.topic or "New Session"
    color = COLORS.get(args.color, COLORS["default"])

    print(f"🚀 Launching Claude in: {project_path}")
    print(f"   Topic: {topic}")

    success = launch_claude_session(
        project_path=project_path,
        topic=topic,
        tab_color=color,
    )

    if success:
        print("✅ Session launched!")
    else:
        print("❌ Failed to launch session")
        sys.exit(1)


def cmd_list(args):
    """List all Claude sessions."""
    sessions = get_claude_iterm_sessions()

    if not sessions:
        print("No Claude sessions found in iTerm2")
        print("\nLaunch one with: cwm new --topic 'My Task'")
        return

    print(f"\n🤖 Claude Sessions ({len(sessions)}):\n")
    for idx, s in enumerate(sessions, 1):
        topic_str = f" — ✳ {s['topic']}" if s.get('topic') else ""
        print(f"  [{idx}] {s['project']}{topic_str}")
    print()


def cmd_switch(args):
    """Switch to a Claude session."""
    sessions = get_claude_iterm_sessions()

    if not sessions:
        print("No Claude sessions found")
        print("\nLaunch one with: cwm new --topic 'My Task'")
        return

    if args.number:
        # Direct switch by number
        idx = args.number - 1
        if 0 <= idx < len(sessions):
            session = sessions[idx]
            switch_to_session(session["window"], session["tab"])
            topic_str = f" — ✳ {session['topic']}" if session.get('topic') else ""
            print(f"✅ Switched to: {session['project']}{topic_str}")
        else:
            print(f"Invalid session number: {args.number}")
            sys.exit(1)
    else:
        # Interactive selection
        print("\n🤖 Claude Sessions:\n")
        for idx, s in enumerate(sessions, 1):
            topic_str = f" — ✳ {s['topic']}" if s.get('topic') else ""
            print(f"  [{idx}] {s['project']}{topic_str}")

        print()
        try:
            choice = input("Enter number to switch (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return

            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                session = sessions[idx]
                switch_to_session(session["window"], session["tab"])
                topic_str = f" — ✳ {session['topic']}" if session.get('topic') else ""
                print(f"\n✅ Switched to: {session['project']}{topic_str}")
            else:
                print("Invalid selection")
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled")


def main():
    parser = argparse.ArgumentParser(
        description="Claude Window Manager - iTerm2 Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch new Claude session in current directory
  claude-wm new --topic "Feature Development"

  # Launch in specific project
  claude-wm new --path ~/Projects/myapp --topic "Bug Fix" --color urgent

  # List all Claude sessions
  claude-wm list

  # Switch to session interactively
  claude-wm switch

  # Switch to session 2 directly
  claude-wm switch 2
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # New session
    new_parser = subparsers.add_parser("new", help="Launch new Claude session")
    new_parser.add_argument("--path", "-p", help="Project path (default: current dir)")
    new_parser.add_argument("--topic", "-t", help="Topic/task description")
    new_parser.add_argument(
        "--color", "-c",
        choices=list(COLORS.keys()),
        default="default",
        help="Tab color scheme",
    )

    # List sessions
    subparsers.add_parser("list", aliases=["ls"], help="List Claude sessions")

    # Switch session
    switch_parser = subparsers.add_parser("switch", aliases=["sw"], help="Switch to session")
    switch_parser.add_argument("number", type=int, nargs="?", help="Session number")

    args = parser.parse_args()

    if args.command in ("new",):
        cmd_new(args)
    elif args.command in ("list", "ls"):
        cmd_list(args)
    elif args.command in ("switch", "sw"):
        cmd_switch(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
