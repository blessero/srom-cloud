#!/usr/bin/env python3
"""extract_mb.py — saves MB's published Polish for the four leaf-1.2 passages as <art>_mb.md.

Usage: python3 extract_mb.py <extract_dir>   (extract_dir holds takacs.md, ostendorf.md, fotta.md, dom.md made by
srom-typeset docx_in.py from vol18-PL-HOLD/*.docx). Only Word right-to-left artefacts ([x]{dir="rtl"}) and
soft line breaks are cleaned; wording is untouched. Passage = from the section heading to the last note of the passage.
"""
import os, re, sys
X = sys.argv[1]; OUT = os.path.dirname(os.path.abspath(__file__))
SPANS = {"takacs": ("Romowie u wrót Ameryki", "[^12]:"),
         "ostendorf": ("Rola historii", "[^23]:"),
         "fotta": ("Badanie urasowienia Romów w ujęciu relacyjnym", "[^24]:"),
         "dom": ("Rozmieszczenie terytorialne i tożsamości", "[^30]:")}
for a, (start, end) in SPANS.items():
    L = open(os.path.join(X, a + ".md"), encoding="utf-8").read().split("\n")
    i = L.index(start); j = next(k for k in range(i, len(L)) if L[k].startswith(end))
    t = "\n".join(L[i:j + 1])
    t = re.sub(r'\[([^\]]*)\]\{dir="rtl"\}', r"\1", t)
    t = t.replace("\\\n", "")
    open(os.path.join(OUT, a + "_mb.md"), "w", encoding="utf-8").write(t.strip() + "\n")
    print(f"{a}: lines {i + 1}–{j + 1}, {len(t.split())} words")
