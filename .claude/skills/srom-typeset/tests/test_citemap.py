"""G8: cite_map resolves unique author-date references (parenthetical, narrative, in-note, inflected,
multi, et al., editor, letter suffix, page-only), refuses ambiguous/unknown, and the converted article
builds cleanly. audit catches transcription errors in refs.json against the original bibliography."""
import os, sys, subprocess, tempfile, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FX = os.path.join(ROOT, "tests", "fixtures")
CM = os.path.join(ROOT, "scripts", "cite_map.py")
REFS = os.path.join(FX, "citemap_refs.json")
d = tempfile.mkdtemp()
res = []

def t(name, ok, out=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n" + str(out)[:3000]))

def cm(*args):
    r = subprocess.run([sys.executable, CM, *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

src = os.path.join(FX, "authordate_article.md")
out_md = os.path.join(d, "conv.md")
c, o = cm("scan", src, "--refs", REFS, "--apply", out_md, "--report", os.path.join(d, "r.md"))
t("scan + apply succeeds; page-only '(s. 21)' converted and listed, not blocking", c == 0 and os.path.exists(out_md) and "PAGE-ONLY" in o, o)
conv = open(out_md, encoding="utf-8").read() if os.path.exists(out_md) else ""
print(conv)
t("parenthetical after abbreviation: 'XV w.[^c1] ' (abbrev. period ends sentence)", "z XV w.[^c1] Ficowski" in conv, conv)
t("…note c1 = ficowski s. 15", "[^c1]: [@ficowski1985, s. 15]." in conv, conv)
t("narrative keeps name, marker after it", "Ficowski[^c2] twierdzi" in conv and "[^c2]: [@ficowski1985, s. 17–19]." in conv, conv)
t("page-only after quote inherits the work cited before it: marker after closing quote", "podwójna”[^c3]." in conv and "[^c3]: [@ficowski1985, s. 21]." in conv, conv)
t("inflected narrative 'Mroza' -> mroz2011", "Mroza[^c4]" in conv and "[@mroz2011, s. 90]" in conv, conv)
t("multi-item with prefix, ff. -> i n., capitalised Zob.", "[Zob. @kolaczek2012, s. 215 i n.; @hancock2007]." in conv, conv)
t("editor '(red.)' form -> kowalski2011", "[@kowalski2011]" in conv, conv)
t("et al. + table locator in braces", "[@fialkowska2020, {tabl. 3}]" in conv, conv)
t("letter suffix a/b via citation-label", "[@nowak2010]" in conv and "[@nowak2010b, s. 7]" in conv, conv)
t("in-note narrative + bare two-author cite converted", "[^1]: Szerzej o tym [@mroz2011, s. 92]; [zob. też @mroz1998, s. 40]." in conv, conv)
t("'Kraków 1985' in a note and '1939–1945 (okupacja)' untouched", "Wydanie: Kraków 1985." in conv and "Okres 1939–1945 (okupacja) nie jest cytatem." in conv, conv)
c2, o2 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "check.py"), out_md, "--refs", REFS], capture_output=True, text=True).returncode, ""
t("converted file passes check.py", c2 == 0)
b = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), out_md, "--refs", REFS, "--out", os.path.join(d, "b")], capture_output=True, text=True)
rep = open(os.path.join(d, "b", "conv_report.md"), encoding="utf-8").read()
t("converted file builds (PASS)", b.returncode == 0, rep[:2500])

amb2 = os.path.join(d, "red.md"); open(amb2, "w", encoding="utf-8").write("Tekst (Kowalski (red.) 2011: 5) i (Zob. Nowak, Kowalski i Mróz (red.) 1999).\n")
c, o = cm("scan", amb2, "--refs", REFS, "--report", os.path.join(d, "red_r.md"))
rr = open(os.path.join(d, "red_r.md"), encoding="utf-8").read()
t("nested '(red.)' parenthetical resolved to kowalski2011", "`(Kowalski (red.) 2011: 5)` | **OK** | kowalski2011" in rr, rr)
t("unresolvable nested one reported once, blocks", c == 1 and o.count("Nowak, Kowalski i Mróz") == 1, o)
amb = os.path.join(d, "amb.md"); open(amb, "w", encoding="utf-8").write("Tekst (Lee 2005: 3) i (Zieliński 1999).\n")
c, o = cm("scan", amb, "--refs", REFS, "--apply", os.path.join(d, "amb_out.md"))
t("ambiguous (two Lee 2005) and unknown author refuse to apply", c == 1 and "AMBIGUOUS" in o and "UNKNOWN" in o and not os.path.exists(os.path.join(d, "amb_out.md")), o)

hist = os.path.join(d, "hist.md"); open(hist, "w", encoding="utf-8").write("Urodził się w Tarnowie (1951), a pokój podpisano (Ryga 1921). Ficowski (1985: 5) pisał.\n")
c, o = cm("scan", hist, "--refs", REFS, "--apply", os.path.join(d, "hist_out.md"))
t("'Tarnowie (1951)' NOT-CITED? (non-blocking); '(Ryga 1921)' UNKNOWN blocks", c == 1 and "NOT-CITED?" in o and "UNKNOWN" in o, o)
c, o = cm("scan", hist, "--refs", REFS, "--apply", os.path.join(d, "hist_out.md"), "--allow-unknown")
ho = open(os.path.join(d, "hist_out.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "hist_out.md")) else ""
t("--allow-unknown: non-citations left verbatim, the real citation converted", c == 0 and "w Tarnowie (1951)" in ho and "(Ryga 1921)" in ho and "Ficowski[^c1] pisał" in ho, o + ho)

# ---- audit: original bibliography vs refs.json
bib = os.path.join(d, "bib.txt")
open(bib, "w", encoding="utf-8").write(
    "Ficowski, Jerzy (1985). Cyganie na polskich drogach. Kraków: Wydawnictwo Literackie.\n"
    "Kołaczek, Małgorzata (2012). Tytuł artykułu. Studia Romologica 5: 211–228. https://doi.org/10.1234/srom.2012.5.11\n")
sub = os.path.join(d, "sub.json")
refs = json.load(open(REFS, encoding="utf-8"))
json.dump([r for r in refs if r["id"] in ("ficowski1985", "kolaczek2012")], open(sub, "w"), ensure_ascii=False)
c, o = cm("audit", "--refs", sub, "--bib", bib)
t("audit: faithful refs pass", c == 0 and "CITEMAP OK" in o, o)
bad = [dict(r) for r in json.load(open(sub))]
for r in bad:
    if r["id"] == "kolaczek2012": r["page"] = "211-218"
    if r["id"] == "ficowski1985": r["publisher"] = "Czytelnik"
json.dump(bad, open(sub, "w"), ensure_ascii=False)
c, o = cm("audit", "--refs", sub, "--bib", bib)
t("audit: wrong page range and wrong publisher caught", c == 1 and "kolaczek2012" in o and "228" in o and "ficowski1985" in o and "literackie" in o, o)
json.dump([r for r in refs if r["id"] == "ficowski1985"], open(sub, "w"), ensure_ascii=False)
c, o = cm("audit", "--refs", sub, "--bib", bib)
t("audit: original entry with no ref caught", c == 1 and "not mapped to exactly one ref" in o, o)

po = os.path.join(d, "po.md"); open(po, "w", encoding="utf-8").write("Pierwszy akapit (s. 4).\n\nDrugi (Ficowski 1985: 3).\n\nTrzeci akapit (s. 9).\n")
c, o = cm("scan", po, "--refs", REFS, "--apply", os.path.join(d, "po_out.md"))
t("page-only with no earlier citation blocks; later one follows the previous paragraph's work", c == 1 and "PAGE-ONLY?" in o and "['ficowski1985']" in o, o)

# E2: the translator's added refs are not matched against the author's list, but need a source
json.dump([r for r in refs if r["id"] == "ficowski1985"], open(sub, "w"), ensure_ascii=False)
tlr = os.path.join(d, "tl.json")
json.dump([{"id": "ficowski1985pl", "type": "book", "author": [{"family": "Ficowski"}], "title": "X", "srom-added": "tlum"}], open(tlr, "w"))
bib1 = os.path.join(d, "bib1.txt"); open(bib1, "w", encoding="utf-8").write(open(bib, encoding="utf-8").read().splitlines()[0] + "\n")
c, o = cm("audit", "--refs", sub, "--refs", tlr, "--bib", bib1)
t("E2: srom-added entry without srom-source -> PROBLEM; not treated as a missing original", c == 1 and "no srom-source" in o and "no matching original entry" not in o, o)
json.dump([{"id": "ficowski1985pl", "type": "book", "author": [{"family": "Ficowski"}], "title": "X", "srom-added": "tlum", "srom-source": "ISBN 978-83-0"}], open(tlr, "w"))
c, o = cm("audit", "--refs", sub, "--refs", tlr, "--bib", bib1)
t("E2: srom-added entry with a source passes the audit", c == 0, o)

n, ok = len(res), sum(res)
print(f"CITEMAP ALL PASS {n}/{n}" if ok == n else f"CITEMAP FAILED {n - ok}/{n}")
