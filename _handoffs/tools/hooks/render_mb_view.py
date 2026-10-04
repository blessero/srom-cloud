#!/usr/bin/env python3
"""render_mb_view.py: Claude Code PostToolUse hook (Edit|Write) that keeps _widok/*.html current.

After an edit to a Markdown file in _handoffs/ or to a notes sheet (<module>/work/<folder>/<folder>_uwagi.md), runs
`mb_view.py --all` (about 1.5 s). Other edits: nothing. Never blocks; a failed render is reported (exit 1).
"""
import json, os, subprocess, sys

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VENV = os.path.expanduser("~/.venvs/srom/bin/python")
MB_VIEW = os.path.join(ROOT, "_handoffs", "tools", "mb_view.py")


def wanted(path):
    rel = os.path.relpath(path, ROOT)
    if rel.startswith("..") or not rel.endswith(".md"):
        return False
    parts = rel.split(os.sep)
    if parts[0] == "_handoffs":
        return True
    return (len(parts) == 4 and parts[0] in ("srom-produkcja", "srom-tlumacz") and parts[1] == "work"
            and parts[3] == f"{parts[2]}_uwagi.md")


def main():
    data = json.load(sys.stdin)
    path = (data.get("tool_input") or {}).get("file_path")
    if not path:
        return 0
    path = os.path.realpath(os.path.join(data.get("cwd") or os.getcwd(), os.path.expanduser(path)))
    if not wanted(path):
        return 0
    r = subprocess.run([VENV, MB_VIEW, "--all"], capture_output=True, text=True, timeout=60)
    if r.returncode:
        print(f"mb_view.py --all failed: {(r.stderr or r.stdout).strip()[-500:]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"render_mb_view.py: {e}", file=sys.stderr)
        sys.exit(1)
