"""One journal-facts file: srom-kanon's references/SROM_knowledge_base.md is the only copy in the repository
(no plugin-root, srom-tlumacz or dump copy), every skill's relative link to it resolves, and the Scope line
of the 03.10.2026 knowledge-base patch is in it."""
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # skills/srom-produkcja
SKILLS = os.path.dirname(ROOT)
REPO = os.path.abspath(os.path.join(SKILLS, "..", "..", ".."))           # the one repository
KB = os.path.join(SKILLS, "srom-kanon", "references", "SROM_knowledge_base.md")
res = []
def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

t("the srom-kanon knowledge base exists", os.path.isfile(KB), KB)
found = []
for d, dirs, files in os.walk(REPO):
    dirs[:] = [x for x in dirs if x not in (".git", "_widok", "node_modules", "__pycache__")]
    found += [os.path.join(d, f) for f in files if f.lower() == "srom_knowledge_base.md"]
t("no second SROM_knowledge_base.md anywhere in the repository", [os.path.realpath(f) for f in found] == [os.path.realpath(KB)],
  [os.path.relpath(f, REPO) for f in found])
bad = []
for sk in glob.glob(os.path.join(SKILLS, "*", "SKILL.md")):
    for m in re.finditer(r"(\.\.?/[\w./-]*)SROM_knowledge_base\.md", open(sk, encoding="utf-8").read()):
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(sk), m.group(0)))):
            bad.append((os.path.relpath(sk, SKILLS), m.group(0)))
t("every relative link to the knowledge base in a SKILL.md resolves", not bad, bad)
t("the Scope line (knowledge-base patch 20261003-0426) is in the knowledge base",
  "**Scope**" in open(KB, encoding="utf-8").read())
n, ok = len(res), sum(res)
print(f"KB ALL PASS {n}/{n}" if ok == n else f"KB FAILED {n - ok}/{n}")
