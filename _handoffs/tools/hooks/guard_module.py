#!/usr/bin/env python3
"""guard_module.py <module>: Claude Code PreToolUse hook (Edit|Write|NotebookEdit) for a module session.

Refuses an edit whose real path lies in the other module's folder (root CLAUDE.md: "Never edit another module's
folder"; the Kanon lives in srom-produkcja, so srom-tlumacz cannot edit it). Symlinks are resolved, so
srom-typeset/ and ~/.claude/skills/srom-* count as srom-produkcja. Everything else (own folder, _handoffs/,
memory, scratchpad) passes. Exit 2 = refuse, with the reason shown to Claude; any other problem lets the edit pass.
"""
import json, os, sys

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OTHER = {"srom-tlumacz": "srom-produkcja", "srom-produkcja": "srom-tlumacz"}


def main():
    module = sys.argv[1]
    data = json.load(sys.stdin)
    inp = data.get("tool_input") or {}
    path = inp.get("file_path") or inp.get("notebook_path")
    if not path:
        return 0
    path = os.path.realpath(os.path.join(data.get("cwd") or os.getcwd(), os.path.expanduser(path)))
    banned = os.path.join(ROOT, OTHER[module])
    if path == banned or path.startswith(banned + os.sep):
        rel = os.path.relpath(path, ROOT)
        msg = (f"Refused: {rel} belongs to {OTHER[module]}. A {module} session never edits another module's "
               "folder (root CLAUDE.md). Ask for the change through _handoffs/ instead.")
        if module == "srom-tlumacz" and "srom-kanon" in rel:
            msg += " The Kanon is edited only from srom-produkcja."
        print(msg, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # a broken hook must never block work
        print(f"guard_module.py: {e}", file=sys.stderr)
        sys.exit(0)
