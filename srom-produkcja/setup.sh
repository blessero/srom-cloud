#!/bin/sh
# One-time setup of the SROM toolchain on plain Linux (Cowork's sandbox) or a Mac. Safe to run again.
#   sh setup.sh            install the Python packages, check pandoc (install 3.8.3 into ~/.local/bin if missing or < 3.1),
#                          install acorn for the optional ES3 test if npm is there
# Lives in srom-produkcja/ (next to requirements.txt): sh srom-produkcja/setup.sh, then
#   python3 srom-produkcja/.claude/skills/srom-produkcja/tests/run_all.py  ->  SUITE ALL PASS n/n
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
PANDOC_VERSION=3.8.3

python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
  || { echo "python3 is $(python3 --version 2>&1): the toolchain needs Python >= 3.10"; exit 1; }
python3 -m pip install -q -r "$HERE/requirements.txt" 2>/dev/null \
  || python3 -m pip install -q --user -r "$HERE/requirements.txt" 2>/dev/null \
  || python3 -m pip install -q --break-system-packages -r "$HERE/requirements.txt"
echo "python packages: ok ($(python3 --version 2>&1))"

pandoc_ok() { command -v pandoc >/dev/null 2>&1 && pandoc --version | head -1 | awk '{split($2,v,"."); exit !(v[1]>3 || (v[1]==3 && v[2]>=1))}'; }
if ! pandoc_ok; then
  case "$(uname -s)-$(uname -m)" in
    Linux-x86_64) arch=amd64 ;; Linux-aarch64|Linux-arm64) arch=arm64 ;;
    *) echo "pandoc >= 3.1 missing: install it (https://pandoc.org/installing.html)"; exit 1 ;;
  esac
  mkdir -p "$HOME/.local/bin"; t=$(mktemp -d)
  curl -fsSL "https://github.com/jgm/pandoc/releases/download/$PANDOC_VERSION/pandoc-$PANDOC_VERSION-linux-$arch.tar.gz" | tar xz -C "$t"
  cp "$t/pandoc-$PANDOC_VERSION/bin/pandoc" "$HOME/.local/bin/"; rm -rf "$t"
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo "add to PATH: export PATH=\$HOME/.local/bin:\$PATH"; export PATH="$HOME/.local/bin:$PATH" ;; esac
fi
echo "pandoc: $(pandoc --version | head -1)"

if command -v npm >/dev/null 2>&1; then
  npm install -g --silent acorn >/dev/null 2>&1 || npm install -g --silent --prefix "$HOME/.local" acorn >/dev/null 2>&1 || true
  echo "acorn: $(node -e 'try{require.resolve("acorn");console.log("ok")}catch(e){console.log("not resolvable: set NODE_PATH or ACORN (optional)")}' 2>/dev/null || echo 'node missing (optional)')"
else
  echo "node/npm: not installed (optional: the ES3 test of the InDesign scripts uses a weaker parser)"
fi

# IBM Plex Sans for srom-quant's cover_page.py (a Mac has it in ~/Library/Fonts; this step is for Linux, i.e. Cowork's VM).
# npm ships the official release as WOFF only: converted to the two TTFs the script wants, in ~/.local/share/fonts.
FD="$HOME/.local/share/fonts"
if [ "$(uname -s)" = Linux ]; then
  if [ -f "$FD/IBMPlexSans-Regular.ttf" ] && [ -f "$FD/IBMPlexSans-Italic.ttf" ]; then
    echo "IBM Plex Sans: ok"
  elif command -v npm >/dev/null 2>&1; then
    t=$(mktemp -d); mkdir -p "$FD"
    ( cd "$t" && npm pack --silent @ibm/plex-sans >/dev/null 2>&1 && tar xzf ibm-plex-sans-*.tgz \
      && python3 -m pip install -q fonttools 2>/dev/null || python3 -m pip install -q --user fonttools 2>/dev/null \
      || python3 -m pip install -q --break-system-packages fonttools
      python3 - "$FD" <<'PY'
import sys, os
from fontTools.ttLib import TTFont
for n in ("Regular", "Italic"):
    f = TTFont(f"package/fonts/complete/woff/IBMPlexSans-{n}.woff"); f.flavor = None
    f.save(os.path.join(sys.argv[1], f"IBMPlexSans-{n}.ttf"))
PY
    ) >/dev/null 2>&1; rm -rf "$t"
    [ -f "$FD/IBMPlexSans-Italic.ttf" ] && echo "IBM Plex Sans: installed in $FD" \
      || echo "IBM Plex Sans: not installed (cover_page.py needs the two .ttf files; set SROM_FONT_DIR to their folder)"
  else
    echo "IBM Plex Sans: missing and no npm (cover_page.py needs IBMPlexSans-Regular/Italic.ttf; set SROM_FONT_DIR)"
  fi
fi
