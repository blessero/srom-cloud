"""E10 — Kanon § 12.2.3: the translator is header data. Front matter `tlumaczenie` (string or list) is not printed,
is reported with the master-CSV value (translators_struct), fails the build when empty, and survives the Word
working copy (export_work.py -> docx_in.py) and the handoff check."""
import os, sys, subprocess, tempfile, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, FX = os.path.join(ROOT, "scripts"), os.path.join(ROOT, "tests", "fixtures")
REFS = os.path.join(FX, "kanon_refs.json")
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1200]))
def py(*a):
    return subprocess.run([sys.executable, *a], capture_output=True, text=True)
d = tempfile.mkdtemp()
BODY = "Tekst[^1].\n\n[^1]: [@ficowski1985, s. 15].\n"
def md(name, front):
    p = os.path.join(d, name); open(p, "w", encoding="utf-8").write(front + BODY); return p
def build(p):
    out = os.path.join(d, os.path.basename(p) + "_out")
    r = py(os.path.join(S, "build.py"), p, "--refs", REFS, "--out", out)
    stem = os.path.splitext(os.path.basename(p))[0]
    return r.returncode, open(os.path.join(out, stem + "_report.md"), encoding="utf-8").read(), open(os.path.join(out, stem + ".txt"), encoding="utf-8").read()

one = md("one.md", '---\ntlumaczenie: "Jan Nowak"\n---\n\n')
code, rep, txt = build(one)
t("one translator: PASS, reported with translators_struct", code == 0 and "## Header data" in rep and "`Jan|Nowak||`" in rep, rep[:900])
t("the translator is not printed", "Nowak" not in txt, txt[:200])
two = md("two.md", '---\ntlumaczenie:\n  - "Jan Nowak"\n  - "Anna Maria Kowalska-Wróbel"\n---\n\n')
code, rep, txt = build(two)
t("two translators: both, in order, joined ' ;; '", code == 0 and "`Jan|Nowak|| ;; Anna Maria|Kowalska-Wróbel||`" in rep, rep[:900])
empty = md("empty.md", '---\ntlumaczenie: ""\n---\n\n')
code, rep, txt = build(empty)
t("empty tlumaczenie fails the build", code == 1 and "front matter 'tlumaczenie' is empty" in rep, rep[:900])
code, rep, txt = build(md("none.md", ""))
t("no front matter: no header section, PASS", code == 0 and "## Header data" not in rep, rep[:600])

# Word working copy round trip
w = os.path.join(d, "two_robocza.docx")
py(os.path.join(S, "export_work.py"), two, "-o", w)
t("working copy stores the names in the custom property srom-tlumaczenie",
  "Kowalska-Wróbel" in zipfile.ZipFile(w).read("docProps/custom.xml").decode("utf-8"))
back = os.path.join(d, "two_back.md")
r = py(os.path.join(S, "docx_in.py"), w, "-o", back)
bt = open(back, encoding="utf-8").read()
t("round trip restores the front matter (both names)", bt.startswith("---\ntlumaczenie:\n") and '"Jan Nowak"' in bt
  and '"Anna Maria Kowalska-Wróbel"' in bt, bt[:300])
code, rep, txt = build(back)
t("build from the round-tripped file reports the same translators", code == 0 and "`Jan|Nowak|| ;; Anna Maria|Kowalska-Wróbel||`" in rep, rep[:900])
src = md("src.md", "")
c = py(os.path.join(S, "check.py"), "--pair", src, back, "--refs", REFS)
t("handoff check: front matter is not a structure difference", c.returncode == 0, c.stdout[-600:])

n, ok = len(res), sum(res)
print(f"E10 ALL PASS {n}/{n}" if ok == n else f"E10 FAILED {n - ok}/{n}")
