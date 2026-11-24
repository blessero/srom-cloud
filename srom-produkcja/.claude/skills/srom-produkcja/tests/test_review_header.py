"""Review header (Kanon § 1 Nagłówek recenzji, 15.11.2026; C55 item 2, review 18.11.2026): a ::: recenzja block in SROM-MD is
built into five paragraphs in one style (review_header), the author line bold, the title italic; a missing or malformed
element (author, italic title, publisher place year, ss. pages, ISBN with a valid check digit) fails the build. The style is
in config, spec, setup script and template, and the block survives the Word working copy."""
import json, os, re, sys, subprocess, tempfile, zipfile
from lxml import etree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, FX = os.path.join(ROOT, "scripts"), os.path.join(ROOT, "tests", "fixtures")
REFS = os.path.join(FX, "kanon_refs.json")
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1200]))
def py(*a):
    return subprocess.run([sys.executable, *a], capture_output=True, text=True)

cfg = json.load(open(os.path.join(ROOT, "config", "styles.json"), encoding="utf-8"))
spec = json.load(open(os.path.join(ROOT, "indesign", "style_spec.json"), encoding="utf-8"))
NAME = cfg["paragraph"].get("review_header")
P = {p["name"]: p for p in spec["paragraph"]}
t("config: review_header names a spec style at the root", NAME in P and P[NAME]["group"] == "", NAME)
def eff(n):
    out, chain = {}, []
    while n: chain.append(n); n = P[n]["basedOn"]
    for n in reversed(chain): out.update(P[n]["props"])
    return out
e, grid = eff(NAME), spec["document"]["grid"]["baselineDivision"]
t("style = vol. 18 header: 10.5/13 on the grid, indent 44 mm, 3 grid lines before and after, none inside, left, no hyphenation",
  (e["pointSize"], e["leading"], e["gridAlignment"], round(e["leftIndent"] / 72 * 25.4, 1), round(e["spaceBefore"] / grid, 3),
   round(e["spaceAfter"] / grid, 3), e["sameParaStyleSpacing"], e["firstLineIndent"], e["justification"], e["hyphenation"])
  == (10.5, 13, "ALIGN_BASELINE", 44.0, 3.0, 3.0, 0, 0, "LEFT_ALIGN", False), e)
jsx = open(os.path.join(ROOT, "indesign", "srom_style_setup.jsx"), encoding="utf-8").read()
t("setup script defines the style", json.dumps(NAME)[1:-1] in jsx or NAME in jsx)

# the template carries every spec paragraph style, and the new one with the spec's values
z = zipfile.ZipFile(os.path.join(ROOT, "indesign", "SROM_szablon_v3.idml"))
t("template: mimetype first and stored (a valid IDML package)", z.infolist()[0].filename == "mimetype" and z.infolist()[0].compress_type == zipfile.ZIP_STORED)
st = etree.fromstring(z.read("Resources/Styles.xml"))
tn = {x.get("Name").split(":")[-1]: x for x in st.iter("ParagraphStyle")}
t("template: every spec paragraph style is present", not [n for n in P if n not in tn], [n for n in P if n not in tn])
x = tn.get(NAME)
ok = x is not None and x.findtext("Properties/BasedOn") == "ParagraphStyle/" + P[NAME]["basedOn"] \
    and abs(float(x.get("LeftIndent")) - e["leftIndent"]) < 1e-6 and abs(float(x.get("SpaceBefore")) - e["spaceBefore"]) < 1e-6 \
    and abs(float(x.get("SpaceAfter")) - e["spaceAfter"]) < 1e-6 and x.findtext("Properties/SameParaStyleSpacing") == "0" \
    and x.get("Justification") == "LeftAlign" and x.get("Hyphenation") == "false" and x.get("KeepWithNext") == str(P[NAME]["props"]["keepWithNext"])
t("template: the review-header style has the spec's values", ok, None if x is None else x.attrib)

# build
d = tempfile.mkdtemp()
sub = os.path.join(d, "refs_sub.json")
json.dump([r for r in json.load(open(REFS, encoding="utf-8")) if r["id"] == "ficowski1985"], open(sub, "w", encoding="utf-8"), ensure_ascii=False)
GOOD = ["Markéta Hajská", "*The Stojka Family. Spatial Mobility and Territorial Anchoredness of Lovara Vlax Roms in the Former Czechoslovakia*",
        "Karolinum Press, Praga 2025", "ss. 280", "ISBN 978-80-246-5917-6"]
def md(name, lines, sep="\n\n"):
    p = os.path.join(d, name + ".md")
    open(p, "w", encoding="utf-8").write("::: recenzja\n" + sep.join(lines) + "\n:::\n\nMonografia[^1] jest ważna.\n\nDrugi akapit.\n\n"
                                         "[^1]: [@ficowski1985, s. 15].\n")
    return p
def build(p):
    out = os.path.join(d, os.path.basename(p) + "_out")
    r = py(os.path.join(S, "build.py"), p, "--refs", sub, "--out", out)
    stem = os.path.splitext(os.path.basename(p))[0]
    rp = os.path.join(out, stem + "_report.md")
    return r.returncode, (open(rp, encoding="utf-8").read() if os.path.exists(rp) else "") + r.stdout + r.stderr, os.path.join(out, stem + ".docx")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
def paras(docx):
    from docx import Document
    doc = Document(docx)
    return [(p.style.name, p.text, [(r.style.name if r.style is not None else None, r.text) for r in p.runs]) for p in doc.paragraphs]

code, rep, dx = build(md("good", GOOD))
t("a complete header: build PASSES", code == 0, rep[-1500:])
ps = paras(dx) if code == 0 else []
head = [p for p in ps if p[0] == NAME]
t("five paragraphs in the review-header style, in order", [p[1] for p in head] == [re.sub(r"\*", "", g) for g in GOOD], head)
t("author line in the bold character style (Pogrubienie)", head and all(r[0] == cfg["character"]["speaker"] for r in head[0][2] if r[1].strip()), head[:1])
t("title in Kursywa", len(head) > 1 and any(r[0] == cfg["character"]["italic"] for r in head[1][2]), head[1:2])
after = ps[len(head)] if len(ps) > len(head) else None
t("the first body paragraph after the header is unindented (body_first)", after and after[0] == cfg["paragraph"]["body_first"], after)

code, rep, dx = build(md("lines", GOOD, sep="\n"))
t("one element per line of one paragraph works the same", code == 0 and len([p for p in paras(dx) if p[0] == NAME]) == 5, rep[-800:])
code, rep, _ = build(md("isbn10", GOOD[:4] + ["ISBN 0-8044-2957-X"]))
t("a valid ISBN-10 with X passes", code == 0, rep[-800:])

def fails(name, lines, needle):
    code, rep, _ = build(md(name, lines))
    t(f"fails: {name}", code != 0 and needle in rep, rep[-1000:])
fails("no_isbn", GOOD[:4], "five expected")
fails("bad_check_digit", GOOD[:4] + ["ISBN 978-80-246-5917-5"], "ISBN check digit wrong")
fails("title_not_italic", [GOOD[0], GOOD[1].strip("*")] + GOOD[2:], "title in italics")
fails("no_year", GOOD[:2] + ["Karolinum Press, Praga"] + GOOD[3:], "publisher, place year")
fails("no_pages", GOOD[:3] + ["280 stron"] + GOOD[4:], "ss. <pages>")

# Word working copy round trip keeps the block
good = os.path.join(d, "good.md")
w = os.path.join(d, "good_robocza.docx")
r1 = py(os.path.join(S, "export_work.py"), good, "-o", w)
back = os.path.join(d, "good_back.md")
r2 = py(os.path.join(S, "docx_in.py"), w, "-o", back)
bt = open(back, encoding="utf-8").read() if os.path.exists(back) else r1.stderr + r2.stderr
t("Word working copy round trip: one ::: recenzja block with the five elements", bt.count("::: recenzja") == 1 and all(g.strip("*")[:20] in bt for g in GOOD), bt[:700])
code, rep, _ = build(back)
t("the round-tripped file builds", code == 0, rep[-800:])
lw = os.path.join(d, "lines_robocza.docx")
py(os.path.join(S, "export_work.py"), os.path.join(d, "lines.md"), "-o", lw)
lb = os.path.join(d, "lines_back.md")
py(os.path.join(S, "docx_in.py"), lw, "-o", lb)
code, rep, _ = build(lb)
t("round trip of the one-paragraph form keeps the five lines", code == 0, rep[-800:])

n, ok = len(res), sum(res)
print(f"REVIEW_HEADER ALL PASS {n}/{n}" if ok == n else f"REVIEW_HEADER FAILED {n - ok}/{n}")
sys.exit(0 if ok == n else 1)
