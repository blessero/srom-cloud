#!/usr/bin/env python3
"""Where srom-tlumacz finds things, from any working directory (Claude Code or a claude.ai container).

  python3 tlumacz_paths.py <skill-name>     -> prints that skill's directory (exit 1 if not found)
  python3 tlumacz_paths.py --source <file>  -> prints the path of a module data file
  python3 tlumacz_paths.py --module         -> prints the module folder (work/, sources/, training/)

SKILL   this skill (the real path, so ~/.claude/skills/srom-tlumacz resolves into the repository).
MODULE  the module folder with the per-article state: $SROM_TLUMACZ, else the folder that holds .claude/skills/srom-tlumacz
        (when it has work/), else the working directory.
ref(n)  SKILL/references/n — termbase, schema, decision log, register.
Skills: $SROM_SKILLS_DIR, MODULE/.claude/skills, MODULE/../.claude/skills, ~/.claude/skills, /mnt/skills/plugins,
/mnt/skills/user, MODULE/.. (sibling module folder). Data files: MODULE, MODULE/sources, ./, ./sources, /mnt/project.
"""
import os, sys

SKILL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_up = os.path.dirname(os.path.dirname(os.path.dirname(SKILL)))
MODULE = os.environ.get("SROM_TLUMACZ") or (_up if os.path.isdir(os.path.join(_up, "work")) else os.getcwd())


def ref(name):
    return os.path.join(SKILL, "references", name)


def skill_dir(name):
    roots = [os.environ.get("SROM_SKILLS_DIR", ""), os.path.join(MODULE, ".claude", "skills"),
             os.path.join(MODULE, "..", ".claude", "skills"), os.path.expanduser("~/.claude/skills"),
             "/mnt/skills/plugins", "/mnt/skills/user", os.path.join(MODULE, "..")]
    for r in roots:
        if r and os.path.isfile(os.path.join(r, name, "SKILL.md")):
            return os.path.abspath(os.path.join(r, name))
    return None


def source(name, *alts):
    for d in (MODULE, os.path.join(MODULE, "sources"), os.getcwd(), os.path.join(os.getcwd(), "sources"), "/mnt/project"):
        for n in (name,) + alts:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return os.path.abspath(p)
    return None


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--source":
        p = source(sys.argv[2])
    elif sys.argv[1:] == ["--module"]:
        p = MODULE
    elif len(sys.argv) == 2:
        p = skill_dir(sys.argv[1])
    else:
        print(__doc__); sys.exit(2)
    if not p:
        sys.stderr.write("not found\n"); sys.exit(1)
    print(p)
