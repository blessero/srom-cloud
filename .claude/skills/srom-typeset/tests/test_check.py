"""G5: check.py catches orphan/undefined/duplicate notes, unresolved keys, broken italics,
author-date leftovers, and marker/citation drift between source and translation."""
import os, sys, json, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(ROOT, "tests", "fixtures", "kanon_refs.json")
CHECK = os.path.join(ROOT, "scripts", "check.py")
d = tempfile.mkdtemp()
results = []

def w(name, text):
    p = os.path.join(d, name); open(p, "w", encoding="utf-8").write(text); return p

def run(*args):
    r = subprocess.run([sys.executable, CHECK, *args, "--refs", REFS], capture_output=True, text=True)
    return r.returncode, r.stdout

def t(name, ok, out=""):
    results.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n" + out))

SRC = """# 1. INTRODUCTION

The first records date from 1501.[^1] Ficowski wrote about it in 1985[^2] and again later.[^3]

[^1]: [@ficowski1985, s. 15].

[^2]: [@ficowski1985, s. 17]; see also [@mroz2011, s. 90].

[^3]: State Archive in Kraków, fond 29/456, file 12, fol. 34v, 4 March 1937.

> A block quotation with a note.[^4]

[^4]: [@hancock2007, s. 3].

Final paragraph.
"""
TGT = """# 1. WSTĘP

Pierwsze wzmianki pochodzą z 1501 r.[^1] Ficowski pisał o tym w 1985 r.[^2] i ponownie później[^3].

[^1]: [@ficowski1985, s. 15].

[^2]: [@ficowski1985, s. 17]; zob. też [@mroz2011, s. 90].

[^3]: Archiwum Narodowe w Krakowie, zespół 29/456, sygn. 12, k. 34v, 04.03.1937.

> Cytat blokowy z przypisem[^4].

[^4]: [@hancock2007, s. 3].

Ostatni akapit.
"""
s, g = w("src.md", SRC), w("tgt.md", TGT)
c, o = run("--pair", s, g)
t("faithful translation passes (dates reformatted = WARN only)", c == 0 and "CHECK OK" in o, o)
t("date reformat 4 March -> 04.03 not an error (numbers equal after int())", "note 3" not in o, o)

c, o = run("--pair", s, w("t1.md", TGT.replace("w 1985 r.[^2] i ponownie później[^3].", "w 1985 r.[^2] i ponownie później.").replace("[^3]: Archiwum", "[^9]: Archiwum")))
t("dropped marker in a paragraph -> ERROR with paragraph located", c == 1 and "note marker(s) in source" in o, o)

c, o = run("--pair", s, w("t2.md", TGT.replace("[@ficowski1985, s. 17]; zob. też [@mroz2011, s. 90]", "[@mroz2011, s. 90]; zob. też [@ficowski1985, s. 17]")))
t("citation keys swapped inside a note -> ERROR", c == 1 and "note 2: citation keys differ" in o, o)

c, o = run("--pair", s, w("t3.md", TGT.replace("[@ficowski1985, s. 15]", "[@ficowski1985, s. 16]")))
t("changed page number -> WARN (reported, not blocking)", c == 0 and "WARN  note 1: numbers differ" in o, o)

c, o = run("--pair", s, w("t4.md", TGT.replace("i ponownie później[^3].\n\n", "i ponownie później[^3]. ").replace("Ostatni akapit.", "")))
t("merged/dropped paragraph -> structure ERROR", c == 1 and ("block structure differs" in o or "leaf block count differs" in o), o)

# ---- IF-TYPESET R1/R2 (srom-tlumacz contract) and the title note
TN = TGT.replace("i ponownie później[^3].", "i ponownie później[^3].[^t1]") + "\n[^t1]: Wyjaśnienie tłumacza – przyp. tłum.\n"
c, o = run("--pair", s, w("r1.md", TN))
t("R1: translator note [^t1] ending '– przyp. tłum.' left out of the comparison", c == 0 and "translator/editorial note" in o, o)
c, o = run("--pair", s, w("r1b.md", TGT.replace("i ponownie później[^3].", "i ponownie później[^3].[^9]") + "\n[^9]: Uwaga – przyp. tłum.\n"))
t("R1: translator note recognised by its formula alone (label lost in Word)", c == 0, o)
c, o = run("--pair", s, w("r1c.md", TN.replace("Wyjaśnienie tłumacza – przyp. tłum.", "Wyjaśnienie tłumacza.")))
t("R1: [^t1] without the formula -> ERROR", c == 1 and "must end with the formula" in o, o)
# E8 (kanon § 7.1): editorial notes [^r<n>] "– przyp. red." join the non-author series; the formula must END the note
RN = TGT.replace("i ponownie później[^3].", "i ponownie później[^3].[^r1]") + "\n[^r1]: Uwaga redakcji – przyp. red.\n"
c, o = run("--pair", s, w("e8a.md", RN))
t("E8: editorial note [^r1] '– przyp. red.' left out of the comparison", c == 0 and "translator/editorial note" in o, o)
c, o = run("--pair", s, w("e8b.md", RN.replace("Uwaga redakcji – przyp. red.", "Uwaga redakcji.")))
t("E8: [^r1] without its formula -> ERROR", c == 1 and "[^r1] must end with the formula \"– przyp. red.\"" in o, o)
c, o = run("--pair", s, w("e8c.md", TN.replace("– przyp. tłum.", "– przyp. red.")))
t("E8: [^t1] closed by the editorial formula -> ERROR (label and formula must agree)", c == 1 and "[^t1] must end" in o, o)
c, o = run(w("e8d.md", RN.replace("Uwaga redakcji – przyp. red.", "Uwaga redakcji.")))
t("E8: single-file check catches [^r1] without formula too", c == 1 and "[^r1] must end" in o, o)
BR = TGT.replace("zob. też [@mroz2011, s. 90].", "zob. też [@mroz2011, s. 90] [zob. też wydanie polskie, s. 45 – przyp. tłum.]")
c, o = run("--pair", s, w("e8e.md", BR))
t("E8: '[… – przyp. tłum.]' closing an AUTHOR's note keeps it an author's note (compared, not left out)",
  BR != TGT and c == 0 and "left out of the comparison" not in o, o)
ADD = TGT.replace("[^1]: [@ficowski1985, s. 15].", "[^1]: [@ficowski1985, s. 15]; wyd. pol. [@mroz2011, s. 3]. <!-- DODANO: @mroz2011 -->")
c, o = run("--pair", s, w("r2.md", ADD))
t("R2: added citation declared with <!-- DODANO: @key --> passes", c == 0, o)
c, o = run("--pair", s, w("r2b.md", ADD.replace(" <!-- DODANO: @mroz2011 -->", "")))
t("R2: undeclared added citation -> ERROR with the fix", c == 1 and "undeclared addition ['mroz2011']" in o, o)
c, o = run("--pair", s, w("r4.md", "::: przypis-tytulowy\nPrzekład z języka angielskiego: Jan Nowak.\n:::\n\n" + TGT))
t("title note div (translation note) has no source counterpart — not a structure error", c == 0, o)
TN = "::: przypis-tytulowy\nPierwodruk: nota o przekładzie.\n\nPodziękowania autorki.\n:::\n\n"
c, o = run("--pair", s, w("r5.md", TN + TGT))
t("E15: translation note + author's note on the title as two paragraphs of one block -> OK", c == 0, o)
c, o = run("--pair", s, w("r6.md", TN.replace("\n\nPodziękowania", "\n:::\n\n::: przypis-tytulowy\nPodziękowania") + TGT))
t("E15: two title-note blocks -> ERROR naming the one-block form", c == 1 and "2 title-note blocks" in o and "further paragraph" in o, o)

# ---- srom-tlumacz requests E1, E2, E4
EX_S = "Tekst.\n\n::: przyklad\n```\n(1)  Me   dikhav\n     1SG  see.1SG\n     ‘I see.’\n```\n:::\n"
EX_T = "Tekst.\n\n::: przyklad\n```\n(1)  Me   dikhav\n     1SG  widzieć.1SG\n     ‘Widzę.’\n```\n:::\n"
xs = w("ex_s.md", EX_S)
c, o = run("--pair", xs, w("ex_t.md", EX_T))
t("E1: example with Polish glosses and translation passes", c == 0, o)
c, o = run("--pair", xs, w("ex_t2.md", EX_T.replace("dikhav", "dikhaw")))
t("E1: changed Romani form line -> ERROR", c == 1 and "form line changed" in o, o)
c, o = run("--pair", xs, w("ex_t3.md", EX_T.replace("     ‘Widzę.’\n", "")))
t("E1: dropped example line -> ERROR", c == 1 and "line(s) in source" in o, o)
tl = os.path.join(d, "refs_tlum.json")
json.dump([{"id": "ficowski1985pl", "type": "book", "author": [{"family": "Ficowski", "given": "Jerzy"}], "title": "Cyganie", "srom-added": "tlum", "srom-source": "https://example.org/rec"}], open(tl, "w"), ensure_ascii=False)
ADD2 = TGT.replace("[^1]: [@ficowski1985, s. 15].", "[^1]: [@ficowski1985, s. 15]; wyd. pol. [@ficowski1985pl, s. 1985].")
r = subprocess.run([sys.executable, CHECK, "--pair", s, w("e2.md", ADD2), "--refs", REFS, "--refs", tl], capture_output=True, text=True)
t("E2: addition marked srom-added in the translator's refs passes (warned where), no DODANO needed", r.returncode == 0 and "added citation @ficowski1985pl" in r.stdout, r.stdout)
t("E4: locator of the added citation and digits of keys not counted as number differences", "note 1: numbers differ" not in r.stdout, r.stdout)
c, o = run("--pair", s, w("r2c.md", ADD))
t("E4: DODANO addition produces no numbers noise", c == 0 and "note 1: numbers differ" not in o, o)

c, o = run(w("u1.md", "Tekst[^1] i dalej[^2].\n\n[^1]: Nota.\n"))
t("marker without definition -> ERROR", c == 1 and "[^2] has no definition" in o, o)
c, o = run(w("u2.md", "Tekst[^1].\n\n[^1]: Nota.\n\n[^2]: Sierota.\n"))
t("orphan definition -> ERROR", c == 1 and "[^2] is never referenced" in o, o)
c, o = run(w("u3.md", "Tekst[^1] i[^1].\n\n[^1]: Nota.\n"))
t("label used twice -> ERROR", c == 1 and "used 2×" in o, o)
c, o = run(w("u4.md", "Tekst[^1].\n\n[^1]: [@brak2020, s. 4].\n"))
t("unknown citation key -> ERROR", c == 1 and "@brak2020 not in refs" in o, o)
c, o = run(w("u5.md", "Tekst o *tytule bez domknięcia.\n"))
t("broken italics (literal *) -> ERROR", c == 1 and "broken italics" in o, o)
c, o = run(w("u6.md", "Jak pisze Ficowski (Ficowski 1985: 15), to prawda.\n"))
t("author-date leftover -> ERROR", c == 1 and "author-date reference not converted" in o, o)
c, o = run(w("u7.md", "Tekst (Nowak i Kowalski, 2010, s. 5) oraz (zob. Mróz 1998).\n"))
t("author-date variants (two authors, 'zob.') -> ERROR ×2", c == 1 and o.count("author-date") == 2, o)
c, o = run(w("u8.md", "Tekst o latach 1939–1945 (okres okupacji) i (XX w.).\n"))
t("ordinary parentheses with years are not flagged", c == 0, o)

c, o = run(w("u9.md", "Bitwa (Warszawa 1920) i pokój (Ryga 1921) nie są cytatami.\n"))
t("place + year in parentheses (not a ref author) -> WARN only, build not blocked", c == 0 and o.count("WARN  parenthesis with a name and a year") == 2, o)
c, o = run(w("u10.md", "Jak twierdzi Ficowski (1985: 15), było inaczej.\n"))
t("narrative author-date leftover with a ref author -> ERROR", c == 1 and "narrative author-date reference not converted" in o, o)
c, o = run(w("u11.md", "Urodził się w Tarnowie (1951).\n"))
t("'Tarnowie (1951)' is not taken for a narrative citation", c == 0 and "narrative" not in o, o)
c, o = run(w("u12.md", "Pisze @ficowski1985 [s. 5].\n"))
t("@key without brackets -> ERROR", c == 1 and "author-in-text" in o, o)

# ---- keyed: author's literal notes vs the same notes turned into [@key] citations
KO, KK = os.path.join(ROOT, "tests", "fixtures", "keyed", "orig.md"), os.path.join(ROOT, "tests", "fixtures", "keyed", "keyed.md")
c, o = run("--keyed", KO, KK)
t("keyed: faithful keying (Tamże->Ibidem, op. cit.->short form, literal archival note) passes", c == 0 and "CHECK OK" in o, o)
kk = open(KK, encoding="utf-8").read()
c, o = run("--keyed", KO, w("k1.md", kk.replace("s. 17–19]", "s. 17–18]")))
t("keyed: page number changed while keying -> ERROR", c == 1 and "page/folio numbers lost" in o, o)
c, o = run("--keyed", KO, w("k2.md", kk.replace("@kolaczek2012", "@hancock2007")))
t("keyed: wrong work keyed (author not in original note) -> ERROR", c == 1 and "@hancock2007" in o, o)
c, o = run("--keyed", KO, w("k3.md", kk.replace("[^2]: [@ficowski1985, s. 17–19].", "[^2]: [@mroz2011, s. 17–19].")))
t("keyed: tamże keyed to a different work than the previous note -> ERROR", c == 1 and "original is ibid./tamże" in o, o)
c, o = run("--keyed", KO, w("k4.md", kk.replace(" oraz[^4]", " oraz").replace("[^4]: ANK, 29/456, sygn. 12, k. 41.\n", "")))
t("keyed: dropped note -> ERROR", c == 1 and "note count differs" in o, o)

# ---- keyed, short-form notes with unlabelled pages (English/French journals: "Hornback, 35–69")
SREFS = w("short_refs.json", json.dumps([
    {"id": "hornback2018", "type": "book", "author": [{"family": "Hornback", "given": "Robert"}], "title": "Racism and Early Blackface",
     "publisher": "Palgrave", "publisher-place": "Cham", "issued": {"date-parts": [[2018]]}},
    {"id": "ndiaye2021", "type": "article-journal", "author": [{"family": "Ndiaye", "given": "Noémie"}], "title": "Come Aloft",
     "container-title": "ELR", "volume": "51", "page": "121–151", "issued": {"date-parts": [[2021]]}},
    {"id": "ndiaye2022", "type": "book", "author": [{"family": "Ndiaye", "given": "Noémie"}], "title": "Scripts of Blackness",
     "publisher": "UPenn Press", "publisher-place": "Philadelphia", "issued": {"date-parts": [[2022]]}},
    {"id": "mw1662", "type": "book", "author": [{"literal": "M. W., M. A."}], "title": "The marriage broaker",
     "publisher": "X", "publisher-place": "London", "issued": {"date-parts": [[1662]]}},
    {"id": "chang2020", "type": "book", "author": [{"family": "Chang", "given": "Felix"}, {"family": "Rucker-Chang", "given": "Sunnie"}],
     "title": "Roma Rights", "publisher": "CUP", "publisher-place": "Cambridge", "issued": {"date-parts": [[2020]]}}], ensure_ascii=False))
SO = w("short_o.md", "A[^1] b[^2] c[^3] d[^4] e[^5] f[^6] g[^7] h[^8].\n\n[^1]: Hornback, 35–69.\n\n[^2]: See Ndiaye, 2021, 145–51; Ndiaye, 2022, 214–31.\n\n"
       "[^3]: “Peace”: M.W., 60.\n\n[^4]: M. W., M. A., 34–36.\n\n[^5]: Ndiaye, 2021.\n\n[^6]: M. W., M. A., 20.\n\n"
       "[^7]: M. W., M. A., 20.\n\n[^8]: Chang and Rucker-Chang, 24.\n")
SK = ("A[^1] b[^2] c[^3] d[^4] e[^5] f[^6] g[^7] h[^8].\n\n[^1]: [@hornback2018, s. 35–69].\n\n[^2]: Zob. [@ndiaye2021, s. 145–151; @ndiaye2022, s. 214–231].\n\n"
      "[^3]: „Peace”: [@mw1662, s. 60].\n\n[^4]: [@mw1662, s. 34–36].\n\n[^5]: [@ndiaye2021].\n\n[^6]: [@mw1662, s. 20].\n\n"
      "[^7]: [@mw1662, s. 20].\n\n[^8]: [@chang2020, s. 24].\n")
def runk(o, k):
    r = subprocess.run([sys.executable, CHECK, "--keyed", o, k, "--refs", SREFS], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
c, o = runk(SO, w("short_k.md", SK))
t("keyed short form: unlabelled pages, abbreviated ranges expanded, 'M.W.' for 'M. W., M. A.', year of a work cited "
  "whole, same page again as bare Ibidem, 'Chang' inside 'Rucker-Chang' -> CHECK OK, no year warnings",
  c == 0 and "CHECK OK" in o and "WARN" not in o, o)
c, o = runk(SO, w("short_k4.md", SK.replace("[^8]: [@chang2020, s. 24]", "[^8]: [@chang2020, s. 42]")))
t("keyed short form: page of a two-author work changed -> ERROR", c == 1 and "note 8" in o and "24" in o, o)
VL = w("vl_refs.json", json.dumps([{"id": "vanlennep1965", "type": "book", "editor": [{"family": "Van Lennep", "given": "William"}],
    "srom-as-written": {"editor": "Van Lannep"}, "title": "The London Stage", "publisher": "SIUP", "publisher-place": "Carbondale",
    "issued": {"date-parts": [[1965]]}}], ensure_ascii=False))
r = subprocess.run([sys.executable, CHECK, "--keyed", w("vl_o.md", "A[^1].\n\n[^1]: See Van Lannep, 256.\n"),
                    w("vl_k.md", "A[^1].\n\n[^1]: Zob. [@vanlennep1965, s. 256].\n"), "--refs", VL], capture_output=True, text=True)
t("keyed: corrected name (Van Lennep) keyed where the author wrote Van Lannep (srom-as-written) -> CHECK OK", r.returncode == 0, r.stdout)
c, o = runk(SO, w("short_k1.md", SK.replace("s. 214–231", "s. 214–230")))
t("keyed short form: unlabelled page changed (214–31 keyed as 214–230) -> ERROR", c == 1 and "page/folio numbers lost" in o and "231" in o, o)
c, o = runk(SO, w("short_k2.md", SK.replace("[@hornback2018, s. 35–69]", "[@hornback2018, s. 35]")))
t("keyed short form: page dropped from a range (Hornback, 35–69 -> s. 35) -> ERROR", c == 1 and "69" in o, o)
# German full citations (stage-1 test 3): the chapter's own range before "hier S." is the work's page field (printed in the
# bibliography, not in the note); a title opening with a number is not a page; a column (Sp.) and a note (Anm.) are locators
DREFS = w("de_refs.json", json.dumps([
    {"id": "landwehr2001", "type": "chapter", "author": [{"family": "Landwehr", "given": "Achim"}], "title": "Norm, Normalität, Anomale",
     "container-title": "Minderheiten", "page": "41–74", "publisher-place": "St. Katharinen", "issued": {"date-parts": [[2001]]}},
    {"id": "scheffknecht2003", "type": "book", "author": [{"family": "Scheffknecht", "given": "Wolfgang"}],
     "title": "100 Jahre Marktgemeinde Lustenau", "publisher-place": "Lustenau", "issued": {"date-parts": [[2003]]}},
    {"id": "jutz1965", "type": "book", "author": [{"family": "Jutz", "given": "Leo"}], "title": "Vorarlbergisches Wörterbuch",
     "volume": "2", "publisher-place": "Wien", "issued": {"date-parts": [[1965]]}}], ensure_ascii=False))
DO = w("de_o.md", "A[^1] b[^2] c[^3] d[^4].\n\n[^1]: Achim Landwehr, Norm, Normalität, Anomale. In: Minderheiten. St. Katharinen 2001, "
       "S.41-74, hier S.56, Anm. 52.\n\n[^2]: Scheffknecht, 100 Jahre Marktgemeinde Lustenau (wie Anmerkung 9), S.49.\n\n"
       "[^3]: Leo Jutz, Vorarlbergisches Wörterbuch, Bd. 2. Wien 1965, Sp.1717.\n\n[^4]: Landwehr, Norm (wie Anmerkung 1), S.57.\n")
DK = ("A[^1] b[^2] c[^3] d[^4].\n\n[^1]: [@landwehr2001, {s. 56, przyp. 52}].\n\n[^2]: [@scheffknecht2003, s. 49].\n\n"
      "[^3]: [@jutz1965, {szp. 1717}].\n\n[^4]: [@landwehr2001, s. 57].\n")
def rund(o, k):
    r = subprocess.run([sys.executable, CHECK, "--keyed", o, k, "--refs", DREFS], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
c, o = rund(DO, w("de_k.md", DK))
t("keyed German full citations: chapter range before 'hier S.' left to the bibliography, '100 Jahre' not a page, "
  "Sp./Anm. kept as szp./przyp. -> CHECK OK", c == 0 and "CHECK OK" in o, o)
c, o = rund(DO, w("de_k1.md", DK.replace("{s. 56, przyp. 52}", "s. 56")))
t("keyed German: note locator (Anm. 52) dropped -> ERROR", c == 1 and "52" in o, o)
c, o = rund(DO, w("de_k2.md", DK.replace("{szp. 1717}", "{szp. 1771}")))
t("keyed German: column changed (Sp.1717 -> szp. 1771) -> ERROR", c == 1 and "1717" in o, o)
c, o = rund(DO, w("de_k3.md", DK.replace("[@landwehr2001, {s. 56, przyp. 52}]", "[@landwehr2001, {s. 41, przyp. 52}]")))
t("keyed German: the page after 'hier' replaced by the range's start -> ERROR (the range exempts only itself)", c == 1 and "56" in o, o)
TO = w("t_o.md", "::: przypis-tytulowy\nVortrag. Achim Landwehr, Norm. In: Minderheiten. St. Katharinen 2001, S.41-74, hier S.56.\n:::\n\n"
       "A[^1].\n\n[^1]: Landwehr, Norm (wie Anmerkung 1), S.57.\n")
TK = "::: przypis-tytulowy\nVortrag. [@landwehr2001, s. 56].\n:::\n\nA[^1].\n\n[^1]: [@landwehr2001, s. 57].\n"
c, o = rund(TO, w("t_k.md", TK))
t("keyed: a citation in the title note is compared as the title note (first citation there); numbered notes unshifted",
  c == 0 and "CHECK OK" in o, o)
c, o = rund(TO, w("t_k1.md", TK.replace("s. 56", "s. 65")))
t("keyed: page changed in the title note -> ERROR named 'title note'", c == 1 and "title note: page/folio numbers lost" in o, o)
c, o = runk(SO, w("short_k3.md", SK.replace("[@mw1662, s. 60]", "[@hornback2018, s. 60]")))
t("keyed short form: wrong work for 'M.W.' -> ERROR", c == 1 and "@hornback2018" in o, o)

n, ok = len(results), sum(results)
print(f"CHECK ALL PASS {n}/{n}" if ok == n else f"CHECK FAILED {n - ok}/{n}")
