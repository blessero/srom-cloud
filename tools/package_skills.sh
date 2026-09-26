#!/bin/sh
# Package the skills for upload to claude.ai: dist/<skill>.skill (a zip with the skill folder at its root).
# Usage: sh tools/package_skills.sh [skill ...]   (default: every skill in .claude/skills)
set -e
cd "$(dirname "$0")/.."
mkdir -p dist
skills="$*"
[ -n "$skills" ] || skills=$(ls .claude/skills)
for s in $skills; do
  [ -f ".claude/skills/$s/SKILL.md" ] || { echo "no skill: $s"; exit 1; }
  out="dist/$s.skill"
  rm -f "$out"
  (cd .claude/skills && zip -qr "../../$out" "$s" -x '*/.DS_Store' '*/__pycache__/*' '*.pyc' '*/node_modules/*')
  echo "written $out"
done
