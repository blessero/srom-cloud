"""Second journal layout (stage-1 test 28.09.2026: Pahulich, Critical Romani Studies 8/1, 2025). A hand-set PDF
reproduces what broke the extractor there:
- page 1 only title, author, e-mail, affiliation, bio; page 2 an "Abstract" with a "Keywords" box in a column
  beside it (baselines a few points off the abstract's); the text begins on page 3 under "Introduction"
- note markers as bracketed superscripts "[1]"; notes at 8 pt under a short rule, the reference list at 9 pt
  (more text at 9 pt than at 8: the note size must come from the rule, not from frequency)
- the repeated author in the reference list drawn as a rule, not typed ("———. 2008.")
- line-end hyphens before a capital (anti-|Roma, Polish-|Lithuanian) and slashes at a line end (police/|carceral)
- a block quotation indented on the left only, set full out to the right margin
Runs with PyMuPDF only."""
import os, re, sys, subprocess, tempfile
import pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "scripts", "pdf_extract.py")
res = []

def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

FB = {"rg": pymupdf.Font("tiro"), "it": pymupdf.Font("tiit")}
doc = pymupdf.open()
W, H = 499, 709
LM, RM = 42.5, 456.4
BS, NS, RS = 10.0, 8.0, 9.0        # body, notes, reference list

def page():
    pg = doc.new_page(width=W, height=H)
    for k, f in FB.items():
        pg.insert_font(fontname=k, fontbuffer=f.buffer)
    return pg

def put(pg, x, y, txt, fn="rg", fs=BS):
    pg.insert_text((x, y), txt, fontname=fn, fontsize=fs)
    return x + FB[fn].text_length(txt, fontsize=fs)

WORDS = ("the old road ran on past the mill and the field and all of us went on with it day by day " * 40).split()

def line_to(end, width=RM - LM, fs=BS, start=0):
    words = []
    for w in WORDS[start:]:
        if FB["rg"].text_length(" ".join(words + [w, end]), fontsize=fs) > width:
            break
        words.append(w)
    return " ".join(words + [end])

def folio(pg, n):
    put(pg, 50, 690, "Critical Test Studies", fs=11)
    put(pg, 16, 690, str(n), fs=11)

# page 1: front matter only
p1 = page()
put(p1, 43, 156, "Racialization of Tests, Modernity,", fs=22)
put(p1, 43, 181, "and the Entanglement of Fixtures", fs=22)
put(p1, 78, 245, "Anna Nowak", fs=18)
put(p1, 78, 263, "anna@example.org")
put(p1, 78, 290, "University of Nowhere, Postdoctoral Fellow")
x = put(p1, 78, 349, "Anna Nowak", "it"); put(p1, x, 349, " is a scholar of tests from Nowhere. She holds a PhD in")
put(p1, 78, 365, "fixtures and writes about the old road and the mill.")
put(p1, 78, 684, "Vol. 1. No. 1. 2025, 1–4 • DOI: 10.0000/test.1")

# page 2: abstract (left) and a keywords box (right), baselines 2-3 pt apart
p2 = page()
put(p2, 42.5, 114, "Abstract", fs=18)
ab = ["The article explores how the old road ran on past the mill",
      "and the field, and how all of us went on with it day by day",
      "and the field, and how all of us went on with it day by day",
      "and the field, and how all of us went on with it day by day",
      "and the field, and how all of us went on with it day by day",
      "and the field, and how all of us went on with it day by day",
      "and the field, and how all of us went on with it day by day",
      "and the field, and how all of us went on with it day by day",
      "until the mill stood still and the field was quiet again."]
for j, l in enumerate(ab):
    put(p2, 42.5, 141 + 13.5 * j, l)
put(p2, 351.5, 138, "Keywords", fs=18)
for j, k in enumerate(["Anti-Test racism", "Fixture Theory", "Eastern Mills", "Racial Roads"]):
    put(p2, 351.5, 156.3 + 13.5 * j, "•")
    put(p2, 368.5, 156.3 + 13.5 * j, k)

# page 3: the text; bracketed superscript marker; hyphen before a capital; slash at a line end; block quote; note
p3 = page()
folio(p3, 3)
put(p3, 42.5, 87, "Introduction", fs=18)
y = 124
x = put(p3, LM, y, "Scholars note that the road ran on (Smith 2000).")
put(p3, x + 0.5, y - 3.5, "[1]", fs=5.83)
put(p3, x + 9, y, " " + line_to("anti-", RM - x - 12))
y += 13.5; put(p3, LM, y, "Roma " + line_to("Polish-", RM - LM - 30, start=5))
y += 13.5; put(p3, LM, y, "Lithuanian lands " + line_to("police/", RM - LM - 80, start=9))
y += 13.5; put(p3, LM, y, "carceral state ran on day by day.")
y += 27; put(p3, LM, y, "As Smith writes:")
y += 27
put(p3, 90.7, y, line_to("on", 458.6 - 90.7, start=11)); y += 13.5
put(p3, 90.7, y, line_to("on", 458.6 - 90.7, start=22)); y += 13.5
put(p3, 90.7, y, "and so it went (2000, 12)."); y += 13.5
y += 13.5; put(p3, LM, y, "After the quotation the text goes on to its end here.")
p3.draw_line((42.5, 585.6), (114.5, 585.6), width=0.3)
put(p3, 42.5, 605, "1 A note set at eight points under a short rule, with a", fs=NS)
put(p3, 42.5, 616, "second line of the same note.", fs=NS)

# page 4: reference list at 9 pt with a drawn repeated-author rule (more 9-pt text than 8-pt notes)
p4 = page()
folio(p4, 4)
put(p4, 42.5, 87, "References", fs=18)
y = 112
refs = [("Achim, Viorel. 2004. ", "The Roma in Romanian History", ". Budapest: CEU Press."),
        ("Hancock, Ian. 1987. ", "The Pariah Syndrome", ". Ann Arbor: Karoma."),
        (None, "", ". 2008. “The ‘Gypsy’ Stereotype.” In Gypsies in Literature, 181–191. New York: Palgrave."),
        ("Smith, John. 2000. ", "A Long Book About the Old Road and the Mill and the Field", ". London: Road Press, and "
         "a further line of it.")]
for a, it, rest in refs:
    if a is None:
        p4.draw_line((42.5, y - 3.1), (66.9, y - 3.1), width=0.28)
        put(p4, 66.9, y, rest, fs=RS)
    else:
        x = put(p4, 42.5, y, a, fs=RS); x = put(p4, x, y, it, "it", RS); put(p4, x, y, rest, fs=RS)
    y += 17.5
put(p4, 42.5, y, "Matache, Margareta. 2020. “Reparations.” Al Jazeera, 5 October. https://www.ex.org/a/?fbclid=IwAR16IM_B7KnIs", fs=RS)
put(p4, 53.9, y + 11.8, "NIMuUPdg.", fs=RS)
p4.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(300, y - 9, 456, y + 14), "uri": "https://www.ex.org/a/?fbclid=IwAR16IM_B7KnIsNIMuUPdg"})
y += 29.3
for j in range(8):                              # enough 9-pt text to outweigh the notes
    put(p4, 42.5, y, f"Zed{j}, Adam. 2001. A Title Long Enough to Fill a Line of the Reference List Here. Oxford: OUP.", fs=RS)
    y += 17.5

d = tempfile.mkdtemp()
pdf = os.path.join(d, "crs.pdf"); doc.save(pdf)
out = os.path.join(d, "c.md")
r = subprocess.run([sys.executable, EX, pdf, "-o", out], capture_output=True, text=True)
rd = lambda f: open(os.path.join(d, f), encoding="utf-8").read() if os.path.exists(os.path.join(d, f)) else ""
md, rep, front = rd("c.md"), rd("c_extract.md"), rd("c_front.md")
bib = rd("c_bib.txt").splitlines()
D = r.stdout + r.stderr + "\n" + md

t("EXTRACT OK", "EXTRACT OK" in r.stdout, D + rep)
t("text begins with the first heading after the abstract/keywords section", md.startswith("# Introduction\n"), D)
t("pages 1-2 out of the text", not re.search(r"Abstract|Keywords|anna@example|Postdoctoral|DOI|scholar of tests", md), D)
fp = front.split("\n\n")
t("front matter: title, author, e-mail, affiliation, bio, journal line, in order",
  fp[:4] == ["Racialization of Tests, Modernity, and the Entanglement of Fixtures", "Anna Nowak", "anna@example.org",
             "University of Nowhere, Postdoctoral Fellow"] and fp[4].startswith("*Anna Nowak* is a scholar")
  and fp[5].startswith("Vol. 1. No. 1."), front)
t("abstract whole, not interleaved with the keywords box beside it",
  "Abstract\n\nThe article explores how the old road ran on past the mill and the field" in front
  and "day by day until the mill stood still and the field was quiet again." in front, front)
t("keywords: one per paragraph, after the abstract", "Keywords\n\n• Anti-Test racism\n\n• Fixture Theory\n\n• Eastern Mills\n\n• Racial Roads" in front, front)
t("front matter columns: a warning, not an issue", "two columns in the front matter" in rep and "two columns?" not in rep, rep)
t("bracketed superscript marker [1] -> [^1]", "(Smith 2000).[^1] " in md and "[1]" not in md, D)
t("note at 8 pt under the rule (reference list at 9 pt is not the note size)",
  "[^1]: A note set at eight points under a short rule, with a second line of the same note." in md, D)
t("line-end hyphen before a capital kept, no space: anti-|Roma, Polish-|Lithuanian",
  "anti-Roma " in md and "Polish-Lithuanian lands" in md and "- R" not in md and "- L" not in md, D)
t("slash at a line end joined without a space: police/|carceral", "police/carceral state" in md, D)
t("block quotation indented left only, full out right -> >", re.search(r"^> and all of us .* and so it went \(2000, 12\)\.$", md, re.M) is not None, D)
t("text after the quotation is a paragraph", "\n\nAfter the quotation the text goes on to its end here.\n" in md, D)
t("reference list: drawn rule -> repeated author, one entry per line",
  bib[:3] == ["Achim, Viorel. 2004. The Roma in Romanian History. Budapest: CEU Press.",
              "Hancock, Ian. 1987. The Pariah Syndrome. Ann Arbor: Karoma.",
              "Hancock, Ian. 2008. “The ‘Gypsy’ Stereotype.” In Gypsies in Literature, 181–191. New York: Palgrave."]
  and len(bib) == 13 and "repeated author" in rep, bib)
t("URL broken inside a token (no hyphen) joined when the link target has no space there",
  bib[4:5] == ["Matache, Margareta. 2020. “Reparations.” Al Jazeera, 5 October. https://www.ex.org/a/?fbclid=IwAR16IM_B7KnIsNIMuUPdg."]
  and "joined (link target)" in rep, bib)
t("reference list out of the text", "References" not in md and "Achim" not in md, D)
t("running footer dropped", "Critical Test Studies" not in md, D)

n, ok = len(res), sum(res)
print(f"PDF-CRS ALL PASS {n}/{n}" if ok == n else f"PDF-CRS FAILED {n - ok}/{n}")
