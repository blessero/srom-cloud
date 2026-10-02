#!/usr/bin/env python3
"""tlumacz-test_handoff.py — contract test of the srom-produkcja handoff (references/handoff.md) as srom-tlumacz uses it.

Run after any srom-produkcja update. Builds fixtures in a temp dir and checks the verdicts of
check.py --pair, export_work.py/docx_in.py round trip, build.py --queries header handling and
cite_map.py audit. KNOWN GAP lines document behaviour that srom-produkcja is asked to change
(../_handoffs/tlumacz-to-produkcja.md); they do not count as failures until the change lands, then flip.

Last line: HANDOFF CONTRACT n/n  (exit 0 only if every contract case holds)
"""
import glob, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlumacz_paths import skill_dir
_T = os.environ.get("SROM_TYPESET") or skill_dir("srom-produkcja")
S = os.path.join(_T, "scripts") if _T and os.path.exists(os.path.join(_T, "scripts", "check.py")) else None
if not S:
    print("srom-produkcja not found (set SROM_TYPESET)"); sys.exit(2)
try:
    import docx  # noqa: F401  srom-produkcja's scripts run under this interpreter (sys.executable)
except ImportError:
    print(f"python-docx missing for {sys.executable}: run with ~/.venvs/srom/bin/python"); sys.exit(2)
D = tempfile.mkdtemp()


def w(name, text):
    p = os.path.join(D, name); open(p, "w", encoding="utf-8").write(text); return p


def pair(src, tgt, refs=None):
    extra = [a for f in (refs or [REFS]) for a in ("--refs", f)]
    r = subprocess.run([sys.executable, os.path.join(S, "check.py"), "--pair", src, tgt] + extra,
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


REFS = w("refs.json", """[
{"id":"fic1989","type":"book","author":[{"family":"Ficowski","given":"Jerzy"}],"title":"The Gypsies in Poland","issued":{"date-parts":[[1989]]},"publisher":"Interpress","publisher-place":"Warsaw"},
{"id":"fic1985","type":"book","author":[{"family":"Ficowski","given":"Jerzy"}],"title":"Cyganie na polskich drogach","issued":{"date-parts":[[1985]]},"publisher":"Wydawnictwo Literackie","publisher-place":"Kraków"}]
""")
SRC = w("src.md", "# 1. INTRODUCTION\n\nThe Great Halt was imposed in 1964.[^1] Second sentence.\n\n[^1]: [@fic1989, p. 15].\n\nThird paragraph.\n")
GOOD = ("# 1. WSTĘP\n\nWielki Postój wprowadzono w 1964 roku[^1]. Drugie zdanie[^t1].\n\n"
        "[^1]: [@fic1985, s. 15]; <!-- DODANO: @fic1985 --> autor cytuje za: [@fic1989, s. 15].\n\n"
        "[^t1]: Objaśnienie – przyp. tłum.\n\nTrzeci akapit.\n")

cases = []  # (name, passed, known_gap)


def expect(name, cond, gap=False):
    cases.append((name, bool(cond), gap))


rc, out = pair(SRC, w("good.md", GOOD))
expect("translator note + declared addition pass", rc == 0 and "CHECK OK" in out)
rc, out = pair(SRC, w("undecl.md", GOOD.replace("<!-- DODANO: @fic1985 --> ", "")))
expect("undeclared added citation fails", rc == 1 and "undeclared addition" in out)
rc, out = pair(SRC, w("noformula.md", GOOD.replace(" – przyp. tłum.", "")))
expect("translator note without formula fails", rc == 1)
rc, out = pair(SRC, w("disguise.md", "# 1. WSTĘP\n\nWielki Postój wprowadzono w 1964 roku[^t1]. Drugie zdanie.\n\n"
                                     "[^t1]: [@fic1989, s. 15] – przyp. tłum.\n\nTrzeci akapit.\n"))
expect("author note relabelled as translator note fails", rc == 1)
rc, out = pair(SRC, w("split.md", GOOD.replace(" Drugie zdanie", "\n\nDrugie zdanie")))
expect("paragraph split fails", rc == 1)
rc, out = pair(SRC, w("dropped.md", GOOD.replace(" autor cytuje za: [@fic1989, s. 15]", "")))
expect("author's citation removed fails", rc == 1)
rc, out = pair(SRC, w("unknown.md", GOOD.replace("@fic1985", "@xyz2000")))
expect("declared key missing from refs.json fails", rc == 1 and "not in refs.json" in out)

# E8 (26.09.2026): editorial notes [^r<n>] + "– przyp. red." join the non-author series; label and formula must agree;
# a bracketed "[… – przyp. tłum.]" inside an author's note leaves it an author's note
EDIT = GOOD.replace("Trzeci akapit.", "Trzeci akapit[^r1].").rstrip("\n") + "\n\n[^r1]: Uwaga redakcji – przyp. red.\n"
rc, out = pair(SRC, w("rnote.md", EDIT))
expect("editorial note [^r1] with – przyp. red. passes", rc == 0 and "CHECK OK" in out)
rc, out = pair(SRC, w("rmismatch.md", EDIT.replace("– przyp. red.", "– przyp. tłum.")))
expect("editorial label with translator formula fails", rc == 1)
rc, out = pair(SRC, w("bracket.md", GOOD.replace("[@fic1989, s. 15].", "[@fic1989, s. 15] [obecnie Interpress – przyp. tłum.].")))
expect("bracketed translator gloss inside an author's note stays an author's note", rc == 0 and "CHECK OK" in out)

# Declaration by "srom-added" in <id>_refs_tlum.json (contract since 26.09.2026): no in-note comment needed
REFS_SRC = w("refs_src.json", "[" + open(REFS, encoding="utf-8").read().split("},\n", 1)[0].lstrip("[").strip() + "}]")
REFS_TLUM = w("refs_tlum.json", "[" + open(REFS, encoding="utf-8").read().split("},\n", 1)[1].rstrip().rstrip("]").replace(
    '"publisher-place":"Kraków"}', '"publisher-place":"Kraków","srom-added":"tlum","srom-source":"https://example.org/catalogue/fic1985"}') + "]")
PLAIN = GOOD.replace("<!-- DODANO: @fic1985 --> ", "")
plain = w("plain.md", PLAIN)
rc, out = pair(SRC, plain, [REFS_SRC, REFS_TLUM])
expect("addition declared by srom-added in refs_tlum.json passes", rc == 0 and "CHECK OK" in out)
rc, out = pair(SRC, plain, [REFS_SRC, w("refs_tlum_undecl.json", open(REFS_TLUM, encoding="utf-8").read().replace('"srom-added":"tlum",', ""))])
expect("same addition without srom-added fails", rc == 1 and "undeclared addition" in out)

# Word working-copy round trip: in-note comments are dropped by design; the refs_tlum.json declaration survives,
# and the translator note ([^t1] -> [^2]) is still recognised by its formula
good = os.path.join(D, "good.md")
docx = os.path.join(D, "plain_robocza.docx"); back = os.path.join(D, "back.md")
subprocess.run([sys.executable, os.path.join(S, "export_work.py"), plain, "-o", docx], capture_output=True)
subprocess.run([sys.executable, os.path.join(S, "docx_in.py"), docx, "-o", back], capture_output=True)
rc, out = pair(SRC, back, [REFS_SRC, REFS_TLUM]) if os.path.exists(back) else (9, "no round-trip file")
expect("Word round trip: srom-added declaration holds, translator note still recognised",
       rc == 0 and "left out of the comparison" in out)

# query sheet: wrong header is reported, right one accepted
bad_q = w("q_bad.csv", "\ufeffkto;co\nautor;x\n")
ok_q = w("q_ok.csv", "\ufeffadresat;rodzaj;przypis;dzieło;szczegóły\nredakcja;termin otwarty — rozstrzygnąć;1;;test\n")
out_dir = os.path.join(D, "build")
r = subprocess.run([sys.executable, os.path.join(S, "build.py"), back, "--refs", REFS, "--out", out_dir,
                    "--queries", ok_q, "--queries", bad_q, "--draft"], capture_output=True, text=True)
sheet = next(iter(glob.glob(os.path.join(out_dir, "*_pytania.csv"))), None)
merged = sheet and "termin otwarty" in open(sheet, encoding="utf-8-sig").read()
rep = " ".join(open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(out_dir, "*_report.md")))
expect("--queries merges a valid sheet and reports a bad header", merged and "query sheet header must be" in rep)

# E10/T7 (27.09.2026): translator in YAML front matter `tlumaczenie:` — ignored by the pair check, not printed,
# reported for the master CSV as translators_struct, kept through the Word round trip; an empty value fails the build
FM = "---\ntlumaczenie:\n  - \"Anna Maria Kowalska\"\n  - \"Jan Nowak\"\n---\n\n"
fm = w("fm.md", FM + PLAIN)
rc, out = pair(SRC, fm, [REFS_SRC, REFS_TLUM])
expect("E10: front matter tlumaczenie is ignored by the pair check", rc == 0 and "CHECK OK" in out)
fm_dir = os.path.join(D, "build_fm")
subprocess.run([sys.executable, os.path.join(S, "build.py"), fm, "--refs", REFS, "--out", fm_dir, "--draft"], capture_output=True, text=True)
rep = " ".join(open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(fm_dir, "*_report.md")))
expect("E10: build reports translators_struct for the CSV",
       "`Anna Maria|Kowalska|| ;; Jan|Nowak||`" in rep and "is empty" not in rep)
fm0_dir = os.path.join(D, "build_fm0")
subprocess.run([sys.executable, os.path.join(S, "build.py"), w("fm0.md", '---\ntlumaczenie: ""\n---\n\n' + PLAIN),
                "--refs", REFS, "--out", fm0_dir, "--draft"], capture_output=True, text=True)
rep0 = " ".join(open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(fm0_dir, "*_report.md")))
expect("E10: empty tlumaczenie is a build error", "front matter 'tlumaczenie' is empty" in rep0)
fm_docx = os.path.join(D, "fm_robocza.docx"); fm_back = os.path.join(D, "fm_back.md")
subprocess.run([sys.executable, os.path.join(S, "export_work.py"), fm, "-o", fm_docx], capture_output=True)
subprocess.run([sys.executable, os.path.join(S, "docx_in.py"), fm_docx, "-o", fm_back], capture_output=True)
txt = open(fm_back, encoding="utf-8").read() if os.path.exists(fm_back) else ""
expect("E10: Word round trip keeps both translators",
       txt.startswith("---\ntlumaczenie:") and '"Anna Maria Kowalska"' in txt and '"Jan Nowak"' in txt)

# T14/T15, D12 (28.09.2026): one title note per article — translation note first, the author's note on the title as a
# further paragraph of the same ::: przypis-tytulowy block; two blocks are an error
TN = "::: przypis-tytulowy\nPierwodruk: A. Autor, *Title*. Tłumaczenie: Michał Bartosz.\n\nDziękuję recenzentom.\n:::\n\n"
rc, out = pair(SRC, w("tn_one.md", TN + PLAIN), [REFS_SRC, REFS_TLUM])
expect("D12: one title-note block with two paragraphs passes", rc == 0 and "CHECK OK" in out)
rc, out = pair(SRC, w("tn_two.md", TN.replace("\n\nDziękuję", "\n:::\n\n::: przypis-tytulowy\nDziękuję") + PLAIN), [REFS_SRC, REFS_TLUM])
expect("D12: two title-note blocks fail", rc == 1 and "title-note blocks" in out)

tn_docx = os.path.join(D, "tn_robocza.docx"); tn_back = os.path.join(D, "tn_back.md")
subprocess.run([sys.executable, os.path.join(S, "export_work.py"), os.path.join(D, "tn_one.md"), "-o", tn_docx], capture_output=True)
subprocess.run([sys.executable, os.path.join(S, "docx_in.py"), tn_docx, "-o", tn_back], capture_output=True)
rc, out = pair(SRC, tn_back, [REFS_SRC, REFS_TLUM]) if os.path.exists(tn_back) else (9, "no round-trip file")
expect("E16: Word round trip keeps the two-paragraph title note as one block", rc == 0 and "CHECK OK" in out, gap=True)

# T11 (28.09.2026): header data both ways — <id>_src_front.md out, <id>_front_pl.md back (Kanon § 12.2.2).
# The contract names both files; srom-produkcja has no checker for the Polish one, so ours is tested here.
HO = open(os.path.join(_T, "references", "handoff.md"), encoding="utf-8").read()
expect("T11: handoff.md names <id>_src_front.md and <id>_front_pl.md", "`<id>_src_front.md`" in HO and "`<id>_front_pl.md`" in HO)
FSRC = w("x_src_front.md", "Black Roma: Afro-Romani Connections\n\nA. AUTHOR, *University*\n\n*This essay shows.*\n")
FPL = ("# Tytuł\nCzarni Romowie\n\n# Podtytuł\nAfroromskie powiązania\n\n# Abstrakt\nArtykuł pokazuje.\n\n"
       "# Słowa kluczowe\nRomowie; dramat; rasa; niewolnictwo; Molière\n\n"
       "# Keywords\nRoma; drama; race; slavery; Molière\n<!-- do zatwierdzenia przez autora -->\n")
FC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tlumacz-front_check.py")
def front(pl):
    r = subprocess.run([sys.executable, FC, FSRC, w("x_front_pl.md", pl)], capture_output=True, text=True)
    return r.returncode, r.stdout
rc, out = front(FPL)
expect("T11: well-formed <id>_front_pl.md passes", rc == 0 and out.rstrip().endswith("FRONT OK"))
rc, out = front(FPL.replace("Afroromskie powiązania", "—"))
expect("T11: subtitle of the original dropped fails", rc == 1 and "keep title and subtitle apart" in out)
rc, out = front(FPL.replace("; Molière\n\n# Keywords", "\n\n# Keywords"))
expect("T11: four keywords fail (5–10)", rc == 1 and "4 keywords" in out)
rc, out = front(FPL.replace("<!-- do zatwierdzenia przez autora -->\n", ""))
expect("T11: drafted English keywords without the approval line fail", rc == 1 and "do zatwierdzenia" in out)

# E3, E5 (27.09.2026, T1): contract text only — the literal-note rule and the terminology slot with the fixed CLI
expect("E3: handoff.md keeps the literal-note rule (kanon § 8: fol. → k., file → sygn., fond → zespół)",
       "Literal notes" in HO and "fol. → k., file → sygn., fond → zespół" in HO)
expect("E5: handoff.md keeps the terminology slot with the fixed tb_check.py CLI",
       "tb_check.py <id>_src.md <id>_pl.md --tb tlumacz-tb.tsv --csv <id>_pytania_tb.csv" in HO)

# E6 (27.09.2026, T1): query rows name the source note label; build.py --pair-src turns it into the printed number.
# A case where the three differ: a citation in the main text takes printed note 1, and two translator notes (no
# number, * series) shift the labels after the Word round trip. Source label 3 -> target label 5 -> printed 4.
SRC6 = w("src6.md", "Intro [@fic1989, s. 3] text.[^1] More.[^2] End.[^3]\n\n[^1]: First.\n\n[^2]: Second.\n\n[^3]: Third.\n")
PL6 = w("pl6.md", "Wstęp [@fic1989, s. 3] tekst[^1]. Dalej[^t1][^2]. Koniec[^t2][^3].\n\n[^1]: Pierwszy.\n\n"
                  "[^t1]: Uwaga – przyp. tłum.\n\n[^2]: Drugi.\n\n[^t2]: Druga uwaga – przyp. tłum.\n\n[^3]: Trzeci.\n")
Q6 = w("q6.csv", "\ufeffadresat;rodzaj;przypis;dzieło;szczegóły\nautor;q-two;2;;x\nautor;q-three;3;;y\nredakcja;q-body;;;akapit 1\n")
pl6_docx = os.path.join(D, "pl6_robocza.docx"); pl6_back = os.path.join(D, "pl6_back.md")
subprocess.run([sys.executable, os.path.join(S, "export_work.py"), PL6, "-o", pl6_docx], capture_output=True)
subprocess.run([sys.executable, os.path.join(S, "docx_in.py"), pl6_docx, "-o", pl6_back], capture_output=True)
back6 = open(pl6_back, encoding="utf-8").read() if os.path.exists(pl6_back) else ""
rc, out = pair(SRC6, pl6_back) if back6 else (9, "no round-trip file")
expect("E6: fixture survives the Word round trip (labels renumbered, CHECK OK)", rc == 0 and "[^5]: Trzeci." in back6)
def rows6(extra):
    od = tempfile.mkdtemp(dir=D)
    subprocess.run([sys.executable, os.path.join(S, "build.py"), pl6_back, "--refs", REFS, "--out", od, "--queries", Q6,
                    "--draft"] + extra, capture_output=True, text=True)
    f = next(iter(glob.glob(os.path.join(od, "*_pytania.csv"))), None)
    return {r.split(";")[1]: r.split(";")[2] for r in open(f, encoding="utf-8-sig").read().splitlines()[1:]} if f else {}
m = rows6(["--pair-src", SRC6])
expect("E6: --pair-src maps source labels 2, 3 to printed 3, 4; a row without a label stays empty",
       m.get("q-two") == "3" and m.get("q-three") == "4" and m.get("q-body") == "")
m0 = rows6([])
expect("E6 control: without --pair-src the cells keep the source labels 2, 3", m0.get("q-two") == "2" and m0.get("q-three") == "3")

# T26 (29.09.2026): the hand-back ("Back" in handoff.md). The Word file in our work/<id>/ is the master; we import it
# with docx_in.py (the md is never edited by hand) and name the files with sha256 in a delivery E-item; srom-produkcja
# takes them with take_back.py, which re-imports the master and requires the md to equal that import byte for byte.
import hashlib, shutil
expect("T26: handoff.md 'Back' — Word master in srom-tlumacz's work/<id>/, delivery E-item, take_back.py",
       "## Back:" in HO and "that Word file is the\n   master" in HO and "delivery: …" in HO and "take_back.py" in HO)
TB = os.path.join(S, "take_back.py")
DL = os.path.join(D, "tl", "work", "x"); SD = os.path.join(D, "ts", "work", "x")
os.makedirs(DL); os.makedirs(SD)
shutil.copy(SRC, os.path.join(SD, "x_src.md")); shutil.copy(REFS_SRC, os.path.join(SD, "refs.json"))
subprocess.run([sys.executable, os.path.join(S, "export_work.py"), plain, "-o", os.path.join(DL, "x_robocza.docx")], capture_output=True)
subprocess.run([sys.executable, os.path.join(S, "docx_in.py"), os.path.join(DL, "x_robocza.docx"), "-o", os.path.join(DL, "x_pl.md")], capture_output=True)
shutil.copy(REFS_TLUM, os.path.join(DL, "x_refs_tlum.json"))
open(os.path.join(DL, "x_front_pl.md"), "w", encoding="utf-8").write(FPL)
def sha(n, short=False):
    h = hashlib.sha256(open(os.path.join(DL, n), "rb").read()).hexdigest()
    return f"{h[:8]}…{h[-7:]}" if short else h
def take(names, short=False):
    exp = [a for n in names for a in ("--expect", f"{n}={sha(n, short)}")]
    r = subprocess.run([sys.executable, TB, DL, "x", "--src-dir", SD, "--out", tempfile.mkdtemp(dir=D)] + exp,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
FILES = ["x_robocza.docx", "x_pl.md", "x_front_pl.md", "x_refs_tlum.json"]
rc, last = take(FILES, short=True)
expect("T26: delivery (Word master + its import + front + refs_tlum, sha256 as first8…last7) → TAKE-BACK OK",
       rc == 0 and last[0].startswith("TAKE-BACK OK x"))
open(os.path.join(DL, "x_pl.md"), "a", encoding="utf-8").write("\nDopisane ręcznie.\n")
rc, last = take(FILES)
expect("T26 control: md edited by hand after the import fails the take-back", rc != 0 and "FAILED" in last[0])

# T30 (01.10.2026): the editor's master may be a _v2 file; at delivery we rename it to <id>_robocza.docx (older exports
# to <id>_robocza_old<n>.docx), import it, and the take-back works as for any master.
shutil.copy(os.path.join(DL, "x_robocza.docx"), os.path.join(DL, "x_robocza_v2.docx"))
shutil.move(os.path.join(DL, "x_robocza.docx"), os.path.join(DL, "x_robocza_old1.docx"))
shutil.move(os.path.join(DL, "x_robocza_v2.docx"), os.path.join(DL, "x_robocza.docx"))
subprocess.run([sys.executable, os.path.join(S, "docx_in.py"), os.path.join(DL, "x_robocza.docx"), "-o", os.path.join(DL, "x_pl.md")], capture_output=True)
rc, last = take(FILES, short=True)
expect("T30: a _v2 master renamed to x_robocza.docx (old export → x_robocza_old1.docx) → TAKE-BACK OK",
       rc == 0 and last[0].startswith("TAKE-BACK OK x"))

# KNOWN GAPS (requests E1, E2, E4): these should flip when srom-produkcja changes
rc, out = pair(w("ex_s.md", "A.\n\n::: przyklad\n```\nme dikhav o kher\nI see.1SG DEF house\n'I see the house'\n```\n:::\n\nB.\n"),
               w("ex_t.md", "A.\n\n::: przyklad\n```\nme dikhaw o kher\nja widzieć.1SG DEF dom\n‘widzę dom’\n```\n:::\n\nB.\n"))
expect("E1: altered Romani form line in ::: przyklad is caught", rc == 1, gap=True)
bib = w("bib.txt", "Ficowski, Jerzy. 1989. The Gypsies in Poland. Warsaw: Interpress.\n")
refs_added = w("refs_added.json", open(REFS, encoding="utf-8").read().replace(
    '"publisher-place":"Kraków"}',
    '"publisher-place":"Kraków","srom-added":"tlum","srom-source":"catalogue record URL or ISBN verified by the translator"}'))
r = subprocess.run([sys.executable, os.path.join(S, "cite_map.py"), "audit", "--refs", refs_added, "--bib", bib], capture_output=True, text=True)
expect("E2: translator-added refs entry passes the audit when declared", r.returncode == 0, gap=True)
rc, out = pair(SRC, good)
expect("E4: numbers from added citation keys not reported", "only in target {1985" not in out, gap=True)

held = [c for c in cases if not c[2]]
for name, ok, gap in cases:
    tag = ("KNOWN GAP " if gap and not ok else "GAP CLOSED " if gap else "") + ("ok" if ok else "FAIL")
    print(f"  {tag:>15}  {name}")
print(f"HANDOFF CONTRACT {sum(ok for _, ok, _ in held)}/{len(held)}")
sys.exit(0 if all(ok for _, ok, _ in held) else 1)
