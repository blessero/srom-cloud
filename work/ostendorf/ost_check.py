#!/usr/bin/env python3
"""Checks for the Ostendorf translation (gates 1.5.3a G3, 1.5.3b G4, G5).
default  : English function words left in body paragraphs of ostendorf_pl.md (notes excluded; italics, comments and
           citation tokens removed first). Last line: "leftover English: n".
--quotes : note labels of source quotations in src/ostendorf_src.md (a “…” span of 4+ words, or a block quotation,
           assigned to the next note marker; quotations inside a note belong to that note) vs the `location` column of
           ostendorf_quotes.tsv; classes checked against PLAN OUT-QUOTES.
           Last line: "quotes: a in text, b in sheet, c bad class" (b = detected labels that have a row; rows for
           shorter quotations are allowed and listed).
--marks  : "DO SPRAWDZENIA: S<n>" in ostendorf_pl.md vs "- S<n>" lines in ostendorf_uwagi.md.
"""
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(H, p), encoding="utf-8").read()
if "--quotes" in sys.argv:
    src = rd("src/ostendorf_src.md")
    labels, pending_block = set(), False
    for para in [p for p in src.split("\n\n") if p.strip()]:
        m = re.match(r"\[\^(\w+)\]:", para)
        if m:
            if re.search(r"“[^”]*?(\S+\s+){3,}\S[^”]*”", para): labels.add(m.group(1))
            continue
        if para.startswith(">"): pending_block = True; continue
        if pending_block:
            nm = re.search(r"\[\^(\w+)\]", para)
            if nm: labels.add(nm.group(1))
            pending_block = False
        for q in re.finditer(r"“([^”]*)”", para):
            if len(q.group(1).split()) >= 4:
                nm = re.search(r"\[\^(\w+)\]", para[q.end():])
                if nm: labels.add(nm.group(1))
    rows = [l.split("\t") for l in rd("ostendorf_quotes.tsv").splitlines()[1:] if l.strip()]
    sheet = {r[1].replace("n. ", "") for r in rows}
    bad = [r[0] for r in rows if r[3] not in ("PL-EDITION", "PL-ORIGINAL", "THIRD-LANG", "EN-NO-PL", "VERSE")]
    if labels - sheet: print("MISSING from sheet:", sorted(labels - sheet, key=int))
    if sheet - labels: print("in sheet only (short quotations under 4 words, not detected):", sorted(sheet - labels, key=int))
    print(f"quotes: {len(labels)} in text, {len(labels & sheet)} in sheet, {len(bad)} bad class")
    sys.exit(0)
pl = rd("ostendorf_pl.md")
if "--marks" in sys.argv:
    a = set(re.findall(r"DO SPRAWDZENIA: (S\d+)", pl))
    b = set(re.findall(r"^- (S\d+)\b", rd("ostendorf_uwagi.md"), re.M))
    if a != b: print("only in text:", sorted(a - b), "only in review sheet:", sorted(b - a))
    print(f"marks: {len(a)} in text, {len(b) if a == b else -1} in review sheet")
    sys.exit(0)
body = pl.split("\n---\n", 1)[1] if pl.startswith("---") else pl
paras = [p for p in body.split("\n\n") if p.strip() and not p.lstrip().startswith(("[^", ":::"))]
hits = []
for p in paras:
    t = re.sub(r"<!--.*?-->", " ", p, flags=re.S)
    t = re.sub(r"\[@[^\]]*\]", " ", t)
    t = re.sub(r"\*[^*]+\*", " ", t)
    for m in re.finditer(r"(?i)\b(the|and|of|with|which|that|this|from|were|was|is|for|not|but|have|had)\b", t):
        hits.append(t[max(0, m.start() - 40):m.end() + 40].replace("\n", " "))
for h in hits: print("  …" + h + "…")
print(f"leftover English: {len(hits)}")
