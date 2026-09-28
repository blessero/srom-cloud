#!/usr/bin/env python3
"""Checks for the Ndiaye draft (gates 1.5.2b G4, G5).
default : English function words left in the body text (notes excluded: they keep the author's originals);
          italics, comments and citation tokens are removed first. Last line: "leftover English: n".
--marks : "DO SPRAWDZENIA: S<n>" marks in ndiaye_pl.md vs "- S<n>" lines in ndiaye_uwagi.md (same set expected).
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
pl = open(os.path.join(HERE, "ndiaye_pl.md"), encoding="utf-8").read()
if "--marks" in sys.argv:
    a = set(re.findall(r"DO SPRAWDZENIA: (S\d+)", pl))
    b = set(re.findall(r"^- (S\d+)\b", open(os.path.join(HERE, "ndiaye_uwagi.md"), encoding="utf-8").read(), re.M))
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
    for m in re.finditer(r"\b(the|and|of|with|which|that|this|from|were|was|is)\b", t):
        hits.append(t[max(0, m.start() - 40):m.end() + 40].replace("\n", " "))
for h in hits: print("  …" + h + "…")
print(f"leftover English: {len(hits)}")
