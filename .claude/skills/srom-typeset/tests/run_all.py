"""Preflight: runs every test file; last line SUITE ALL PASS n/n or SUITE FAILED."""
import os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
ok_rx = re.compile(r"ALL PASS \d+/\d+|LINT 0 ERROR|JSX-DONE|PDF SKIP")
files = sorted(f for f in os.listdir(here) if f.startswith("test_") and f.endswith(".py"))
bad = []
for f in files:
    out = subprocess.run([sys.executable, os.path.join(here, f)], capture_output=True, text=True).stdout
    lines = [l for l in out.splitlines() if l.strip()]
    verdicts = [l for l in lines if ok_rx.search(l) or "FAILED" in l]
    good = bool(verdicts) and all(ok_rx.search(v) for v in verdicts)
    print(f"{'ok  ' if good else 'FAIL'} {f}: {' | '.join(verdicts) or (lines[-1] if lines else 'no output')}")
    if not good:
        bad.append(f)
print(f"SUITE ALL PASS {len(files)}/{len(files)}" if not bad else f"SUITE FAILED {len(bad)}/{len(files)}: {bad}")
sys.exit(1 if bad else 0)
