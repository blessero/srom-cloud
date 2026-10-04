#!/bin/bash
# setup-cloud.sh: the SROM toolchain in a Claude Code cloud environment (Ubuntu 24.04, runs as root before Claude
# starts). Paste this whole file into the environment's "Setup script" box (claude.ai/code → environment settings).
# Kept under about five minutes so the environment is cached. Pins = the Mac venv (~/.venvs/srom) and Cowork's
# requirements.txt (check_pins.py keeps them equal). The first session checks the result: run_all.py → SUITE ALL PASS.
set -u
log() { echo "[srom-setup] $*"; }

# Python packages, the same versions as on the Mac and in Cowork
python3 -m pip install -q --break-system-packages python-docx==1.2.0 lxml==6.1.3 PyMuPDF==1.28.2 fonttools \
  || python3 -m pip install -q python-docx==1.2.0 lxml==6.1.3 PyMuPDF==1.28.2 fonttools
log "python $(python3 --version 2>&1 | cut -d' ' -f2): python-docx, lxml, PyMuPDF installed"

# pandoc: GitHub release downloads of other repositories are blocked in cloud sessions, so it comes from PyPI
# (pypandoc_binary 1.17 = pandoc 3.9; the Mac has 3.8.3); Ubuntu's own 3.1.3 only as a last resort
if python3 -m pip install -q --break-system-packages pypandoc_binary==1.17 2>/dev/null \
   || python3 -m pip install -q pypandoc_binary==1.17; then
  P=$(python3 -c 'import os, pypandoc; print(os.path.join(os.path.dirname(pypandoc.__file__), "files", "pandoc"))')
  [ -x "$P" ] && ln -sf "$P" /usr/local/bin/pandoc
fi
command -v pandoc >/dev/null || { apt-get update -qq && apt-get install -y -qq pandoc >/dev/null; }
log "$(pandoc --version | head -1)"

# LibreOffice (test_pdf.py makes its test PDFs with it) and the Polish locale data
(apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
  libreoffice-writer-nogui fonts-dejavu >/dev/null) && log "$(soffice --version 2>/dev/null | head -1)" \
  || log "LibreOffice: not installed (test_pdf.py will say so)"

# acorn: the strict ES3 test of the InDesign scripts
npm install -g --silent acorn >/dev/null 2>&1 && log "acorn: ok" || log "acorn: not installed (weaker parser used)"

# IBM Plex Sans for srom-quant's cover_page.py: Code's version looks in ~/Library/Fonts, Cowork's in
# ~/.local/share/fonts; the two TTFs go to both (npm ships WOFF only: converted with fonttools)
t=$(mktemp -d)
if (cd "$t" && npm pack --silent @ibm/plex-sans >/dev/null 2>&1 && tar xzf ibm-plex-sans-*.tgz); then
  for d in "$HOME/Library/Fonts" "$HOME/.local/share/fonts"; do
    mkdir -p "$d"
    python3 - "$t" "$d" <<'PY'
import os, sys
from fontTools.ttLib import TTFont
for n in ("Regular", "Italic"):
    f = TTFont(os.path.join(sys.argv[1], f"package/fonts/complete/woff/IBMPlexSans-{n}.woff")); f.flavor = None
    f.save(os.path.join(sys.argv[2], f"IBMPlexSans-{n}.ttf"))
PY
  done
  log "IBM Plex Sans: $(ls "$HOME/Library/Fonts" | tr '\n' ' ')"
else
  log "IBM Plex Sans: not installed (cover_page.py will stop with 'not found')"
fi
rm -rf "$t"
exit 0
