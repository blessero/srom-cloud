"""srom-ikonograf files: the contact-sheet template renders in the side panel (no lazy images, local thumbnails
embedded, render after the MINI block), carries alt/also; the record template has the footnote-leads section; no
User-Agent or command in the skill names the journal's domain (the live-site hook would block it)."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IK = os.path.join(ROOT, "srom-ikonograf")
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))
def rd(*p):
    return open(os.path.join(IK, *p), encoding="utf-8").read()

html = rd("assets", "template", "kontaktowka.html")
t("template: no lazy <img> (the side panel never loads lazy images)", not re.search(r"<img[^>]*loading=", html))
t("template: local thumbnails come from the MINI block, rendered after it loads",
  "var MINI = {}" in html and "MINI" in html.split("var MINI")[0] and 'addEventListener("DOMContentLoaded", render)' in html
  and html.index("var MINI = {}") > html.index("DOMContentLoaded"))
t("template: better copy (alt) and also-in fields rendered", "Lepsza kopia:" in html and "Też w:" in html)
t("template: size toggle and enlarged view", '"duże"' in html and 'id="lb"' in html)
t("record template: § 7 footnote leads and the zgody.md pointer",
  "## 7. Footnote leads" in rd("assets", "template", "ikonografia.md") and "zgody.md" in rd("assets", "template", "ikonografia.md"))
bad = [(f, m) for f in ("SKILL.md", "references/sources.md", "references/rights.md")
       for m in re.findall(r"-A\s+\"[^\"]*studiaromologica[^\"]*\"", rd(*f.split("/")))]
t("no User-Agent naming the journal's domain", not bad, bad)
print(f"IKONOGRAF ALL PASS {sum(res)}/{len(res)}" if all(res) else f"IKONOGRAF FAILED {res.count(False)}/{len(res)}")
