"""G5: check.py catches orphan/undefined/duplicate notes, unresolved keys, broken italics,
author-date leftovers, and marker/citation drift between source and translation."""
import os, re, sys, json, subprocess, tempfile
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

# Chicago full citations (stage-1 test 4, Ostendorf, CUP): the page after the publication parenthesis or a short title
# is a locator; a volume before it ("5:365", "I:183 … and II:452", "1: iv, 358") is not; "103n24" = page + note; an
# Ibidem opening a note that cites more works; DOI, URL, article range belong to the bibliography (no warning)
CREFS = w("chi_refs.json", json.dumps([
    {"id": "weinstein1960", "type": "book", "author": [{"family": "Weinstein", "given": "Donald"}], "title": "Ambassador from Venice",
     "publisher": "UMP", "publisher-place": "Minneapolis", "issued": {"date-parts": [[1960]]}},
    {"id": "actas1915", "type": "book", "title": "Actas da Camara", "volume": "5", "publisher": "AM", "publisher-place": "São Paulo",
     "issued": {"date-parts": [[1915]]}},
    {"id": "paucke1959", "type": "book", "author": [{"family": "Paucke", "given": "Florian"}], "title": "Zwettler Codex 420",
     "publisher": "Braumüller", "publisher-place": "Wien", "issued": {"date-parts": [[1959]]}},
    {"id": "lambert1813", "type": "book", "author": [{"family": "Lambert", "given": "John"}], "title": "Travels", "publisher": "R",
     "publisher-place": "London", "issued": {"date-parts": [[1813]]}},
    {"id": "tabili2003", "type": "article-journal", "author": [{"family": "Tabili", "given": "Laura"}], "title": "Race Is a Relationship",
     "container-title": "JSH", "volume": "37", "issue": "1", "page": "125–130", "DOI": "10.1353/jsh.2003.0162", "issued": {"date-parts": [[2003]]}},
    {"id": "herzog2003", "type": "book", "author": [{"family": "Herzog", "given": "Tamar"}], "title": "Defining Nations",
     "title-short": "Defining Nations…", "publisher": "YUP", "publisher-place": "New Haven", "issued": {"date-parts": [[2003]]}},
    {"id": "galletti2021", "type": "article-journal", "author": [{"family": "Galletti", "given": "Patricia"}], "title": "Los Gitanos como Otro",
     "container-title": "IJRS", "volume": "3", "issue": "2", "DOI": "10.17583/ijrs.8527", "issued": {"date-parts": [[2021]]}}], ensure_ascii=False))
CO = w("chi_o.md", "A[^1] b[^2] c[^3] d[^4] e[^5] f[^6] g[^7] h[^8].\n\n"
       "[^1]: Donald Weinstein, *Ambassador from Venice* (University of Minnesota Press, 1960), 73, 103n24.\n\n"
       "[^2]: *Actas da Camara* (Archivo Municipal, 1915), 5:365.\n\n"
       "[^3]: Florian Paucke, *Zwettler Codex 420* (Braumüller, 1959), I:183, 239 and II:452.\n\n"
       "[^4]: John Lambert, *Travels* (London, 1813), 1: iv, 358.\n\n"
       "[^5]: Laura Tabili, “Race Is a Relationship,” *JSH* 37, no. 1 (2003): 125–130, https://dx.doi.org/10.1353/jsh.2003.0162.\n\n"
       "[^6]: Patricia Galletti, “Los Gitanos como Otro,” *IJRS* 3, no. 2 (2021): 119, https://doi.org/10.17583/ijrs.8527.\n\n"
       "[^7]: Tamar Herzog, *Defining Nations* (Yale University Press, 2003), 133.\n\n"
       "[^8]: Herzog, *Defining Nations*, 133; Galletti, “Los Gitanos como Otro,” 121–22.\n")
CK = ("A[^1] b[^2] c[^3] d[^4] e[^5] f[^6] g[^7] h[^8].\n\n[^1]: [@weinstein1960, {s. 73, 103, przyp. 24}].\n\n"
      "[^2]: [@actas1915, s. 365].\n\n[^3]: [@paucke1959, {t. 1, s. 183, 239 i t. 2, s. 452}].\n\n"
      "[^4]: [@lambert1813, {t. 1, s. iv, 358}].\n\n[^5]: [@tabili2003].\n\n[^6]: [@galletti2021, s. 119].\n\n"
      "[^7]: [@herzog2003, s. 133].\n\n[^8]: [@herzog2003, s. 133; @galletti2021, s. 121–122].\n")
def runc(o, k):
    r = subprocess.run([sys.executable, CHECK, "--keyed", o, k, "--refs", CREFS], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
c, o = runc(CO, w("chi_k.md", CK))
t("keyed Chicago: pages after '(Publisher, Year),' and '(Year):', volume:page, 103n24, roman page, Ibidem opening a "
  "note with more works, DOI/article range not warned -> CHECK OK, no warnings", c == 0 and "CHECK OK" in o and "WARN" not in o, o)
c, o = runc(CO, w("chi_k1.md", CK.replace("s. 119]", "s. 118]")))
t("keyed Chicago: journal page after '(2021):' changed -> ERROR", c == 1 and "note 6" in o and "119" in o, o)
c, o = runc(CO, w("chi_k2.md", CK.replace(" i t. 2, s. 452", "")))
t("keyed Chicago: second volume's page (… and II:452) dropped -> ERROR", c == 1 and "452" in o, o)
c, o = runc(CO, w("chi_k3.md", CK.replace("{s. 73, 103, przyp. 24}", "{s. 73, 103}")))
t("keyed Chicago: note number of '103n24' dropped -> ERROR", c == 1 and "24" in o, o)
c, o = runc(CO, w("chi_k4.md", CK.replace("@galletti2021, s. 121–122", "@galletti2021, s. 121")))
t("keyed Chicago: page after a quoted short title ('…Otro,” 121–22') cut -> ERROR", c == 1 and "122" in o, o)

# On_Culture (stage-1 test 5, Tittel): an Ibidem after a quotation ("Original: „…”, Ibidem.") on the same page as the
# note before; the author's siglum ("hereafter abbreviated as MEW 23") naming the work in later notes, its page a
# locator; a journal volume after a comma before the year ("*CTK*, 7 (2018)") is not a page; a series number
# (collection-number, kept in refs.json) not warned
TREFS = w("onc_refs.json", json.dumps([
    {"id": "marx1962", "type": "book", "author": [{"family": "Marx", "given": "Karl"}], "title": "Das Kapital", "publisher": "Dietz",
     "publisher-place": "Berlin", "collection-title": "Werke", "collection-number": "23", "issued": {"date-parts": [[1962]]}},
    {"id": "zeller1842", "type": "book", "author": [{"family": "Zeller", "given": "G. H."}], "title": "Sammlung der Gesetze",
     "publisher": "Fues", "publisher-place": "Tübingen", "collection-title": "Sammlung", "collection-number": "13",
     "issued": {"date-parts": [[1842]]}},
    {"id": "zhav2018", "type": "article-journal", "author": [{"family": "Zhavoronkov", "given": "Alexey"}], "title": "The Concept of Race",
     "container-title": "CTK", "volume": "7", "page": "275–292", "issued": {"date-parts": [[2018]]}}], ensure_ascii=False))
OO = w("onc_o.md", "A[^1] b[^2] c[^3] d[^4] e[^5] f[^6].\n\n"
       "[^1]: Karl Marx, *Das Kapital*. Werke 23 (Berlin: Dietz, 1962), 743 (hereafter abbreviated as MEW 23).\n\n"
       "[^2]: MEW 23, 746.\n\n"
       "[^3]: G. H. Zeller, *Sammlung der Gesetze*. Sammlung Bd. 13 (Tübingen: Fues, 1842), 822.\n\n"
       "[^4]: Original: “gänzlicher Ausrottung,” Zeller, *Sammlung Bd. 13*, 823.\n\n"
       "[^5]: Original: “todt geschossen,” Zeller, *Sammlung Bd. 13*, 823.\n\n"
       "[^6]: Alexey Zhavoronkov, “The Concept of Race,” in *CTK*, 7 (2018), 275–292.\n")
OK_ = ("A[^1] b[^2] c[^3] d[^4] e[^5] f[^6].\n\n[^1]: [@marx1962, s. 743] (hereafter abbreviated as MEW 23).\n\n"
       "[^2]: [@marx1962, s. 746].\n\n[^3]: [@zeller1842, s. 822].\n\n"
       "[^4]: Original: “gänzlicher Ausrottung,” [@zeller1842, s. 823].\n\n"
       "[^5]: Original: “todt geschossen,” [@zeller1842, s. 823].\n\n[^6]: [@zhav2018].\n")
def runo(o, k):
    r = subprocess.run([sys.executable, CHECK, "--keyed", o, k, "--refs", TREFS], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
c, o = runo(OO, w("onc_k.md", OK_))
t("keyed: Ibidem after a quotation (same page), a siglum introduced by the author (MEW 23), a volume before the year, "
  "series numbers -> CHECK OK, no warnings", c == 0 and "CHECK OK" in o and "WARN" not in o, o)
c, o = runo(OO, w("onc_k1.md", OK_.replace("[@marx1962, s. 746]", "[@marx1962, s. 747]")))
t("keyed: the page after the siglum changed (MEW 23, 746 -> s. 747) -> ERROR", c == 1 and "746" in o, o)
c, o = runo(OO, w("onc_k2.md", OK_.replace("[^2]: [@marx1962, s. 746]", "[^2]: [@zeller1842, s. 746]")))
t("keyed: the siglum's note keyed to another work -> ERROR", c == 1 and "@zeller1842" in o, o)
c, o = runo(OO, w("onc_k3.md", OK_.replace("todt geschossen,” [@zeller1842, s. 823]", "todt geschossen,” [@zeller1842, s. 824]")))
t("keyed: after a quotation, a different page (not the bare Ibidem) -> ERROR", c == 1 and "823" in o, o)
c, o = runo(w("onc_o4.md", open(OO, encoding="utf-8").read().replace("823.\n\n[^5]", "822.\n\n[^5]")), w("onc_k4.md", OK_))
t("keyed: Ibidem after a quotation where the note before cites another page -> ERROR", c == 1 and "823" in o, o)
# a page after "here:" and a Kant Akademie-Ausgabe page ("420/AA VII 324–325") are locators; a volume named in the note
# ("Vol. IV") must be the keyed work's (two volumes by one editor with one title)
HREFS = w("here_refs.json", json.dumps([
    {"id": "decker2018", "type": "chapter", "author": [{"family": "Decker", "given": "Oliver"}], "title": "Die Leipziger Studie",
     "container-title": "Flucht ins Autoritäre", "page": "65–115", "publisher": "PV", "publisher-place": "Gießen", "issued": {"date-parts": [[2018]]}},
    {"id": "kant2010a", "type": "chapter", "author": [{"family": "Kant", "given": "Immanuel"}], "title": "Anthropology",
     "container-title": "AHE", "page": "227–429", "publisher": "CUP", "publisher-place": "Cambridge", "issued": {"date-parts": [[2010]]}},
    {"id": "raithby3", "type": "book", "author": [{"family": "Raithby", "given": "John"}], "title": "The Statutes at Large", "volume": "3",
     "publisher": "EyS", "publisher-place": "London", "issued": {"date-parts": [[1811]]}},
    {"id": "raithby4", "type": "book", "author": [{"family": "Raithby", "given": "John"}], "title": "The Statutes at Large", "volume": "4",
     "publisher": "EyS", "publisher-place": "London", "issued": {"date-parts": [[1811]]}}], ensure_ascii=False))
HO = w("here_o.md", "A[^1] b[^2] c[^3].\n\n"
       "[^1]: Oliver Decker, “Die Leipziger Studie,” in *Flucht ins Autoritäre* (Gießen: PV, 2018), 65–115, here: 102–103.\n\n"
       "[^2]: Immanuel Kant, “Anthropology,” in *AHE* (Cambridge: CUP, 2010), 227–429, here: 420/AA VII 324–325.\n\n"
       "[^3]: Raithby, *Statutes at large Vol. IV*, 233.\n")
HK = ("A[^1] b[^2] c[^3].\n\n[^1]: [@decker2018, s. 102–103].\n\n[^2]: [@kant2010a, {s. 420 / AA VII 324–325}].\n\n"
      "[^3]: [@raithby4, s. 233].\n")
def runh(k):
    r = subprocess.run([sys.executable, CHECK, "--keyed", HO, w("here_k.md", k), "--refs", HREFS], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
c, o = runh(HK)
t("keyed: 'here: 102–103' after the chapter's range, '420/AA VII 324–325', 'Vol. IV' = the work's volume -> CHECK OK",
  c == 0 and "CHECK OK" in o and "WARN" not in o, o)
c, o = runh(HK.replace("s. 102–103]", "s. 102]"))
t("keyed: the page after 'here:' cut (102–103 -> 102) -> ERROR", c == 1 and "103" in o, o)
c, o = runh(HK.replace("{s. 420 / AA VII 324–325}", "s. 420"))
t("keyed: the Akademie-Ausgabe page dropped -> ERROR", c == 1 and "324" in o, o)
c, o = runh(HK.replace("[@raithby4, s. 233]", "[@raithby3, s. 233]"))
t("keyed: 'Vol. IV' keyed to vol. 3 of the same work -> ERROR", c == 1 and "volume [4]" in o, o)

# Manchester UP (stage-1 test 6, West Ohueri): "40:3 (2021)" is volume:issue, "2nd ed." an edition, "26 May 2020" a date —
# none is a page. Works: every work the original cites by surname and title must be cited in the keyed note (dropped from
# a note citing several, swapped for another author's, or cited by the author's short form "Galaty, *Memory*"); a work
# only named in prose ("Kant’s essay “On the Use …”") is not a citation; a title inside another edition's subtitle is not
MREFS = w("mup_refs.json", json.dumps([
    {"id": "wo2021", "type": "article-journal", "author": [{"family": "West Ohueri", "given": "Chelsi"}],
     "title": "On Living and Moving with Zor", "container-title": "MA", "volume": "40", "issue": "3", "page": "241–253",
     "issued": {"date-parts": [[2021]]}},
    {"id": "wo2016", "type": "thesis", "author": [{"family": "West Ohueri", "given": "Chelsi"}], "title": "Mapping Race and Belonging",
     "publisher": "UT Austin", "issued": {"date-parts": [[2016]]}},
    {"id": "cornell2007", "type": "book", "author": [{"family": "Cornell", "given": "Stephen"}], "title": "Ethnicity and Race",
     "edition": "2", "publisher": "PFP", "publisher-place": "Thousand Oaks", "issued": {"date-parts": [[2007]]}},
    {"id": "galaty2018", "type": "book", "author": [{"family": "Galaty", "given": "Michael"}], "title": "Memory and Nation Building",
     "publisher": "RL", "publisher-place": "Lanham", "issued": {"date-parts": [[2018]]}},
    {"id": "mehilli2017", "type": "book", "author": [{"family": "Mëhilli", "given": "Elidor"}], "title": "From Stalin to Mao",
     "publisher": "CUP", "publisher-place": "Ithaca", "issued": {"date-parts": [[2017]]}},
    {"id": "frank1993", "type": "book", "author": [{"family": "Frankenberg", "given": "Ruth"}], "title": "White Women, Race Matters",
     "publisher": "UMP", "publisher-place": "Minneapolis", "issued": {"date-parts": [[1993]]}},
    {"id": "wekker2016", "type": "book", "author": [{"family": "Wekker", "given": "Gloria"}], "title": "White Innocence",
     "publisher": "Duke", "publisher-place": "Durham", "issued": {"date-parts": [[2016]]}},
    {"id": "kant1788", "type": "chapter", "author": [{"family": "Kant", "given": "Immanuel"}],
     "title": "On the Use of Teleological Principles in Philosophy", "container-title": "AHE", "publisher": "CUP",
     "publisher-place": "Cambridge", "issued": {"date-parts": [[2010]]}},
    {"id": "gr1783", "type": "book", "author": [{"family": "Grellmann", "given": "H. M. G."}],
     "title": "Die Zigeuner: Ein historischer Versuch über die Lebensart", "publisher": "BdG", "publisher-place": "Dessau",
     "issued": {"date-parts": [[1783]]}},
    {"id": "gr1787", "type": "book", "author": [{"family": "Grellmann", "given": "H. M. G."}],
     "title": "Historischer Versuch über die Zigeuner", "publisher": "Dieterich", "publisher-place": "Göttingen",
     "issued": {"date-parts": [[1787]]}},
    {"id": "erebara2020", "type": "webpage", "author": [{"family": "Erebara", "given": "Gjergj"}], "title": "Organizatat",
     "container-title": "Reporter.al", "URL": "https://www.reporter.al/x/", "issued": {"date-parts": [[2020, 5, 26]]}}],
    ensure_ascii=False))
MO = w("mup_o.md", "A[^1] b[^2] c[^3] d[^4] e[^5] f[^6] g[^7].\n\n"
       "[^1]: Chelsi West Ohueri, ‘On Living and Moving with Zor’, *MA*, 40:3 (2021), 241–53.\n\n"
       "[^2]: Stephen Cornell, *Ethnicity and Race*, 2nd ed. (Thousand Oaks: PFP, 2007).\n\n"
       "[^3]: Gjergj Erebara, ‘Organizatat’, *Reporter.al*, 26 May 2020, www.reporter.al/x/.\n\n"
       "[^4]: Galaty, *Memory*; Elidor Mëhilli, *From Stalin to Mao* (Ithaca: CUP, 2017), 12.\n\n"
       "[^5]: See West Ohueri, ‘Mapping Race’; West Ohueri, ‘Zor’.\n\n"
       "[^6]: Here I return to both Wekker (*White Innocence*) and Frankenburg (*White Women, Race Matters*). Kant’s essay "
       "“On the Use of Teleological Principles in Philosophy” is often cited.\n\n"
       "[^7]: See H. M. G. Grellmann, *Die Zigeuner*: *Ein historischer Versuch über die Lebensart* (Dessau: BdG, 1783).\n")
MK = ("A[^1] b[^2] c[^3] d[^4] e[^5] f[^6] g[^7].\n\n[^1]: [@wo2021].\n\n[^2]: [@cornell2007].\n\n[^3]: [@erebara2020].\n\n"
      "[^4]: [@galaty2018; @mehilli2017, s. 12].\n\n[^5]: Zob. [@wo2016; @wo2021].\n\n"
      "[^6]: Here I return to both Wekker ([@wekker2016]) and Frankenburg ([@frank1993]). Kant’s essay "
      "“On the Use of Teleological Principles in Philosophy” is often cited.\n\n[^7]: Zob. [@gr1783].\n")
def runm(k):
    r = subprocess.run([sys.executable, CHECK, "--keyed", MO, w("mup_k.md", k), "--refs", MREFS], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
c, o = runm(MK)
t("keyed MUP: volume:issue '40:3 (2021)', '2nd ed.', '26 May 2020' are not pages; a work named in prose, a title inside "
  "another edition's subtitle -> CHECK OK", c == 0 and "CHECK OK" in o and "ERROR" not in o, o)
c, o = runm(MK.replace("[@galaty2018; @mehilli2017, s. 12]", "[@mehilli2017, s. 12]"))
t("keyed: a work cited by the author's short form ('Galaty, *Memory*') dropped -> ERROR", c == 1 and "@galaty2018" in o, o)
c, o = runm(MK.replace("Zob. [@wo2016; @wo2021]", "Zob. [@wo2016]"))
t("keyed: the author's second work ('West Ohueri, ‘Zor’') dropped -> ERROR", c == 1 and "@wo2021" in o, o)
c, o = runm(MK.replace("Frankenburg ([@frank1993])", "Frankenburg ([@wekker2016])"))
t("keyed: a key swapped for another author's named in the same note (misspelt 'Frankenburg') -> ERROR",
  c == 1 and "@frank1993" in o, o)
c, o = runm(MK.replace("[^4]: [@galaty2018; @mehilli2017, s. 12]", "[^4]: [@galaty2018; @mehilli2017, s. 13]"))
t("keyed MUP: a page after the imprint parenthesis still counts (12 -> 13) -> ERROR", c == 1 and "12" in o, o)

# an edited volume cited as "Turda and Weindling (eds), *Blood and Homeland*" beside another book by Turda: dropping it
# must fail (found by mutate_keyed.py on West Ohueri n. 48); and mutate_keyed.py itself: every mutant caught here
EREFS = w("eds_refs.json", json.dumps([
    {"id": "turda2007", "type": "book", "editor": [{"family": "Turda", "given": "Marius"}, {"family": "Weindling", "given": "Paul J."}],
     "title": "Blood and Homeland", "publisher": "CEU Press", "publisher-place": "Budapest", "issued": {"date-parts": [[2007]]}},
    {"id": "turda2010", "type": "book", "author": [{"family": "Turda", "given": "Marius"}], "title": "Modernism and Eugenics",
     "publisher": "Palgrave", "publisher-place": "Basingstoke", "issued": {"date-parts": [[2010]]}},
    {"id": "bucur2010", "type": "book", "author": [{"family": "Bucur", "given": "Maria"}], "title": "Eugenics in Eastern Europe",
     "publisher": "OUP", "publisher-place": "Oxford", "issued": {"date-parts": [[2010]]}}], ensure_ascii=False))
EO = w("eds_o.md", "A[^1] b[^2].\n\n[^1]: Marius Turda and Paul J. Weindling (eds), *Blood and Homeland* (Budapest: CEU Press, "
       "2007); Marius Turda, *Modernism and Eugenics* (Basingstoke: Palgrave, 2010), 12.\n\n"
       "[^2]: Maria Bucur, *Eugenics in Eastern Europe* (Oxford: OUP, 2010), 5; Turda, *Modernism*, 14.\n")
EK = "A[^1] b[^2].\n\n[^1]: [@turda2007; @turda2010, s. 12].\n\n[^2]: [@bucur2010, s. 5; @turda2010, s. 14].\n"
r = subprocess.run([sys.executable, CHECK, "--keyed", EO, w("eds_k.md", EK.replace("@turda2007; ", "")), "--refs", EREFS],
                   capture_output=True, text=True)
t("keyed: an edited volume ('Turda and Weindling (eds), *Title*') dropped beside another book by Turda -> ERROR",
  r.returncode == 1 and "@turda2007" in r.stdout, r.stdout)
MUT = os.path.join(os.path.dirname(CHECK), "mutate_keyed.py")
r = subprocess.run([sys.executable, MUT, EO, w("eds_k0.md", EK), "--refs", EREFS], capture_output=True, text=True)
m = re.search(r"MUTATIONS CAUGHT (\d+)/(\d+)", r.stdout)
t("mutate_keyed.py: page+1, nopage, drop and swap mutants of a clean keyed file are all caught (exit 0)",
  r.returncode == 0 and m and m.group(1) == m.group(2) and int(m.group(2)) >= 8, r.stdout + r.stderr)
r = subprocess.run([sys.executable, MUT, EO, w("eds_k1.md", EK), "--refs", EREFS, "--max", "3"], capture_output=True, text=True)
t("mutate_keyed.py --max 3: three mutants", "MUTATIONS CAUGHT 3/3" in r.stdout, r.stdout + r.stderr)

# author-only short forms (Ndiaye: "Taylor, 66–86; Cressy."; "various essays in Hendricks and Parker; Nocentelli."): a work
# dropped from such a note -> ERROR (found by mutate_keyed.py on Ndiaye nn. 60, 120); a surname in prose is not a citation
AREFS = w("ao_refs.json", json.dumps([
    {"id": "taylor2014", "type": "book", "author": [{"family": "Taylor", "given": "Becky"}], "title": "Another Darkness",
     "publisher": "Reaktion", "publisher-place": "London", "issued": {"date-parts": [[2014]]}},
    {"id": "cressy2016", "type": "book", "author": [{"family": "Cressy", "given": "David"}], "title": "Trouble with the Gypsies",
     "publisher": "OUP", "publisher-place": "Oxford", "issued": {"date-parts": [[2016]]}},
    {"id": "hend1994", "type": "book", "editor": [{"family": "Hendricks", "given": "Margo"}, {"family": "Parker", "given": "Patricia"}],
     "title": "Women, Race, and Writing", "publisher": "Routledge", "publisher-place": "London", "issued": {"date-parts": [[1994]]}},
    {"id": "noc2013", "type": "book", "author": [{"family": "Nocentelli", "given": "Carmen"}], "title": "Empires of Love",
     "publisher": "UPP", "publisher-place": "Philadelphia", "issued": {"date-parts": [[2013]]}}], ensure_ascii=False))
AO = w("ao_o.md", "A[^1] b[^2] c[^3].\n\n[^1]: Taylor, 66–86; Cressy.\n\n"
       "[^2]: On gendered rhetoric, see various essays in Hendricks and Parker; Nocentelli.\n\n"
       "[^3]: As Cressy has shown, this was common; see Taylor, 70.\n")
AK = ("A[^1] b[^2] c[^3].\n\n[^1]: [@taylor2014, s. 66–86; @cressy2016].\n\n"
      "[^2]: On gendered rhetoric, zob. various essays in [@hend1994; @noc2013].\n\n"
      "[^3]: As Cressy has shown, this was common; zob. [@taylor2014, s. 70].\n")
def runa(k):
    r = subprocess.run([sys.executable, CHECK, "--keyed", AO, w("ao_k.md", k), "--refs", AREFS], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
c, o = runa(AK)
t("keyed, author-only short forms: all works cited; a surname in prose ('As Cressy has shown') -> CHECK OK", c == 0, o)
c, o = runa(AK.replace("[@taylor2014, s. 66–86; @cressy2016]", "[@cressy2016]"))
t("keyed: 'Taylor, 66–86' dropped from 'Taylor, 66–86; Cressy.' -> ERROR", c == 1 and "@taylor2014" in o, o)
c, o = runa(AK.replace("[@hend1994; @noc2013]", "[@noc2013]"))
t("keyed: 'Hendricks and Parker' dropped -> ERROR", c == 1 and "@hend1994" in o, o)

# --pair: a sentence dropped from one paragraph -> length warning on that block only (never an error)
EN = ["Paragraph %d opens with a sentence about the camp near the river and the people who lived there for years. "
      "The second sentence describes the road, the market and the long winter of that particular year in detail. "
      "The third sentence names the families, their trades, their horses and the officials who counted them all. "
      "The last sentence closes the paragraph with a remark about the archive where the records are kept today." % i for i in range(1, 7)]
PL = ["Akapit %d zaczyna się zdaniem o obozowisku nad rzeką i o ludziach, którzy mieszkali tam przez wiele lat. "
      "Drugie zdanie opisuje drogę, targ i długą zimę tamtego roku, ze wszystkimi jej szczegółami i trudnościami. "
      "Trzecie zdanie wymienia rodziny, ich zajęcia, konie i urzędników, którzy wszystkich skrupulatnie liczyli. "
      "Ostatnie zdanie zamyka akapit uwagą o archiwum, w którym przechowuje się dziś te wszystkie akta." % i for i in range(1, 7)]
es = w("len_en.md", "\n\n".join(EN) + "\n")
cut = PL[:]; cut[3] = cut[3].split(". Drugie")[0] + ". Ostatnie zdanie zamyka akapit uwagą o archiwum."
c, o = run("--pair", es, w("len_pl.md", "\n\n".join(cut) + "\n"))
c0, o0 = run("--pair", es, w("len_pl0.md", "\n\n".join(PL) + "\n"))
t("--pair: a paragraph missing sentences -> WARN on that block (not an error); the full translation: no warning",
  c == 0 and "block 4: length" in o and "missing" in o and "length" not in o0, o + o0)

n, ok = len(results), sum(results)
print(f"CHECK ALL PASS {n}/{n}" if ok == n else f"CHECK FAILED {n - ok}/{n}")
