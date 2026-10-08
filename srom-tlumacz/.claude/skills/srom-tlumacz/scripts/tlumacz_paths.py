#!/usr/bin/env python3
"""Where srom-tlumacz finds things, from any working directory (Claude Code or a claude.ai container).

  python3 tlumacz_paths.py <skill-name>     -> prints that skill's directory (exit 1 if not found)
  python3 tlumacz_paths.py --source <file>  -> prints the path of a module data file
  python3 tlumacz_paths.py --module         -> prints the module folder (work/, sources/, training/)

SKILL   this skill (its real path, so a link into the repository resolves).
MODULE  the folder with the per-article state (work/, sources/, training/): $SROM_TLUMACZ, else the nearest
        `srom-tlumacz/` folder with work/ found from the working directory upwards (the folder itself, or a child of
        it: the workspace or repository root holds srom-tlumacz/), else the folder that holds this skill's
        .claude/skills/ (when it has work/), else Cowork's `workspace/srom-tlumacz/` next to the repository (the one
        folder, since 08.10.2026: Code keeps no copies of the texts), else the working directory.
ref(n)  SKILL/references/n — termbase, schema, decision log, register.
Skills: $SROM_SKILLS_DIR, MODULE/.claude/skills, MODULE/../.claude/skills (the root links), ~/.claude/skills, next to
this skill, /mnt/skills/plugins, /mnt/skills/user, MODULE/.. (sibling module folder). Data files: MODULE, MODULE/sources, ./, ./sources, /mnt/project.
"""
import os, sys

SKILL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def _module():
    if os.environ.get("SROM_TLUMACZ"):
        return os.environ["SROM_TLUMACZ"]
    d = os.getcwd()
    while True:
        for c in (d, os.path.join(d, "srom-tlumacz")):
            if os.path.basename(c) == "srom-tlumacz" and os.path.isdir(os.path.join(c, "work")):
                return c
        up = os.path.dirname(d)
        if up == d:
            break
        d = up
    _up = os.path.dirname(os.path.dirname(os.path.dirname(SKILL)))
    for c in (_up, os.path.join(os.path.dirname(os.path.dirname(_up)), "workspace", "srom-tlumacz")):
        if os.path.isdir(os.path.join(c, "work")):
            return c
    return os.getcwd()


MODULE = _module()


def ref(name):
    return os.path.join(SKILL, "references", name)


def skill_dir(name):
    roots = [os.environ.get("SROM_SKILLS_DIR", ""), os.path.join(MODULE, ".claude", "skills"),
             os.path.join(MODULE, "..", ".claude", "skills"), os.path.expanduser("~/.claude/skills"),
             os.path.dirname(SKILL), "/mnt/skills/plugins", "/mnt/skills/user", os.path.join(MODULE, "..")]
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
