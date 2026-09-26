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
# build must fail on lint ERROR: '"' survives normalisation only if normalise was skipped; op. cit. in a literal note
md = os.path.join(out, "opcit.md")
open(md, "w", encoding="utf-8").write("Tekst[^1].\n\n[^1]: Kowalski, op. cit., s. 5.\n")
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), md, "--out", out], capture_output=True, text=True)
rep = open(os.path.join(out, "opcit_report.md"), encoding="utf-8").read()
blocks = r.returncode == 1 and "kanon linter:" in rep
print("negative control detected:", control, "| build blocked on lint ERROR:", blocks)
if "--- ERROR ---" in lo:
    print(lo)
print("LINT 0 ERROR" if ("--- ERROR ---" not in lo and os.path.getsize(txt) > 0 and control and blocks) else "LINT FAILED")
