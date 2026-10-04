"""G15: working copy round trip. SROM-MD -> export_work.py -> Word -> docx_in.py -> SROM-MD must be
lossless (same document tree), must carry the editor's Word edits, and whatever Word damages must be
caught by check.py --pair. The build from the round-tripped file prints exactly the same text."""
import os, re, sys, json, shutil, subprocess, tempfile, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, FX = os.path.join(ROOT, "scripts"), os.path.join(ROOT, "tests", "fixtures")
REFS = os.path.join(FX, "kanon_refs.json")
FROM = ("markdown-smart-superscript-subscript-strikeout-raw_html-raw_tex-tex_math_dollars"
        "-implicit_figures-fancy_lists-example_lists-task_lists-auto_identifiers")
d = tempfile.mkdtemp()
res = []
def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))
def py(*a):
    return subprocess.run([sys.executable, *a], capture_output=True, text=True)
def tree(path):
    txt = open(path, encoding="utf-8").read()
    txt = re.sub(r"[ \t]*<!--.*?-->", "", txt, flags=re.S)       # comments travel as Word comments and are dropped on import
    j = json.loads(subprocess.run(["pandoc", "-f", FROM, "-t", "json"], input=txt, capture_output=True, text=True).stdout)
    def clean(x):
        if isinstance(x, list): return [clean(i) for i in x]
        if isinstance(x, dict):
            if x.get("t") == "CodeBlock": return {"t": "CodeBlock", "c": [["", [], []], x["c"][1]]}
            return {k: clean(v) for k, v in x.items()}
        return x
    return clean(j["blocks"])
def roundtrip(src, name):
    w = os.path.join(d, name + "_robocza.docx")
    py(os.path.join(S, "export_work.py"), src, "-o", w)
    back = os.path.join(d, name + "_back.md")
    r = py(os.path.join(S, "docx_in.py"), w, "-o", back)
    return w, back, r

for fx in ("sample_article.md", "blocks.md", "roundtrip.md"):
    w, back, r = roundtrip(os.path.join(FX, fx), fx[:-3])
    t(f"{fx}: working copy recognised on import", "working copy round trip" in r.stdout, r.stdout + r.stderr)
    t(f"{fx}: round trip is lossless (identical document tree)", tree(os.path.join(FX, fx)) == tree(back), open(back, encoding="utf-8").read()[:1200])
    if fx == "blocks.md":   # pandoc 3.8 puts the "Table Caption" style inside the caption: it must survive
        t("blocks.md: table caption survives the round trip", "Tabela 1. Liczebność Romów" in open(back, encoding="utf-8").read())

# editorial brackets come back as written (text level, not only the tree): no \\[ … \\] escapes
bk = os.path.join(d, "brackets.md")
BK = ("Within CSEE [Central and South Eastern Europe], the “children of [a national] group” […] stay.[^1]\n\n"
      "[^1]: A note with [@ficowski1985, s. 15] and an insertion [sic].\n")
open(bk, "w", encoding="utf-8").write(BK)
w, back, r = roundtrip(bk, "brackets")
t("editorial brackets survive the round trip as plain text (file identical)", open(back, encoding="utf-8").read() == BK,
  open(back, encoding="utf-8").read())

src = os.path.join(FX, "sample_article.md")
w, back, r = roundtrip(src, "s")
b1 = py(os.path.join(S, "build.py"), src, "--refs", REFS, "--out", os.path.join(d, "b1"))
b2 = py(os.path.join(S, "build.py"), back, "--refs", REFS, "--out", os.path.join(d, "b2"))
t1 = open(os.path.join(d, "b1", "sample_article.txt"), encoding="utf-8").read()
t2 = open(os.path.join(d, "b2", "s_back.txt"), encoding="utf-8").read()
t("build from the round-tripped file: PASS and the very same printed text", b1.returncode == 0 and b2.returncode == 0 and t1 == t2, (b2.stdout, t1[:300], t2[:300]))

def edit_docx(path, out, repl):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(path) as z:
        z.extractall(tmp); names = z.namelist()
    for part in ("word/document.xml", "word/footnotes.xml"):
        p = os.path.join(tmp, part); x = open(p, encoding="utf-8").read()
        for a, b in repl: x = x.replace(a, b)
        open(p, "w", encoding="utf-8").write(x)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names: z.write(os.path.join(tmp, n), n)

# the editor's changes in Word: a word in the text, a page number inside a token
ed = os.path.join(d, "ed.docx")
edit_docx(w, ed, [("Drugi akapit", "Kolejny akapit"), ("s. 17]", "s. 18]")])
py(os.path.join(S, "docx_in.py"), ed, "-o", os.path.join(d, "ed.md"))
em = open(os.path.join(d, "ed.md"), encoding="utf-8").read()
t("editor's Word edits come back (text and a page inside a token)", "Kolejny akapit" in em and "[@ficowski1985, s. 18]" in em, em[:800])
c = py(os.path.join(S, "check.py"), "--pair", src, os.path.join(d, "ed.md"), "--refs", REFS)
t("pair check: edited page is a WARN, not an error", c.returncode == 0 and "numbers differ" in c.stdout, c.stdout)

# Word damages a token (autocorrect, typo in the key)
dm = os.path.join(d, "dm.docx")
edit_docx(w, dm, [("@mroz2011", "@mroz2101")])
py(os.path.join(S, "docx_in.py"), dm, "-o", os.path.join(d, "dm.md"))
c = py(os.path.join(S, "check.py"), "--pair", src, os.path.join(d, "dm.md"), "--refs", REFS)
t("damaged citation token caught (unknown key / keys differ)", c.returncode == 1 and "mroz2101" in c.stdout, c.stdout)

# a comment (e.g. srom-tlumacz's open item) becomes a Word comment: listed on import, never blocking
rt = os.path.join(FX, "roundtrip.md")
w3, back3, r3 = roundtrip(rt, "rt")
t("comment exported as a real Word comment", "word/comments.xml" in zipfile.ZipFile(w3).namelist() and "DO SPRAWDZENIA" in zipfile.ZipFile(w3).read("word/comments.xml").decode())
irep = open(os.path.join(d, "rt_back_import.md"), encoding="utf-8").read()
t("import report lists the Word comment; text carries no comment", "DO SPRAWDZENIA: termin" in irep and "<!--" not in open(back3, encoding="utf-8").read(), irep)
b = py(os.path.join(S, "build.py"), back3, "--refs", REFS, "--out", os.path.join(d, "b3"))
t("build passes regardless of comments", b.returncode == 0, b.stdout)

# E16: Word styles are per paragraph — a block of several paragraphs must come back as ONE block (the one title
# note of D12 above all); blocks that are one paragraph each by nature stay separate even when adjacent
mb = os.path.join(d, "multi.md")
MB = ("# Tytuł\n\n::: przypis-tytulowy\nTłumaczenie z języka angielskiego: Anna Nowak.\n\n"
      "Autorka dziękuje recenzentom.\n:::\n\n::: motto\nWers pierwszy.\n\nWers drugi.\n:::\n\n"
      "::: nota\nNota, akapit pierwszy.\n\nNota, akapit drugi.\n:::\n\n::: dialog\nA: Jeden.\n\nB: Dwa.\n:::\n\n"
      "Tekst.[^1]\n\n[^1]: Przypis.\n\n::: podpis\nRyc. 1. Pierwsza.\n:::\n\n::: podpis\nRyc. 2. Druga.\n:::\n\n"
      "::: mowca\nJan Kowalski\nUniwersytet Warszawski\n:::\n\n::: mowca\nAnna Nowak\nUniwersytet Jagielloński\n:::\n")
open(mb, "w", encoding="utf-8").write(MB)
w, back, r = roundtrip(mb, "multi")
bm = open(back, encoding="utf-8").read()
t("E16: multi-paragraph blocks (title note, motto, nota, dialog) come back whole; podpis/mowca stay separate",
  tree(mb) == tree(back), bm)
c = py(os.path.join(S, "check.py"), "--pair", mb, back)
t("E16: pair check after the Word round trip: one title-note block, CHECK OK",
  c.returncode == 0 and bm.count("przypis-tytulowy") == 1, c.stdout + bm)

# a comment between a citation token and punctuation: Word drops the comment, the space before it must go too
# (the build prints "[@key];"); a file exported before the fix still has "[@key] ;": closed up on import
cp = os.path.join(d, "cpunct.md")
open(cp, "w", encoding="utf-8").write("Tekst.[^1] Dalej.[^2]\n\n[^1]: [@ficowski1985, s. 15] <!-- DO SPRAWDZENIA: S2 – strona -->; "
                                      "oryginał: „x”.\n\n[^2]: [@mroz2011] ; stary eksport.\n")
w, back, r = roundtrip(cp, "cpunct")
cb = open(back, encoding="utf-8").read()
t("comment before punctuation: token and punctuation come back together; old-export gap closed on import",
  "[@ficowski1985, s. 15]; oryginał" in cb and "[@mroz2011]; stary" in cb, cb)

n, ok = len(res), sum(res)
print(f"ROUNDTRIP ALL PASS {n}/{n}" if ok == n else f"ROUNDTRIP FAILED {n - ok}/{n}")
