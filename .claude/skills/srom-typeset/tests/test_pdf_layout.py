"""Journal-layout PDF (the first real stage-1 test, 27.09.2026: an English humanities journal set by a
typesetting system, not by Word). A hand-set 3-page PDF reproduces what broke the extractor there:
- italic font known only by an obfuscated name with a style suffix (AdvOTa14f9db0.I+20)
- a note's number and first words on a raised baseline, the rest of its first line lower ("2 Smith, 35" / "–69.")
- a note whose whole first line, number included, sits on one baseline (number only smaller)
- a superscript ("XVIIᵉ") inside a note line
- section headings in capitals *smaller* than the body; a two-line one
- opening words in small capitals; title, author and abstract on page 1; an unnumbered title note
- verse quoted line by line; a figure caption interrupting a paragraph; a reference list at note size
- line-end hyphens after "prefixes" that are not prefixes there (pro-|duction), closed em dash at a line end
Runs with PyMuPDF only (no LibreOffice)."""
import os, re, sys, subprocess, tempfile
import pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "scripts", "pdf_extract.py")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import pdf_extract as P
res = []

def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

# ---- font names
t("italic by style suffix: AdvOTa14f9db0.I+20", P.is_italic({"font": "AdvOTa14f9db0.I+20", "flags": 4}))
t("italic by style suffix: AdvOTa14f9db0.I", P.is_italic({"font": "AdvOTa14f9db0.I", "flags": 4}))
t("roman obfuscated name not italic: AdvOT635f2c37+20", not P.is_italic({"font": "AdvOT635f2c37+20", "flags": 4}))
t("bold by style suffix: AdvOTx.B, not italic", P.is_bold({"font": "AdvOTx.B", "flags": 4}) and not P.is_italic({"font": "AdvOTx.B", "flags": 4}))
t("italic suffix is not bold", not P.is_bold({"font": "AdvOTa14f9db0.I", "flags": 4}))

# ---- the PDF
FB = {"rg": pymupdf.Font("tiro"), "it": pymupdf.Font("tiit")}
doc = pymupdf.open()
W, H = 432, 666
LM, RM = 48, 372          # text block
BS, NS = 10.8, 9.0        # body, notes

def page():
    pg = doc.new_page(width=W, height=H)
    for k, f in FB.items():
        pg.insert_font(fontname=k, fontbuffer=f.buffer)
    return pg

def put(pg, x, y, txt, fn="rg", fs=BS):
    pg.insert_text((x, y), txt, fontname=fn, fontsize=fs)
    return x + FB[fn].text_length(txt, fontsize=fs)

def fill(words, width, fs=BS):
    """greedy lines of short words, each within a few points of the measure (so none looks 'short')"""
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if FB["rg"].text_length(cand, fontsize=fs) > width:
            lines.append(cur); cur = w
        else:
            cur = cand
    return lines, cur

def line_to(end, width=RM - LM, fs=BS):
    """a full-measure line that ends with `end`"""
    words = []
    for w in WORDS:
        if FB["rg"].text_length(" ".join(words + [w, end]), fontsize=fs) > width:
            break
        words.append(w)
    return " ".join(words + [end])

WORDS = ("the old road ran on past the mill and the field and all of us went on with it day by day " * 12).split()

# page 1: title, author, abstract, caps heading, small-caps opener, marker 1, title note, note 1 (raised start)
p1 = page()
put(p1, 70, 80, "A Test Title for Stage One", fs=16)
x = put(p1, 110, 110, "ANNA NOWAK", fs=8); put(p1, x, 110, ", University of Nowhere", "it", NS)
put(p1, LM, 140, "This abstract is set in italics at the note size", "it", NS)
put(p1, LM, 152, "and it runs on to a second line of its own.", "it", NS)
put(p1, 170, 190, "INTRODUCTION", fs=10.5)
x = put(p1, LM, 210, "THIS ESSAY BEGINS", fs=9)
body, rest = fill(WORDS[:60], RM - x - 4)
put(p1, x, 210, " " + body[0])
y = 223
more, rest = fill(WORDS[len(body[0].split()):80], RM - LM)
for ln in more:
    put(p1, LM, y, ln); y += 13
x = put(p1, LM, y, line_to("so it all"))
put(p1, x + 0.5, y - 3.3, "1", fs=7.6)
last_body_y = y
put(p1, LM, last_body_y + 32, "I owe many thanks to my colleagues for their help, and to the", fs=NS)
put(p1, LM, last_body_y + 44, "reviewers for their generous reading.", fs=NS)
x = put(p1, 60, last_body_y + 58, "1", fs=6.4)
x = put(p1, x, last_body_y + 58, " Smith, 35", fs=NS)
put(p1, x, last_body_y + 62, "–69; the pro-", fs=NS)
put(p1, LM, last_body_y + 74, "duction of the text was slow, see https://www.example.org/", fs=NS)
put(p1, LM, last_body_y + 86, "2018/feb/old-road-and-the-mill-", fs=NS)
put(p1, LM, last_body_y + 98, "and-the-field.", fs=NS)
for yy in (74, 86, 98):
    p1.insert_link({"kind": pymupdf.LINK_URI, "uri": "https://www.example.org/2018/feb/old-road-and-the-mill-and-the-field",
                    "from": pymupdf.Rect(LM, last_body_y + yy - 9, RM, last_body_y + yy + 2)})
put(p1, LM, last_body_y + 140, "Test Journal 12 (2020): 1–30 © The Author(s), 2020. doi: 10.1234/tj.2020.1", fs=NS)

# page 2: running head, paragraph continued from page 1, two-line caps heading, verse with marker 2,
# notes 2 (whole first line on one baseline) and 3 (raised start + superscript e)
p2 = page()
put(p2, 150, 54, "TEST JOURNAL", fs=8)
y = 78
cont, _ = fill(WORDS[80:130], RM - LM)
for ln in cont[:3]:
    put(p2, LM, y, ln); y += 13
put(p2, LM, y, line_to("of intrigue—")); y += 13
put(p2, LM, y, "and more production here, and the end."); y += 13
y += 20
put(p2, 90, y, "SECOND PART: A LONG HEADING", fs=10.5); y += 13
put(p2, 150, y, "IN CAPITALS", fs=10.5); y += 20
for ln in fill(WORDS[130:170], RM - LM - 16)[0][:2]:
    put(p2, LM, y, ln); y += 13
put(p2, LM, y, "and so the old song says of it:"); y += 19
verse = ["Dark goddess whose splendor", "Burns with the force of suns:", "Snow cannot rival her", "And ebony triumphs over ivory."]
for i, v in enumerate(verse):
    x = put(p2, 72, y, v, fs=10)
    if i == len(verse) - 1:
        put(p2, x + 0.5, y - 3.3, "2", fs=7.6)
    y += 13
y += 6
put(p2, 60, y, "And the text goes on after the verse to the end of the page.")
ny = 540
put(p2, 60, ny, "2", fs=6.4)
put(p2, 64, ny, " Whole first line on one baseline, number only smaller,", fs=NS)
put(p2, LM, ny + 12, "and a second line of the same note.", fs=NS)
x = put(p2, 60, ny + 20, "3", fs=6.4)
x = put(p2, x, ny + 20, " Asséo,", fs=NS)
x2 = put(p2, x, ny + 24, " 1974: “Le XVII", fs=NS)
x2 = put(p2, x2, ny + 24, " ", fs=3)          # kerning space in the small size, on the baseline
x3 = put(p2, x2, ny + 20, "e", fs=6.4)
put(p2, x3, ny + 24, " siècle”.", fs=NS)

# page 3: marker 3 in a paragraph interrupted by a figure caption, then BIBLIOGRAPHY at note size
p3 = page()
put(p3, 150, 54, "TEST JOURNAL", fs=8)
y = 78
para, _ = fill(WORDS[170:250], RM - LM)
put(p3, 60, y, para[0]); y += 13
for ln in para[1:3]:
    put(p3, LM, y, ln); y += 13
x = put(p3, LM, y, para[3]); put(p3, x + 0.5, y - 3.3, "3", fs=7.6)
y += 30
put(p3, LM, y, "Figure 1. A drawing of the old road, 1631. Private collection.", fs=NS)
y += 30
put(p3, LM, y, "after the figure the same sentence goes on and ends here."); y += 30
put(p3, 175, y, "BIBLIOGRAPHY", fs=10.5); y += 18
put(p3, LM, y, "Acton, Thomas. Gypsy Politics and Social Change. London: Routledge", fs=NS); y += 12
put(p3, 60, y, "and Kegan Paul, 1974.", fs=NS); y += 12
put(p3, LM, y, "Fraser, Angus. The Gypsies. Oxford: Blackwell, 1992. https://www.gyp-", fs=NS); y += 12
put(p3, 60, y, "sylore.org/fraser.html.", fs=NS); y += 12
for yy in (y - 24, y - 12):
    p3.insert_link({"kind": pymupdf.LINK_URI, "uri": "https://www.gypsylore.org/fraser.html", "from": pymupdf.Rect(LM, yy - 9, RM, yy + 2)})
put(p3, LM, y, "Galland, Nora. Name-Calling. Shakespeare en devenir 12 (2017): https://www.ex.org/i.php?id¼12.", fs=NS)
p3.insert_link({"kind": pymupdf.LINK_URI, "uri": "https://www.ex.org/i.php?id=12", "from": pymupdf.Rect(LM, y - 9, RM, y + 2)}); y += 12

d = tempfile.mkdtemp()
pdf = os.path.join(d, "journal.pdf"); doc.save(pdf)
out = os.path.join(d, "j.md")
r = subprocess.run([sys.executable, EX, pdf, "-o", out], capture_output=True, text=True)
md = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
rep = open(os.path.join(d, "j_extract.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "j_extract.md")) else ""
front = open(os.path.join(d, "j_front.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "j_front.md")) else ""
bib = open(os.path.join(d, "j_bib.txt"), encoding="utf-8").read().splitlines() if os.path.exists(os.path.join(d, "j_bib.txt")) else []
D = md + "\n---REPORT---\n" + rep + r.stdout + r.stderr

notes = {m.group(1): m.group(2) for m in re.finditer(r"^\[\^(\d+)\]:\s*(.+)$", md, re.M)}
t("EXTRACT OK, 3 notes, 3 markers in order", "EXTRACT OK" in r.stdout and sorted(notes) == ["1", "2", "3"]
  and re.findall(r"\[\^(\d+)\](?!:)", md) == ["1", "2", "3"], D)
t("URL broken after a slash: no space; after a hyphen: hyphen kept and listed",
  "https://www.example.org/2018/feb/old-road-and-the-mill-and-the-field." in notes.get("1", "")
  and "URL" in rep and "hyphen kept (link target)" in rep, D)
t("block set apart below the notes (journal, licence, DOI) not in the last note; page 1: with the front matter",
  "doi" not in notes.get("1", "") and "Test Journal 12 (2020)" in front and "set apart below the notes" in rep, D + front)
t("raised note start joined without a space: 'Smith, 35–69'", notes.get("1", "").startswith("Smith, 35–69;"), notes)
t("note line joined with evidence: pro-|duction -> production (word found in the text)",
  "the production of the text was slow" in notes.get("1", "") and "(prefix, but found in the text)" in rep, D)
t("note number on the line's own baseline, smaller -> note 2",
  notes.get("2") == "Whole first line on one baseline, number only smaller, and a second line of the same note.", notes)
t("superscript inside a note line kept in place: 'XVIIe siècle' (listed)",
  notes.get("3") == "Asséo, 1974: “Le XVIIe siècle”." and "['e']" in rep, notes)
t("front matter out of the text into _front.md (title, author, abstract)",
  "A Test Title" not in md and "abstract is set" not in md and "A Test Title for Stage One" in front
  and "*This abstract is set in italics at the note size and it runs on to a second line of its own.*" in front, D + front)
t("caps heading smaller than the body -> # heading, kept though it sits just above the text",
  re.search(r"^# INTRODUCTION$", md, re.M) is not None, D)
t("two-line caps heading -> one heading", re.search(r"^# SECOND PART: A LONG HEADING IN CAPITALS$", md, re.M) is not None, D)
t("small-caps opening words retyped and listed", re.search(r"^This essay begins the old road", md, re.M) is not None
  and "opening words in small capitals retyped" in rep, D)
t("unnumbered note at the foot of page 1 -> ::: przypis-tytulowy at the top",
  md.startswith("::: przypis-tytulowy\nI owe many thanks to my colleagues for their help, and to the reviewers for their generous reading.\n:::"), D)
t("paragraph running over the page (running head between) stays one paragraph",
  re.search(r"so it all\[\^1\] " + re.escape(cont[0].split()[0]) + " ", md) is not None, D)
t("closed em dash at a line end joined without a space: intrigue—and", "intrigue—and more" in md, D)
t("verse -> one quotation, forced line breaks, marker on the last line",
  "> Dark goddess whose splendor\\\n> Burns with the force of suns:\\\n> Snow cannot rival her\\\n> And ebony triumphs over ivory.[^2]" in md, D)
t("caption -> ::: podpis, placed after the paragraph it interrupted; paragraph rejoined",
  re.search(r"\[\^3\] after the figure the same sentence goes on and ends here\.\n\n\[\^3\]: .*\n\n::: podpis\nFigure 1\. A drawing", md) is not None, D)
t("reference list at note size -> _bib.txt, one entry per item; out of the text with its heading",
  bib[:1] == ["Acton, Thomas. Gypsy Politics and Social Change. London: Routledge and Kegan Paul, 1974."] and len(bib) == 3 and "BIBLIOGRAPHY" not in md and "Acton" not in md, (bib, D))
t("URL hyphen at a line break decided by the link target: typesetter's removed, the address's own kept",
  bib[1:2] == ["Fraser, Angus. The Gypsies. Oxford: Blackwell, 1992. https://www.gypsylore.org/fraser.html."]
  and "hyphen removed (link target)" in rep and "hyphen kept (link target)" in rep, (bib, D))
t("URL text with a wrong glyph (id¼12) replaced by its link target, listed",
  bib[2:] == ["Galland, Nora. Name-Calling. Shakespeare en devenir 12 (2017): https://www.ex.org/i.php?id=12."]
  and "differs from its link target" in rep, (bib, D))
t("running head dropped", "TEST JOURNAL" not in md, D)

n, ok = len(res), sum(res)
print(f"PDF-LAYOUT ALL PASS {n}/{n}" if ok == n else f"PDF-LAYOUT FAILED {n - ok}/{n}")
