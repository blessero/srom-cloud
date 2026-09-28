#!/usr/bin/env python3
"""build_src.py — makes the four leaf-1.2 source passages from srom-typeset's docx_in.py extraction.

Usage: python3 build_src.py <extract_dir>   (extract_dir holds takacs.md, ostendorf.md, fotta.md, dom.md
made by docx_in.py; Fotta via `textutil -convert docx` from the RTF first).
Only extraction repairs are made (page-break joins, PDF hyphenation, typed note markers → [^n], notes moved
to the end, italic fragments merged, layout '>' removed). Wording and the authors' own errors are untouched.
"""
import os, re, sys
X = sys.argv[1]; OUT = os.path.dirname(os.path.abspath(__file__))
def lines(name): return open(os.path.join(X, name + ".md"), encoding="utf-8").read().split("\n")
def must(s, a, b):
    assert a in s, a[:60]; return s.replace(a, b, 1)
def save(name, text):
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    open(os.path.join(OUT, name + "_src.md"), "w", encoding="utf-8").write(text)

# Takács: lines 30–81 (1-based) — two whole sections, real Word notes 6–12
L = lines("takacs"); t = "\n".join(L[29:81])
t = t.replace("[HathiTrust]{.underline}", "HathiTrust")
save("takacs", t)

# Ostendorf: lines 19–44 — two whole sections; author-date citations kept; typed markers 3, 4 (note texts absent from the file)
L = lines("ostendorf"); t = "\n".join(L[18:44])
t = re.sub(r"^# \*\*(.+?)\*\*$", r"# \1", t, flags=re.M)
t = must(t, "amateurs alike.3", "amateurs alike.[^3]")
t = must(t, "professional historians.4", "professional historians.[^4]")
t += "\n\n[^3]: [note text missing from the source file]\n\n[^4]: [note text missing from the source file]\n"
save("ostendorf", t)

# Fotta: lines 51–101 — one whole section; PDF rip: notes 4–6 interleaved, figure caption, hyphenation
L = [re.sub(r"^> ?", "", l) for l in lines("fotta")[50:101]]
t = "\n".join(L)
t = re.sub(r"^\*\*(.+?)\*\*$", r"# \1", t, count=1, flags=re.M)
n4 = re.search(r"\nEven when an analyst argues.*?Shih 2008\)\.\n", t, re.S).group(0)
n5 = re.search(r"\nAnn Ostendorf \(e\.g\. 2020.*?Wakeley-Smith 2022a: 174\)\.\n", t, re.S).group(0)
n6 = re.search(r"\nRomanies’ tangential place.*?horse dealers and\n", t, re.S).group(0)
for n in (n4, n5, n6): t = t.replace(n, "\n")
t = must(t, "\nFigure 2. Cover of the first edition of *Os Ciganos no Brasil* (1886)\n", "\n")
t = re.sub(r"\(Moraes Filho 1885:\s*\n+\s*xxiii;", "(Moraes Filho 1885: xxiii;", t)
t = re.sub(r"was not unique to\s*\n+\s*Brazil\.", "was not unique to Brazil.", t)
t = re.sub(r"examining the impact of\s*\n+\s*this process", "examining the impact of this process", t)
t = re.sub(r"or “adapted,”6 to this\s*\n+\s*system;", "or “adapted,”[^6] to this system;", t)
for a, b in (("Paradox- ically", "Paradoxically"), ("raciali- zation", "racialization"), ("Czecho- slovakia", "Czechoslovakia"),
             ("charac- teristics", "characteristics"), ("area’s impact.4", "area’s impact.[^4]"),
             ("isolated manner.5", "isolated manner.[^5]")):
    t = must(t, a, b)
for q in ("On July 6 of that turbulent year", "It is possible, still, that,", "Investigating who would have carried"):
    t = must(t, "\n" + q, "\n> " + q)
n6 = n6.strip() + " traders, and repairers of pans, cauldrons, and machines for sugar refinement.” Consequently, “many Ciganos, following the initial phase of the socially pathological marginality, dissolved within the Brazilian whole” (Freyre 1951: 790–1)."
t = re.sub(r"\n(?!#|>|\[\^)", "\n\n", t)
t += "\n\n[^4]: " + n4.strip() + "\n\n[^5]: " + n5.strip() + "\n\n[^6]: " + n6 + "\n"
save("fotta", t)

# Marushiakova/Popov: section "Territorial Distributions and Identities", to the end of the paragraph on Belorechensk;
# notes 27–28 on that page belong to the previous section and are dropped; notes 29–30 moved to the end
L = [re.sub(r"^> ?", "", l) for l in lines("dom")]
a = L.index("## Territorial Distributions and Identities")
b = next(i for i in range(a, len(L)) if L[i].endswith("Krasnodar Krai of the Russian Federation."))
t = "\n".join(L[a:b + 1])
t = re.sub(r"\n27 MARUSHIAKOVA.*?\n\n28 Ibid, p\. 122\.\n", "\n", t, flags=re.S)
n29 = re.search(r"\n29 BUDAGOV.*?p\. 326\.\n", t, re.S).group(0)
n30 = re.search(r"\n30 MARUSHIAKOVA, Elena – POPOV, Vesselin: \*Gypsies\*.*?p\. 68\.\n", t, re.S).group(0)
for n in (n29, n30): t = t.replace(n, "\n")
t = re.sub(r"we have not\s*\n+\s*visited", "we have not visited", t)
t = re.sub(r"regions of Goychay,\s*\n+\s*Shamakhi", "regions of Goychay, Shamakhi", t)
t = re.sub(r"where a small\s*\n+\s*number of Dom", "where a small number of Dom", t)
t = must(t, "Winter Camp”29.", "Winter Camp”[^29].")
t = must(t, "Kvemo Kartli30.", "Kvemo Kartli[^30].")
t = must(t, "present- day", "present-day")
def merge_it(s): return re.sub(r"\*(\S[^*]*?)\*(\s+)\*(?=\S)", r"*\1\2", s)
for _ in range(12): t = merge_it(t)
n29 = n29.strip()[3:].replace('[’]{dir="rtl"}', "’")
for _ in range(12): n29 = merge_it(n29)
n30 = n30.strip()[3:]
for _ in range(12): n30 = merge_it(n30)
t += "\n\n[^29]: " + n29 + "\n\n[^30]: " + n30 + "\n"
save("dom", t)
print("built 4 sources in", OUT)
