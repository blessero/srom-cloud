# Gates: cloud move, Cowork checkup, Code↔Cowork lines (root session, 04.10.2026)

Scope: (1) a backup and a reversible move of the Code system to a GitHub-backed cloud mirror, with MB's guide and
credit advice; (2) a checkup for Cowork, slim, sharing its sync part with Code's; (3) a Code↔Cowork channel that
survives the cloud phase, with a read-only check that measures drift.

- [ ] G1: backup archive of Code root, Cowork folder, skill links and project memory exists and lists every source file
  CHECK: sh "_cloud/verify_backup.sh"
  EXPECT: BACKUP OK
  EVIDENCE: pending

- [ ] G2: round trip on scratch copies: init, simulated cloud commit (tracked edit, new ignored data file, deletion, root CLAUDE.md, handoff entry), import back, guards (dirty module, local change after export, unimported cloud work), Cowork channel files pass through
  CHECK: python3 _cloud/test_roundtrip.py
  EXPECT: /ROUNDTRIP OK (\d+)\/\1/
  EVIDENCE: pending

- [ ] G3: cloud setup script parses, and pins the same Python packages as Cowork's tested requirements.txt
  CHECK: bash -n _cloud/setup-cloud.sh && python3 _cloud/check_pins.py
  EXPECT: PINS OK
  EVIDENCE: pending

- [ ] G4: root CLAUDE.md has the cloud rules; root hook is portable; root .claude/skills links resolve to six SKILL.md
  CHECK: grep -c '^## Cloud sessions' CLAUDE.md; grep -c 'CLAUDE_PROJECT_DIR' .claude/settings.json; for s in .claude/skills/*; do [ -f "$s/SKILL.md" ] && echo ok; done | wc -l | tr -d ' '
  EXPECT: /^1\n1\n6$/
  EVIDENCE: pending

- [ ] G5: cowork_sync.py is read-only and, on today's state, names the Cowork patches Code applied but nobody ticked, the 02:54 patches Code still has to apply, the one that does not fit Code, and the SYS ID collision (the 20:39 reset of Cowork's copy was repaired there by 21:22, so it no longer shows)
  CHECK: ~/.venvs/srom/bin/python _handoffs/tools/cowork_sync.py; echo "exit $?"
  EXPECT: /0426_srom-produkcja\.patch: in Code, in Cowork; not ticked[\s\S]*0254_srom-produkcja\.patch: not in Code: Code to apply[\s\S]*0254_srom-tlumacz\.patch: not in Code, does not apply[\s\S]*SYS-6 open in Code only[^\n]*Cowork used SYS-6[\s\S]*exit 1/
  EVIDENCE: pending

- [ ] G6: Code→Cowork channel: code-to-cowork.md K1 (setup, regression, ID rule, checkup) and README rules; root CLAUDE.md start-of-session reads cowork-to-code.md; committed in _handoffs
  CHECK: grep -c '^## K1 ' _handoffs/code-to-cowork.md; grep -c 'cowork-to-code.md' _handoffs/README.md CLAUDE.md | tr '\n' ' '; git -C _handoffs status --short | wc -l | tr -d ' '
  EXPECT: /^1\n.*README.md:[1-9].*CLAUDE.md:[1-9].*\n0$/
  EVIDENCE: pending

- [ ] G7: MB-decisions has the new SYS questions with table rows, Next free right; mb_view renders
  CHECK: ~/.venvs/srom/bin/python _handoffs/tools/mb_view.py --all < /dev/null >/dev/null && echo RENDER_OK; grep -c -E '^\| SYS-(9|10) ' _handoffs/MB-decisions.md; grep -c -E '^### SYS-(9|10) ' _handoffs/MB-decisions.md; grep -o 'Next free: SYS-[0-9]*' _handoffs/MB-decisions.md
  EXPECT: /RENDER_OK\n2\n2\nNext free: SYS-11/
  EVIDENCE: pending

- [ ] G8: Cowork checkup procedure exists; Code's checkup runs the sync check too
  CHECK: test -s _handoffs/checkup/COWORK.md && echo has; grep -c cowork_sync _handoffs/checkup/SKILL.md _handoffs/checkup/COWORK.md
  EXPECT: /has\n.*SKILL.md:[1-9]\n.*COWORK.md:[1-9]/
  EVIDENCE: pending

- [ ] G9: the real local mirror exists with the three histories, clean, nothing pushed (no remote until MB says so)
  CHECK: M="../srom-cloud"; git -C "$M" status --short | wc -l | tr -d ' '; git -C "$M" remote | wc -l | tr -d ' '; git -C "$M" log --oneline -- srom-produkcja | wc -l | tr -d ' '
  EXPECT: /^0\n0\n(1[1-9][0-9]|[2-9][0-9][0-9])$/
  EVIDENCE: pending

- [ ] G10: MB's guide _cloud/README.md: credit answer with sources, steps (claim, GitHub, environment: network list, variables, setup script), first cloud prompt, bring back, spending advice, Cowork paste-prompt
  EVIDENCE: pending

- [ ] G11: report numbers re-measured at report time
  EVIDENCE: pending
