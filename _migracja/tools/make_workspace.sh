# Builds build/srom-cowork/workspace from the live Code folders (copy only; the sources are never written), then the
# Cowork files: CLAUDE.md (src/), the ledger patched for Cowork, STATUS.md (src/STATUS_head.md + hand-off log).
set -e
R="/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans"
M=$(cd "$(dirname "$0")/.." && pwd)
W="$M/build/srom-cowork/workspace"
rm -rf "$W"; mkdir -p "$W/srom-produkcja" "$W/srom-tlumacz"
J="--exclude=__pycache__ --exclude=.DS_Store --exclude=*.pyc"
rsync -a $J "$R/srom-produkcja/volumes/" "$W/srom-produkcja/volumes/"
rsync -a $J --exclude=wordcheck.py --exclude=source_imprints.py --exclude=build_inject "$R/srom-produkcja/work/" "$W/srom-produkcja/work/"
rsync -a $J --exclude='/*/build' "$R/srom-tlumacz/work/" "$W/srom-tlumacz/work/"
rsync -a $J --exclude=/SROM_knowledge_base.md "$R/srom-tlumacz/sources/" "$W/srom-tlumacz/sources/"
rsync -a $J "$R/srom-tlumacz/training/" "$W/srom-tlumacz/training/"
rsync -a $J "$R/srom-tlumacz/tlumacz-1.3.2/" "$W/srom-tlumacz/tlumacz-1.3.2/"
cp "$R/_handoffs/MB-decisions.md" "$W/MB-decisions.md"
python3 "$M/tools/ledger_cowork.py" "$W/MB-decisions.md"
cp "$M/src/CLAUDE.md" "$W/CLAUDE.md"
python3 "$M/tools/make_status.py"
echo "WORKSPACE BUILT $(find "$W" -type f | wc -l | tr -d ' ') files, $(du -sh "$W" | cut -f1)"
