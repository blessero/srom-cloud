"""E8 — kanon § 7.1: non-author notes (title note, "– przyp. tłum.", "– przyp. red.") form one asterisk series,
set by hand above the numbered notes. They must leave the Word footnotes (an InDesign story has one footnote
sequence): a marker * in its character style in the text, the notes as paragraphs at the end of the DOCX
(title note first), and nothing of them in the numbered sequence, the Ibidem logic or the note numbers."""
import os, re, sys, json, subprocess, tempfile, zipfile
from lxml import etree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FX = os.path.join(ROOT, "tests", "fixtures")
REFS = os.path.join(FX, "kanon_refs.json")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
cfg = json.load(open(os.path.join(ROOT, "config", "styles.json"), encoding="utf-8"))
AST_P, AST_C = cfg["paragraph"]["asterisk_note"], cfg["character"]["asterisk_ref"]
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

def build(md, extra=()):
    out = tempfile.mkdtemp()
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), md, "--refs", REFS, "--out", out, *extra],
                       capture_output=True, text=True)
    stem = os.path.splitext(os.path.basename(md))[0]
    rep = open(os.path.join(out, stem + "_report.md"), encoding="utf-8").read()
    return r.returncode, out, stem, rep

def ptext(p):
    return "".join(x.text or "" for x in p.iter(W + "t"))

code, out, stem, rep = build(os.path.join(FX, "e8.md"))
t("build PASS with title, translator, editorial and multi-paragraph non-author notes", code == 0, rep[:1500])
z = zipfile.ZipFile(os.path.join(out, stem + ".docx"))
sty = etree.fromstring(z.read("word/styles.xml"))
id2name = {s.get(W + "styleId"): s.find(W + "name").get(W + "val") for s in sty.iter(W + "style") if s.find(W + "name") is not None}
doc = etree.fromstring(z.read("word/document.xml"))
fn = etree.fromstring(z.read("word/footnotes.xml"))
notes = [f for f in fn.iter(W + "footnote") if f.get(W + "type") is None]
ntexts = [ptext(f) for f in notes]
t("numbered footnotes are the author's notes only (3)", len(notes) == 3, ntexts)
t("no '– przyp. tłum./red.' note among the numbered footnotes", not any(re.search(r"przyp\. (tłum|red)\.\s*$", x) for x in ntexts), ntexts)
t("author's note closed by '[… – przyp. tłum.]' stays numbered (note 3)", "wydanie polskie" in ntexts[2], ntexts)
marks = [r for r in doc.iter(W + "r") if r.find(W + "rPr/" + W + "rStyle") is not None
         and id2name.get(r.find(W + "rPr/" + W + "rStyle").get(W + "val")) == AST_C]
t("three markers * in the character style for the asterisk series", len(marks) == 3 and all(ptext(r) == "*" for r in marks),
  [ptext(r) for r in marks])
paras = list(doc.iter(W + "p"))
def pname(p):
    ps = p.find(W + "pPr/" + W + "pStyle")
    return id2name.get(ps.get(W + "val")) if ps is not None else None
ast = [ptext(p) for p in paras if pname(p) == AST_P]
t("asterisk notes: title note first, then in text order, each opening '* '",
  len(ast) == 5 and ast[0].startswith("* Pierwodruk") and ast[1].startswith("* Por.") and ast[2].startswith("* Uwaga redakcji")
  and ast[3].startswith("* Pierwszy akapit") and not ast[4].startswith("*") and ast[4].startswith("Drugi akapit"), ast)
t("asterisk notes are the last paragraphs of the document (after the bibliography)",
  [pname(p) for p in paras[-5:]] == [AST_P] * 5, [pname(p) for p in paras[-6:]])
t("title note no longer at the top of the text", pname(paras[0]) != AST_P, pname(paras[0]))
t("no Ibidem inside an asterisk note (short form instead)", not any("Ibidem" in a for a in ast) and "Cyganie na polskich drogach…, s. 16" in ast[1], ast[1])
t("numbered note after a non-author note: Ibidem replaced by the short form, reason in the report",
  "Ibidem" not in ntexts[1] and "non-author (asterisk) note" in rep, (ntexts[1], rep[rep.find("## Ibidem replaced"):][:300]))
t("DOCX verification lines for the series pass", "[x] asterisk markers in the text = translator/editorial notes: markers 3 / notes 3" in rep
  and "[x] asterisk notes at the end = notes + title note" in rep and "[x] no translator/editorial note among the numbered" in rep, rep[:2500])
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
t("page-less citation inside a translator note -> query row with note '*'", re.search(r"\| redakcja \| odwołanie do całości dzieła[^|]*\| \* \| mroz1998", q), q)
gw = os.path.join(out, stem + "_gwiazdki.jsx")
g = open(gw, encoding="utf-8").read() if os.path.exists(gw) else ""
t("_gwiazdki.jsx written: 3 markers, title note, 4 notes listed in order", "var AST_MARKS = 3;" in g and "var TITLE = true;" in g
  and g.find("Pierwodruk") < g.find("* Por.") < g.find("Uwaga redakcji") < g.find("Pierwszy akapit"), g[:900])
pi = open(os.path.join(out, stem + "_postimport.jsx"), encoding="utf-8").read()
t("_postimport.jsx expects 3 markers and 4 asterisk notes", "var AST_MARKS = 3;" in pi and "var AST_NOTES = 4;" in pi, pi[:600])
r = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), gw, os.path.join(out, stem + "_postimport.jsx")],
                   capture_output=True, text=True)
t("both scripts valid ES3", "JSX-DONE" in r.stdout and r.stdout.count("acorn es3") + r.stdout.count("fallback") == 2, r.stdout)

# without non-author notes: nothing changes, no _gwiazdki.jsx
code, out, stem, rep = build(os.path.join(FX, "sample_article.md"))
t("article without non-author notes: PASS, no _gwiazdki.jsx, series checks 0 / 0", code == 0
  and not os.path.exists(os.path.join(out, stem + "_gwiazdki.jsx")) and "markers 0 / notes 0" in rep, rep[:1200])

# label and formula must agree (check.py, run by the build)
d = tempfile.mkdtemp()
bad = os.path.join(d, "bad.md")
open(bad, "w", encoding="utf-8").write("Tekst[^r1].\n\n[^r1]: Uwaga bez formuły.\n")
code, out, stem, rep = build(bad)
t("[^r1] without '– przyp. red.' fails the build", code == 1 and "[^r1] must end with the formula" in rep, rep[:800])

# printed numbers (--pair-src / query rows): the * series takes no number
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import check
src = os.path.join(d, "src.md"); tgt = os.path.join(d, "tgt.md")
open(src, "w", encoding="utf-8").write("A[^a1] b[^a2] c[^a3].\n\n[^a1]: X.\n\n[^a2]: Y.\n\n[^a3]: Z.\n")
open(tgt, "w", encoding="utf-8").write("A[^a1] t[^t1] b[^a2] r[^r1] c[^a3].\n\n[^a1]: X.\n\n[^t1]: T – przyp. tłum.\n\n"
                                      "[^a2]: Y.\n\n[^r1]: R – przyp. red.\n\n[^a3]: Z.\n")
t("printed numbers skip translator/editorial notes", check.printed_numbers(src, tgt) == {"a1": 1, "a2": 2, "a3": 3},
  check.printed_numbers(src, tgt))

n, ok = len(res), sum(res)
print(f"E8 ALL PASS {n}/{n}" if ok == n else f"E8 FAILED {n - ok}/{n}")
