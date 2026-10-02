"""G9: the srom-kanon skill's linter reports zero ERRORs on the rendered sample,
and — negative control — does report errors on a known-bad text and fails the build."""
import os, sys, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FX = os.path.join(ROOT, "tests", "fixtures")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import kanon_path
KDIR = kanon_path.find_kanon()
if not KDIR:
    print("LINT FAILED — " + kanon_path.MISSING); sys.exit(1)
LINT = kanon_path.linter(KDIR)
out = tempfile.mkdtemp()
subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), os.path.join(FX, "sample_article.md"),
                "--refs", os.path.join(FX, "kanon_refs.json"), "--out", out], capture_output=True)
txt = os.path.join(out, "sample_article.txt")
lo = subprocess.run([sys.executable, LINT, txt], capture_output=True, text=True).stdout
bad = os.path.join(out, "bad.txt")
open(bad, "w", encoding="utf-8").write('Tekst "cytat" i op. cit. oraz 1990-2000.\n')
lb = subprocess.run([sys.executable, LINT, bad], capture_output=True, text=True).stdout
control = "--- ERROR ---" in lb and "ABBR-OPCIT" in lb
# BIB-COLON: an imprint colon is an error, the ethnonym Roma before a colon in prose is not (Roma = Rome in the list)
open(bad, "w", encoding="utf-8").write("J. Kowalski, Tytuł, Kraków: Universitas 2001. Historia Romów: a phase, the French Roma: faza.\n"
                                       "Pierwodruk: N. Ndiaye, Black Roma: Afro-Romani Connections (E15, a title).\n"
                                       "Smith, J. (2001). Title. London: Routledge.\n")
lc = subprocess.run([sys.executable, LINT, bad], capture_output=True, text=True).stdout
control = control and lc.count("[BIB-COLON]") == 2
# build must fail on lint ERROR: '"' survives normalisation only if normalise was skipped; op. cit. in a literal note
md = os.path.join(out, "opcit.md")
open(md, "w", encoding="utf-8").write("Tekst[^1].\n\n[^1]: Kowalski, op. cit., s. 5.\n")
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), md, "--out", out], capture_output=True, text=True)
rep = open(os.path.join(out, "opcit_report.md"), encoding="utf-8").read()
blocks = r.returncode == 1 and "kanon linter:" in rep
# build --source (proof of an untranslated source): Polish typography is counted, not an error; the rest still is
src = os.path.join(out, "en_src.md")
open(src, "w", encoding="utf-8").write("An essay—in English—about “Roma.” [...][^1]\n\n[^1]: Kowalski, op. cit., 5.\n")
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), src, "--out", out, "--source"], capture_output=True, text=True)
rep = open(os.path.join(out, "en_src_report.md"), encoding="utf-8").read()
errs = rep.split("## Errors")[1].split("##")[0]
source_ok = ("## Source language" in rep and "no em dash: 2" in rep and "EMDASH" not in errs
             and "no English quotes" not in errs and "ASCII ellipsis" not in errs and "ELLIPSIS-DOTS" in rep.split("## Source language")[1].split("##")[0]
             and "kanon linter: 1 ERROR" in errs)   # op. cit. stays an error
print("source proof: typography counted, op. cit. still an error:", source_ok)
blocks = blocks and source_ok
# Kanon § 12.3 (spelling from 01.01.2026): WARN, never ERROR; surnames, pronoun nie and verb forms stay silent
open(bad, "w", encoding="utf-8").write(
    "Tu jest Molierowski przekład i ujęcie Kantowskie, dane nie znane, osoby nie będące Romami.\n"
    "J. Ficowski pisze, że według Ficowskiego nie zostaną przez nie kształtowani. Kowalski, Jan.\n"
    "Zdanie. Kantowskie pytanie zaczyna zdanie.\n")
lo2 = subprocess.run([sys.executable, LINT, bad], capture_output=True, text=True)
orth = (lo2.stdout.count("[ORTH-OWSKI]") == 2 and lo2.stdout.count("[ORTH-NIE-IMIESLOW]") == 2
        and lo2.returncode == 0)
open(bad, "w", encoding="utf-8").write("Pisał, mimo, że nie mógł; zwłaszcza że wiedział. Myślę chyba, że tak.\n")
lo3 = subprocess.run([sys.executable, LINT, bad], capture_output=True, text=True)
orth = orth and lo3.stdout.count("[PUNCT-SPOJNIK]") == 1 and lo3.returncode == 0
open(bad, "w", encoding="utf-8").write("Cytat.^[Herzog, *Tytuł…*, s. 133. [tłum. z przekładu angielskiego – przyp. tłum.]]\n")
lo4 = subprocess.run([sys.executable, LINT, bad], capture_output=True, text=True)
open(bad, "w", encoding="utf-8").write("Cytat.^[Herzog, *Tytuł…*, s. 133. [Tłum. z przekładu angielskiego – przyp. tłum.]]\n")
lo4c = subprocess.run([sys.executable, LINT, bad], capture_output=True, text=True)
orth = orth and lo4.stdout.count("[TLUM-ADNOTACJA]") == 1 and lo4.returncode == 0
orth = orth and lo4c.stdout.count("[TLUM-ADNOTACJA]") == 1 and lo4c.returncode == 0   # capitalised form (review 02.10.2026)
print("§ 12.2.4 c (MB 02.10.2026): withdrawn annotation flagged (WARN), also capitalised:", lo4.stdout.count("[TLUM-ADNOTACJA]") == 1 and lo4c.stdout.count("[TLUM-ADNOTACJA]") == 1)
print("§ 12.3 spelling warnings (2 + 2, surnames/pronoun/verb/sentence start silent; mimo, że flagged, chyba, że not; no ERROR):", orth)
control = control and orth
print("negative control detected:", control, "| build blocked on lint ERROR:", blocks)
if "--- ERROR ---" in lo:
    print(lo)
print("LINT 0 ERROR" if ("--- ERROR ---" not in lo and os.path.getsize(txt) > 0 and control and blocks) else "LINT FAILED")
