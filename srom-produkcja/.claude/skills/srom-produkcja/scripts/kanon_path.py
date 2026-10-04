"""Where is the srom-kanon skill (the house rules and their linter)? srom-produkcja requires it.

Order: $SROM_KANON (if set, the only candidate) · next to this skill (repo, ~/.claude/skills, /mnt/skills/user)
· ~/.claude/skills/srom-kanon · /mnt/skills/user|plugins/srom-kanon. A candidate counts only if it has the linter.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISSING = ("srom-kanon skill not found — srom-produkcja needs its linter (scripts/lint_srom.py) and rules. "
           "Install srom-kanon next to srom-produkcja (or in ~/.claude/skills), or set SROM_KANON=<its folder>.")


def find_kanon():
    env = os.environ.get("SROM_KANON")
    cands = [env] if env else [os.path.join(os.path.dirname(ROOT), "srom-kanon"),
                               os.path.expanduser("~/.claude/skills/srom-kanon"),
                               "/mnt/skills/user/srom-kanon", "/mnt/skills/plugins/srom-kanon"]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "scripts", "lint_srom.py")):
            return os.path.abspath(c)
    return None


def linter(kanon_dir):
    return os.path.join(kanon_dir, "scripts", "lint_srom.py")


def kanon_version(kanon_dir):
    """version of the normative Kanon text (its header "**Wersja X.Y") or None"""
    p = os.path.join(kanon_dir, "references", "kanon-redakcyjny.md")
    if not os.path.isfile(p):
        return None
    m = re.search(r"\*\*Wersja (\d+\.\d+)", open(p, encoding="utf-8").read(3000))
    return m.group(1) if m else None
