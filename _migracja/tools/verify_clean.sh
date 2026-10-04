# Clean-room run of the bundle: Python 3.10 venv built only from requirements.txt, empty HOME, minimal PATH,
# LANG=C.UTF-8, bundle copied (or unzipped) to a path with spaces. Modes: suite tlumacz paths examples.
#   sh tools/verify_clean.sh [--from-zip] mode...
set -u
M=$(pwd)
SP=/private/tmp/claude-501/-Users-michalbartosz-ARBEIT-Bima-SROM-CODE-SROM-SROM-edit-and-trans/6ed649f8-2c3f-4244-8ea7-29cbf76cc9e0/scratchpad
VENV=$SP/venv310
if [ ! -x "$VENV/bin/python" ] || [ "$M/build/srom-cowork/plugin/srom/requirements.txt" -nt "$VENV/.req" ]; then
  rm -rf "$VENV"; "$SP/py310/bin/python" -m venv "$VENV" && "$VENV/bin/pip" install -q -r "$M/build/srom-cowork/plugin/srom/requirements.txt" && touch "$VENV/.req" || { echo "VENV FAILED"; exit 1; }
fi
T=$(cd "$(mktemp -d)" && pwd -P)/"Cowork test dir"; mkdir -p "$T" "$T/../home"
if [ "${1:-}" = "--from-zip" ]; then
  shift; Z=$(ls -t "$M"/srom-cowork-*.zip | head -1); (cd "$T" && unzip -q "$Z") || { echo "UNZIP FAILED"; exit 1; }
  echo "from zip: $(basename "$Z")"
else
  cp -R "$M/build/srom-cowork" "$T/"
fi
B="$T/srom-cowork"; P="$B/plugin/srom/skills"; W="$B/workspace"
PANDOC_DIR=$(dirname "$(command -v pandoc)"); NODE_DIR=$(dirname "$(command -v node)")
run() { (cd "$1" && shift && env -i HOME="$T/../home" LANG=C.UTF-8 PATH="$VENV/bin:$PANDOC_DIR:$NODE_DIR:/usr/bin:/bin" "$@"); }
for mode in "$@"; do
  case $mode in
  suite)
    run "$W" python "$P/srom-produkcja/tests/run_all.py" | grep -E "^FAIL|SUITE" ;;
  tlumacz)
    ok=0; S="$P/srom-tlumacz/scripts"
    o=$(run "$W" python "$S/tlumacz-check_tb.py" --schema --shape --vocab --precedent --evidence 2>&1) && ok=$((ok+1)) || echo "FAIL check_tb: $(echo "$o" | tail -3)"
    o=$(run "$W" python "$S/tlumacz-check_tb.py" --selftest 2>&1); echo "$o" | grep -qE "selftest: ([0-9]+)/\1 " && ok=$((ok+1)) || echo "FAIL selftest: $(echo "$o" | tail -2)"
    o=$(run "$W" python "$S/tlumacz-test_handoff.py" 2>&1); echo "$o" | grep -qE "^HANDOFF CONTRACT ([0-9]+)/\1$" && ok=$((ok+1)) || echo "FAIL handoff: $(echo "$o" | grep -E 'FAIL|CONTRACT' | tail -4)"
    o=$(run "$W/srom-tlumacz/work" python "$S/tlumacz-draft_check.py" --all 2>&1); n=$(echo "$o" | grep -c "^DRAFT .*: leftover 0, marks \([0-9]*\)=\1"); t=$(echo "$o" | grep -c "^DRAFT ")
    [ "$n" -gt 0 ] && [ "$n" = "$t" ] && ok=$((ok+1)) || echo "FAIL draft_check ($n/$t): $(echo "$o" | tail -4)"
    echo "TLUMACZ PREFLIGHT OK $ok/4" ;;
  paths)
    ok=0
    a=$(run "$W/srom-tlumacz/work" python "$P/srom-tlumacz/scripts/tlumacz_paths.py" srom-produkcja); [ "$a" = "$P/srom-produkcja" ] && ok=$((ok+1)) || echo "FAIL skill_dir: $a"
    a=$(run "$W" python "$P/srom-tlumacz/scripts/tlumacz_paths.py" --module); [ "$a" = "$W/srom-tlumacz" ] && ok=$((ok+1)) || echo "FAIL module: $a"
    a=$(run "$W" python -c "import sys; sys.path.insert(0, '$P/srom-produkcja/scripts'); import kanon_path; print(kanon_path.find_kanon())"); [ "$a" = "$P/srom-kanon" ] && ok=$((ok+1)) || echo "FAIL kanon: $a"
    echo "PATHS OK $ok/3" ;;
  examples)
    run "$B" python "$M/tools/check_examples.py" --run "$B" ;;
  esac
done
rm -rf "$(dirname "$T")"
