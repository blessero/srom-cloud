"""Turns the Code ledger (a copy of _handoffs/MB-decisions.md) into the Cowork ledger, in place: Code-only paths
rewritten, SYS-1 restated for the plugin (GEN-15, SYS-6 raised by the move were decided by MB 03.10.2026 03:40). Every replacement must hit exactly once."""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()
EDITS = [
    ("Rules for sessions writing here: `_handoffs/README.md` § Questions for MB.",
     "Rules for sessions writing here: the workspace `CLAUDE.md` § Questions for MB."),
    ("🔴 `srom-produkcja/.claude/skills/srom-kanon/references/kanon-redakcyjny.md`",
     "🔴 `srom-kanon/references/kanon-redakcyjny.md`"),
    ("Your decision of 28.09.2026: the live site is old; when the work here is finished, you update the quant skill "
     "(srom-quant, now in the srom-produkcja repo) in\ndesktop Claude and the plugin on the site together (the skill's "
     "copy carries plugin v2.3). Until then nothing to do.\nDetail: 🔴 `_handoffs/curator-update-2026-09-27/CHANGES.md`",
     "Your decision of 28.09.2026: the live site is old; when the work here is finished, you update the site's plugin\n"
     "(the srom-quant skill carries v2.3) and decide whether the site shows the translator (the tools already put it\n"
     "in the CSV and the Crossref deposit: column `translators_struct`). In Cowork the quant skill is part of the srom plugin, so\n"
     "the \"desktop Claude\" half is done by installing the plugin. Until then nothing to do.\n"
     "Detail: 🔴 `srom-quant/assets/srom-scholarly.php` (the site's plugin, v2.3)"),
    ("| SYS-1 | Translator on the website, quant skill upload | Later | nothing |",
     "| SYS-1 | Translator on the website; update the site's plugin | Later | nothing |"),
    ("### SYS-1 · Translator on the website; quant skill (former curator) in desktop Claude",
     "### SYS-1 · Translator on the website; update the site's plugin"),
]
for a, b in EDITS:
    n = s.count(a)
    if n != 1:
        sys.exit(f"LEDGER EDIT FAILED ({n} hits): {a[:60]}")
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("LEDGER COWORK OK")
