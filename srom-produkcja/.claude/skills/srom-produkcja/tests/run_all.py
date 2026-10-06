"""Preflight: runs every test file; last line SUITE ALL PASS n/n or SUITE FAILED."""
import os, re, subprocess, sys
# the editor's Mac: system python3 is too old / lacks python-docx -> re-run in the SROM venv if there is one
VENV = os.path.expanduser("~/.venvs/srom/bin/python")
def _usable():
    try:
        import docx, fitz, lxml, pikepdf  # noqa: F401
    except ImportError:
        return False
    return sys.version_info >= (3, 10)
if not _usable() and os.path.exists(VENV) and os.path.realpath(sys.executable) != os.path.realpath(VENV):
    os.execv(VENV, [VENV] + sys.argv)
here = os.path.dirname(os.path.abspath(__file__))
ok_rx = re.compile(r"ALL PASS \d+/\d+|LINT 0 ERROR|JSX-DONE|PDF SKIP")
files = sorted(f for f in os.listdir(here) if f.startswith("test_") and f.endswith(".py"))
bad = []
for f in files:
    r = subprocess.run([sys.executable, os.path.join(here, f)], capture_output=True, text=True)
    out = r.stdout
    lines = [l for l in out.splitlines() if l.strip()]
    verdicts = [l for l in lines if ok_rx.search(l) or "FAILED" in l]
    if r.returncode:                       # a crash after an early verdict must not pass
        verdicts.append(f"FAILED exit {r.returncode}: " + (r.stderr.strip().splitlines() or ["?"])[-1][:200])
    good = bool(verdicts) and all(ok_rx.search(v) for v in verdicts)
    print(f"{'ok  ' if good else 'FAIL'} {f}: {' | '.join(verdicts) or (lines[-1] if lines else 'no output')}")
    if not good:
        bad.append(f)
print(f"SUITE ALL PASS {len(files)}/{len(files)}" if not bad else f"SUITE FAILED {len(bad)}/{len(files)}: {bad}")
sys.exit(1 if bad else 0)
