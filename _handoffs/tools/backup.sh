# backup.sh: one archive of everything the SROM system needs to come back as it is now, made before any big step.
# Into /Users/michalbartosz/ARBEIT/Bima/SROM/CODE/_backup/:
#   srom-<yyyymmdd-HHMM>.tar.gz   the one folder SROM/Redakcja (Code's repository with .git, Cowork's workspace, MB's
#                                 folders; not "4. Archive"), Code's old Zizek folder, the ~/.claude/skills/srom-* links,
#                                 this project's Claude memory
#   .manifest (every path archived), .sha256 (of the archive). Check it with verify_backup.sh.
# Restore one part: tar -xzf <archive> -C / <path as listed in the manifest, without the leading />
set -e
D=/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/_backup; mkdir -p "$D"
N="srom-$(date +%Y%m%d-%H%M)"
set -- "Users/michalbartosz/ARBEIT/Bima/SROM/Redakcja" \
       "Users/michalbartosz/ARBEIT/Bima/SROM/CODE/Zizek"
for m in /Users/michalbartosz/.claude/projects/-Users-michalbartosz-ARBEIT-Bima-SROM-Redakcja-SROM-edit-and-trans*/memory; do
  [ -d "$m" ] && set -- "$@" "${m#/}"
done
for s in /Users/michalbartosz/.claude/skills/srom-*; do set -- "$@" "${s#/}"; done
X="Users/michalbartosz/ARBEIT/Bima/SROM/Redakcja/4. Archive"
(cd / && find "$@" -path "$X" -prune -o \( -type f -o -type l -o -type d \) ! -name .DS_Store -print | sort) > "$D/$N.manifest"
(cd / && tar -czf "$D/$N.tar.gz" --exclude .DS_Store --exclude "$X" "$@")
(cd "$D" && shasum -a 256 "$N.tar.gz" > "$N.sha256")
echo "$D/$N.tar.gz"
