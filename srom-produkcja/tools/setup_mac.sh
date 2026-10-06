#!/bin/sh
# One-time setup of the editor's Mac (idempotent). Needs Homebrew, pandoc >= 3.1 and node.
#   - Python 3.13 venv ~/.venvs/srom with python-docx, lxml, PyMuPDF, pikepdf (system python3 is too old;
#     pikepdf: cover_page.py's text-layer repair, 06.10.2026)
#   - acorn in ~/.venvs/srom/node for the strict ES3 check of the InDesign scripts
#   - the repo's skills symlinked into ~/.claude/skills, so they load in every Claude Code project
# LibreOffice is optional (only tests/test_pdf.py uses it; without it that test reports SKIP).
set -e
cd "$(dirname "$0")/.."
REPO=$(pwd)
command -v pandoc >/dev/null || { echo "pandoc missing: brew install pandoc"; exit 1; }
[ -x /opt/homebrew/bin/python3.13 ] || brew install python@3.13
[ -x "$HOME/.venvs/srom/bin/python" ] || /opt/homebrew/bin/python3.13 -m venv "$HOME/.venvs/srom"
"$HOME/.venvs/srom/bin/pip" install -q python-docx lxml pymupdf pikepdf
[ -d "$HOME/.venvs/srom/node/node_modules/acorn" ] || npm install --silent --prefix "$HOME/.venvs/srom/node" acorn
mkdir -p "$HOME/.claude/skills"
for s in .claude/skills/*/; do
  s=$(basename "$s"); dst="$HOME/.claude/skills/$s"
  if [ -L "$dst" ]; then ln -sfn "$REPO/.claude/skills/$s" "$dst"
  elif [ -e "$dst" ]; then echo "SKIP $dst exists and is not a symlink — move it away first"
  else ln -s "$REPO/.claude/skills/$s" "$dst"; fi
done
"$HOME/.venvs/srom/bin/python" .claude/skills/srom-produkcja/tests/run_all.py | tail -1
