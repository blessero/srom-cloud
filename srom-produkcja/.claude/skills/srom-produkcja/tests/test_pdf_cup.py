"""Cambridge University Press book chapter (stage-1 test 4, 28.09.2026: Ostendorf, "Familiar Outsiders Abroad", in
The Romani Atlantic, CUP 2026, downloaded from Cambridge Core). What broke the extractor there:
- the text layer has no digits and no small capitals: Sabon LT Std old-style figures come as private-use code points
  U+F643–F64C, small capitals as U+F761–F77A (Adobe's legacy PUA); "=" in a URL as "¼" from a TeX math font; a TeX
  accent "Savi´c" (a spacing acute printed over the c). PyMuPDF cannot write such a text layer: tested on
  repair_glyphs() with the character records the extractor reads
- word spaces set as gaps with no space glyph: letterspaced small-caps headings, loosely justified lines where every
  word is its own text object, a figure-font number followed by a word ("1501 letters")
- a chapter numeral set larger than the title above it (the title block must still be front matter, with the author)
- notes with a hanging number and no separator rule: a note running onto the next page opens that page's note zone
  without a number, at the notes' second-line indent (not a quotation at note size)
- a compound broken at its hyphen ("light-" | "brown") where the text has another compound on the same element
  ("dark-brown"): the hyphen stays
Runs with PyMuPDF only."""
import os, re, sys, subprocess, tempfile
import pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "scripts", "pdf_extract.py")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import pdf_extract as P
res = []


def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))


# ---- repair_glyphs on character records (what page_lines reads from rawdict)
def chars(text, x=100.0, w=5.0, gaps=None):
    out = []
    for i, c in enumerate(text):
        x0 = x
        out.append({"c": c, "bbox": (x0, 90.0, x0 + w, 100.0), "origin": (x0, 98.0)})
        x += w + ((gaps or {}).get(i, 0.0))
    return out

P.GLYPHS.clear(); P.PUA_LEFT.clear()
got = "".join(c["c"] for c in P.repair_glyphs(chars(""), "KALMLA+SabonLTStd-Roman+f6", 8.0, 1))
t("Linotype old-style figures U+F643–F64C -> digits (2025)", got == "2025", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars(""), "X+MinionPro-Regular", 8.0, 1))
t("Adobe legacy old-style figures U+F730–F739 -> digits (1501)", got == "1501", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars(""), "KALMLE+SabonLTStd-Roman+f7", 11.0, 1))
t("Adobe legacy small capitals U+F761–F77A -> capitals (INTRO)", got == "INTRO", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars(""), "X+Font", 11.0, 1))
t("accented small capital U+F7E9 -> É", got == "É", got)
# "Savi´c": the acute is set after the i but printed over the c
acute = [{"c": "i", "bbox": (211.4, 568, 213.5, 576), "origin": (211.4, 574)},
         {"c": "´", "bbox": (214.2, 568, 216.3, 576), "origin": (214.2, 574)},
         {"c": "c", "bbox": (213.5, 568, 217.0, 576), "origin": (213.5, 574)}]
got = "".join(c["c"] for c in P.repair_glyphs(acute, "X+SabonLTStd-Roman", 8.0, 1))
t("spacing acute printed over the next letter -> composed (i´c -> ić)", got == "ić", got)
sep = chars("a´ b")
got = "".join(c["c"] for c in P.repair_glyphs(sep, "X+SabonLTStd-Roman", 8.0, 1))
t("spacing acute beside a letter (not over it) is kept", got == "a´ b", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars("¼"), "KALNCJ+TeXCMMathsSymbols", 8.0, 1))
t("'¼' from a TeX math font -> '=' (id¼6 in a Cambridge URL)", got == "=", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars("¼"), "X+SabonLTStd-Roman", 8.0, 1))
t("'¼' from a text font stays ¼", got == "¼", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars("1000 bce"), "Sabon-RomanSC", 10.0, 1))
t("a small-capitals font's lower case -> capitals (1000 bce -> 1000 BCE, Manchester UP)", got == "1000 BCE", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars("Ibce"), "ABCDEF+MinionPro-RegularSC", 10.0, 1))
t("… also behind a subset prefix (ABCDEF+MinionPro-RegularSC)", got == "IBCE", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars("disc"), "X+Sabon-Roman", 10.0, 1))
t("a text font's lower case stays", got == "disc", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars("disc"), "TimesNewRomanPSMT", 10.0, 1))
t("… also a font without subset prefix whose name does not end in SC", got == "disc", got)
got = "".join(c["c"] for c in P.repair_glyphs(chars("IBERIANATLANTIC", w=6.0, gaps={6: 3.9}), "X+SabonLTStd-Roman+f7", 11.0, 1))
t("word space set as a gap inside a span (letterspaced heading) -> space", got == "IBERIAN ATLANTIC", got)
P.repair_glyphs(chars("xy"), "X+Font", 10.0, 7)
t("a private-use glyph no table explains is recorded (-> an issue in the report)",
  len(P.PUA_LEFT) == 1 and P.PUA_LEFT[0][0] == 7 and "U+E123" in P.PUA_LEFT[0][1], P.PUA_LEFT)

# ---- a hand-set chapter: 2 pages
FB = {"rg": pymupdf.Font("tiro"), "it": pymupdf.Font("tiit"), "bo": pymupdf.Font("tibo")}
doc = pymupdf.open()
W, H = 430, 650
BS, NS, LEAD, NLEAD = 10.0, 8.0, 13, 10
X0, MEAS = 60, 300


def page():
    pg = doc.new_page(width=W, height=H)
    for k, f in FB.items():
        pg.insert_font(fontname=k, fontbuffer=f.buffer)
    return pg


def put(pg, x, y, txt, fn="rg", fs=BS):
    pg.insert_text((x, y), txt, fontname=fn, fontsize=fs)
    return x + FB[fn].text_length(txt, fontsize=fs)


def spread(pg, y, words, fs=BS, x=X0, meas=MEAS):
    """a justified line with every word its own text object and no space glyph between them"""
    wid = sum(FB["rg"].text_length(w, fontsize=fs) for w in words)
    gap = (meas - wid) / (len(words) - 1)
    for w in words:
        x = put(pg, x, y, w, fs=fs) + gap


FILL = ("the racial matrix bound people together across the ocean and its ports while ideas moved with ships and "
        "letters between the colonies and the old world " * 12).split()
_k = [0]


def line(pg, y, width=MEAS, x=X0, end=""):
    out = []
    while FB["rg"].text_length(" ".join(out + [FILL[_k[0] % len(FILL)]]) + end, fontsize=BS) < width - 6:
        out.append(FILL[_k[0] % len(FILL)]); _k[0] += 1
    put(pg, x, y, " ".join(out) + end)


p1 = page()
put(p1, 205, 60, "3", fs=15)                                      # chapter numeral, larger than the title
put(p1, 120, 95, "Familiar Outsiders Abroad", fn="bo", fs=13)
put(p1, 90, 115, "Relational Racialization in the Atlantic World", fn="it", fs=13)
put(p1, 170, 140, "Ann Author", fs=12)
x = 170
for w in ("INTRODUCTION",):
    x = put(p1, x, 180, w, fs=11)
y = 200
line(p1, y, x=X0 + 12); y += LEAD
for _ in range(3):
    line(p1, y); y += LEAD
x = put(p1, X0, y, "global practices in general.")
x = put(p1, x, y - 3.5, "1", fs=7)
put(p1, x + 3, y, "Race was scripted relationally, and this")
y += LEAD
spread(p1, y, ["In", "Spain,", "this", "veil", "expressed", "itself", "in", "practical", "ways."]); y += LEAD
x = put(p1, X0, y, "two")
x = put(p1, x + 3, y, "1501")                                      # a number, then a word with no space glyph
put(p1, x + 3, y, "letters by the ambassador, others dark-brown, others light-")
y += LEAD
put(p1, X0, y, "brown. The ambassador wrote of colour, figure and stature, and of the likeness he saw."); y += LEAD + 4
x = put(p1, X0 + 12, y, "A second paragraph begins here and runs on")
x = put(p1, x, y - 3.5, "2", fs=7)
put(p1, x + 2, y, ".")
# notes: number hanging at X0, text at X0+7; no separator rule; note 1 runs onto page 2
ny = 520
put(p1, X0, ny, "1", fs=NS * 0.7)
put(p1, X0 + 7, ny, "Margareta Matache, The Permanence of Anti-Roma Racism (Routledge, 2026);", fs=NS); ny += NLEAD
put(p1, X0 + 7, ny, "Jelena Savic, “Gadjo Supremacy and Gadjo Privileges,”", fs=NS)
put(p1, 205, 600, "86", fs=9)
p2 = page()
y = 60
for _ in range(8):
    line(p2, y); y += LEAD
put(p2, X0, y, "the end of the section."); y += 2 * LEAD
x = 160
for w in ("IBERIAN", "ATLANTIC"):                                  # the text's heading style again
    x = put(p2, x, y, w, fs=11) + 4
y += 2 * LEAD
line(p2, y, x=X0 + 12); y += LEAD
for _ in range(8):
    line(p2, y); y += LEAD
ny = 480
put(p2, X0 + 7, ny, "Conference Paper presented at the Critical Approaches Conference, 2022;", fs=NS); ny += NLEAD
put(p2, X0 + 7, ny, "Noemie Ndiaye, “Black Roma,” Renaissance Quarterly 75 (2022): 1266–302.", fs=NS); ny += NLEAD
put(p2, X0, ny, "2", fs=NS * 0.7)
put(p2, X0 + 7, ny, "Klaus-Michael Bogdal, Europe and the Roma (Penguin, 2023).", fs=NS)
put(p2, 205, 600, "87", fs=9)

tmp = tempfile.mkdtemp()
pdf = os.path.join(tmp, "cup.pdf")
doc.save(pdf)
out = os.path.join(tmp, "cup.md")
r = subprocess.run([sys.executable, EX, pdf, "-o", out], capture_output=True, text=True)
md = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
front = open(os.path.join(tmp, "cup_front.md"), encoding="utf-8").read() if os.path.exists(os.path.join(tmp, "cup_front.md")) else ""
rep = open(os.path.join(tmp, "cup_extract.md"), encoding="utf-8").read() if os.path.exists(os.path.join(tmp, "cup_extract.md")) else ""
t("extracts: EXTRACT OK, 2 notes, 2 markers", "EXTRACT OK" in r.stdout and "notes 2 · markers 2" in r.stdout, r.stdout + r.stderr)
t("a chapter numeral set larger than the title: title, subtitle and author are front matter",
  "Familiar Outsiders Abroad" in front and "Ann Author" in front and "Familiar" not in md and "Ann Author" not in md,
  front + "\n---\n" + md[:300])
t("the text's headings stay in the text (a second one set with a gap for its word space)",
  md.startswith("# INTRODUCTION") and "\n# IBERIAN ATLANTIC" in md, md[:200])
t("words set as separate objects with no space glyph -> spaced", "In Spain, this veil expressed itself in practical ways." in md, md)
t("a number and the next word with no space glyph -> spaced (1501 letters)", "two 1501 letters" in md, md)
t("a gap-inserted space is listed in the report", "word space set as a gap between text objects" in rep, rep)
t("marker after the gap: '[^1] Race' (the space kept)", "general.[^1] Race was" in md, md)
n1 = re.search(r"^\[\^1\]: (.*)$", md, re.M)
t("a note running onto the next page (no rule, no number, at the notes' second-line indent) continues it",
  n1 is not None and "Privileges,” Conference Paper presented" in n1.group(1) and "1266–302" in n1.group(1)
  and not re.search(r"^> Conference", md, re.M), md)
t("the continuation is listed", "note zone opens without a number after a note ending mid-sentence" in rep, rep)
t("'light-' | 'brown' with 'dark-brown' in the text: hyphen kept, listed",
  "light-brown" in md and "compound like 'dark-brown'" in rep, rep)

n, ok = len(res), sum(res)
print(f"PDF-CUP ALL PASS {n}/{n}" if ok == n else f"PDF-CUP FAILED {n - ok}/{n}")
sys.exit(0 if ok == n else 1)
