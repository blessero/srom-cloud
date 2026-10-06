#!/usr/bin/env python3
"""check_pins.py: the Python packages pinned in setup-cloud.sh equal the Mac venv's (~/.venvs/srom) and, when its
folder is on this Mac, Cowork's requirements.txt. Prints PINS OK, or each mismatch (exit 1)."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.realpath(__file__))
COWORK = "/Users/michalbartosz/ARBEIT/Bima/SROM/Cowork/srom-cowork/plugin/srom/requirements.txt"
VENV = os.path.expanduser("~/.venvs/srom/bin/python")

cloud = dict(re.findall(r"\b(python-docx|lxml|PyMuPDF|pikepdf)==([\d.]+)", open(os.path.join(HERE, "setup-cloud.sh")).read()))
sources = {}
if os.path.exists(VENV):
    out = subprocess.run([VENV, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True).stdout
    sources["Mac venv"] = {k: v for k, v in (l.split("==") for l in out.splitlines() if "==" in l)}
if os.path.exists(COWORK):
    sources["Cowork requirements.txt"] = dict(re.findall(r"^([\w-]+)==([\d.]+)", open(COWORK).read(), re.M))
bad = []
for name, pins in sources.items():
    low = {k.lower(): v for k, v in pins.items()}
    for pkg, ver in cloud.items():
        if low.get(pkg.lower()) != ver:
            bad.append(f"{pkg}: setup-cloud.sh {ver}, {name} {low.get(pkg.lower())}")
if len(cloud) != 4 or not sources:
    bad.append(f"expected 4 pins and at least one source, found {cloud} / {list(sources)}")
print("PINS OK (" + ", ".join(f"{k} {v}" for k, v in cloud.items()) + "; vs " + ", ".join(sources) + ")"
      if not bad else "PINS DIFFER\n  " + "\n  ".join(bad))
sys.exit(1 if bad else 0)
