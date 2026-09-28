#!/usr/bin/env python3
"""Locate skills and source files in any environment (claude.ai container or Claude Code).

  python3 tlumacz_paths.py <skill-name>     -> prints the skill directory (exit 1 if not found)
  python3 tlumacz_paths.py --source <file>  -> prints the path of a source file
Search order for skills: $SROM_SKILLS_DIR, ./.claude/skills, ../.claude/skills, ~/.claude/skills,
/mnt/skills/plugins, /mnt/skills/user, ../<name> (sibling module folder).
Sources: ./, ./sources, ../sources, ../_shared, /mnt/project.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def skill_dir(name):
    roots = [os.environ.get("SROM_SKILLS_DIR", ""), os.path.join(HERE, ".claude", "skills"),
             os.path.join(HERE, "..", ".claude", "skills"), os.path.expanduser("~/.claude/skills"),
             "/mnt/skills/plugins", "/mnt/skills/user", os.path.join(HERE, "..")]
    for r in roots:
        if r and os.path.isfile(os.path.join(r, name, "SKILL.md")):
            return os.path.abspath(os.path.join(r, name))
    return None


def source(name, *alts):
    for d in (HERE, os.path.join(HERE, "sources"), os.path.join(HERE, "..", "sources"),
              os.path.join(HERE, "..", "_shared"), "/mnt/project"):
        for n in (name,) + alts:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return os.path.abspath(p)
    return None


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--source":
        p = source(sys.argv[2])
    elif len(sys.argv) == 2:
        p = skill_dir(sys.argv[1])
    else:
        print(__doc__); sys.exit(2)
    if not p:
        sys.stderr.write("not found\n"); sys.exit(1)
    print(p)
