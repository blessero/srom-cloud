#!/bin/sh
# Link the SROM InDesign scripts into InDesign's Scripts Panel (idempotent; InDesign may be closed).
#   tools/install_scripts.sh                 the two general scripts (style setup, final pass)
#   tools/install_scripts.sh <build dir>     also that article's scripts: <stem>_postimport/_ibidem/_gwiazdki.jsx,
#                                            in their own panel folder "srom_<stem>" (several texts never mix)
# Everything is a symlink, so a rebuild or a repo update is picked up without copying again.
# InDesign reads the folder on launch and refreshes it while open; running a script needs InDesign open.
set -e
cd "$(dirname "$0")/.."
REPO=$(pwd)
IND="$REPO/.claude/skills/srom-produkcja/indesign"
APP=$(ls -d "/Applications/Adobe InDesign "*/ 2>/dev/null | sort | tail -1)
[ -n "$APP" ] || { echo "InDesign not found in /Applications"; exit 1; }
NAME=$(basename "$APP")
VER=$(defaults read "${APP}${NAME}.app/Contents/Info" CFBundleShortVersionString | cut -d. -f1)
BASE="$HOME/Library/Preferences/Adobe InDesign/Version $VER.0"
LOC=$(ls -d "$BASE"/*/Scripts 2>/dev/null | head -1)
[ -n "$LOC" ] || { echo "no Scripts folder under $BASE (start InDesign once)"; exit 1; }
PANEL="$LOC/Scripts Panel"
mkdir -p "$PANEL"

link() { # link <target> <dir>
  dst="$2/$(basename "$1")"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    mkdir -p "$LOC/replaced"; mv "$dst" "$LOC/replaced/$(basename "$1").$(date +%Y%m%d%H%M)"
    echo "moved the old copy of $(basename "$1") to $LOC/replaced/"
  fi
  ln -sfn "$1" "$dst"; echo "linked $dst"
}

link "$IND/srom_style_setup.jsx" "$PANEL"
link "$IND/srom_final_pass.jsx" "$PANEL"

if [ -n "$1" ]; then
  B=$(cd "$1" && pwd)
  n=0
  for f in "$B"/*_postimport.jsx; do
    [ -f "$f" ] || { echo "no *_postimport.jsx in $B (build first)"; exit 1; }
    stem=$(basename "$f" _postimport.jsx)
    D="$PANEL/srom_$stem"; mkdir -p "$D"
    for k in postimport ibidem gwiazdki; do [ -f "$B/${stem}_$k.jsx" ] && { link "$B/${stem}_$k.jsx" "$D"; n=$((n+1)); }; done
  done
  echo "article scripts: $n"
fi
if pgrep -x "$NAME" >/dev/null; then echo "InDesign is open: the panel refreshes by itself"; else echo "InDesign is closed: the scripts appear at the next launch"; fi
