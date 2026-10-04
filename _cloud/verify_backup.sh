# verify_backup.sh [archive]: checks the newest (or the given) backup made by backup.sh against its manifest:
# the sha256 of the archive, and every path listed in the manifest present in the archive. Prints BACKUP OK.
set -e
D=/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/_backup
A=${1:-$(ls -t "$D"/srom-*.tar.gz | head -1)}
M="${A%.tar.gz}.manifest"
[ -f "$A" ] && [ -f "$M" ] || { echo "BACKUP MISSING: $A"; exit 1; }
(cd "$D" && shasum -a 256 -c "$(basename "${A%.tar.gz}").sha256" >/dev/null) || { echo "BACKUP SHA256 MISMATCH"; exit 1; }
missing=$(python3 - "$A" "$M" <<'PY'
import sys, tarfile, unicodedata as u
n = lambda s: u.normalize("NFC", s.rstrip("/"))
have = {n(m.name) for m in tarfile.open(sys.argv[1])}
want = {n(l.rstrip("\n")) for l in open(sys.argv[2], encoding="utf-8")}
gone = sorted(want - have); print(len(gone)); [print("  " + g, file=sys.stderr) for g in gone[:10]]
PY
)
n=$(wc -l < "$M" | tr -d ' ')
[ "$missing" = 0 ] && echo "BACKUP OK $(basename "$A"): $n paths, sha256 verified, $(du -h "$A" | cut -f1)" \
  || { echo "BACKUP INCOMPLETE: $missing of $n paths missing"; exit 1; }
