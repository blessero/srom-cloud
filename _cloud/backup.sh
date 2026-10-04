# backup.sh: one archive of everything the SROM system needs to come back as it is now, made before a cloud move
# (or any big step). Into /Users/michalbartosz/ARBEIT/Bima/SROM/CODE/_backup/:
#   srom-<yyyymmdd-HHMM>.tar.gz   the Code root (with every .git), Cowork's folder, Code's old Zizek folder,
#                                 the ~/.claude/skills/srom-* links, this project's Claude memory
#   .manifest (every path archived), .sha256 (of the archive). Check it with verify_backup.sh.
# Restore one part: tar -xzf <archive> -C / <path as listed in the manifest, without the leading />
set -e
D=/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/_backup; mkdir -p "$D"
N="srom-$(date +%Y%m%d-%H%M)"
set -- "Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM" \
       "Users/michalbartosz/ARBEIT/Bima/SROM/Cowork" \
       "Users/michalbartosz/ARBEIT/Bima/SROM/CODE/Zizek" \
       "Users/michalbartosz/.claude/projects/-Users-michalbartosz-ARBEIT-Bima-SROM-CODE-SROM-SROM-edit-and-trans/memory"
for s in /Users/michalbartosz/.claude/skills/srom-*; do set -- "$@" "${s#/}"; done
(cd / && find "$@" \( -type f -o -type l -o -type d \) ! -name .DS_Store | sort) > "$D/$N.manifest"
(cd / && tar -czf "$D/$N.tar.gz" --exclude .DS_Store "$@")
(cd "$D" && shasum -a 256 "$N.tar.gz" > "$N.sha256")
echo "$D/$N.tar.gz"
