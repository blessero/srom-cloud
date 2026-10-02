# Gates: 1.4.1 srom-tlumacz as a skill (SKILL.md, references, scripts)

Opened 03.10.2026 00:49 [general], at MB's request ("package srom-tlumacz into a complete, coherent and lean skill").
Deliverable: `.claude/skills/srom-tlumacz/` in this repository, linked as `~/.claude/skills/srom-tlumacz`. The skill holds
the procedure and the stable assets (termbase and its schema, decision log, race register, per-article file formats)
and the four tested scripts; the module folder keeps only state (HANDOVER, PLAN, gates, `work/`, `sources/`, `training/`,
closed leaf folders). Nothing is copied: each file has one home. Leaves 1.4.2 (tb_lookup, tb_check, calque_lint) and 1.4.3
(review sheet) are decided here on measured grounds (lean rule), not built by default.

Measured before the move (03.10.2026 00:45, venv): check_tb 0 problems, selftest 9/9; HANDOFF CONTRACT 34/34;
draft_check --all: ndiaye 0, 7=7, –; ostendorf 0, 2=2, 43/43; pahulich 0, 10=10, –; tittel 0, 12=12, 34/34; selftest 6/6.
Prototype termbase check (scratchpad, HOUSE + PROVISIONAL rows, Polish stems) on the four drafts: 4 flags, all false
(Ndiaye "itinerant pilgrimage", Tittel "belonging to", "lifelong enslavement", Pahulich anti-Roma 31/32), 0 real misses.

Moved paths (closed gates of earlier leaves cite the old ones; they are not reopened): `tlumacz-check_tb.py`,
`tlumacz-draft_check.py`, `tlumacz-front_check.py`, `tlumacz-test_handoff.py`, `tlumacz_paths.py` → `K/scripts/`;
`tlumacz-tb.tsv`, `tlumacz-tb-schema.md`, `tlumacz-decisions.md`, `tlumacz-rasa.md` → `K/references/`
(`K` = `.claude/skills/srom-tlumacz`). Deleted (git keeps them): `work/ndiaye/leftover_en.py`, `work/ostendorf/ost_check.py`,
`work/pahulich/pah_check.py`, `work/tittel/tit_check.py` (gates 1.5.2b–1.5.5b G4/G5: the same checks are
`tlumacz-draft_check.py <id>`, which agreed with them in 1.4.2a), `kanon-12-2-przeklady-PROJEKT.md` (adopted as Kanon
§ 12.2), the root copy of the Dom DOCX (byte-identical to `sources/vol18-en/`). The PLAN's per-article outputs section
moved to `K/references/outputs.md`. Handoff test: the E5 case (terminology slot) removed, 34 → 33 cases.

P=~/.venvs/srom/bin/python, T=~/.claude/skills/srom-tlumacz/scripts (in every CHECK below).

- [x] G1: the skill is installed, resolves into this repository, and its front matter is valid (name, description ≤ 1024 characters)
  CHECK: [ "$(cd ~/.claude/skills/srom-tlumacz && pwd -P)" = "$(pwd -P)/.claude/skills/srom-tlumacz" ] && ~/.venvs/srom/bin/python -c "import re;t=open('.claude/skills/srom-tlumacz/SKILL.md',encoding='utf-8').read();m=re.match(r'---\nname: (\S+)\ndescription: (.+?)\n---\n',t,re.S);print('FRONTMATTER OK' if m and m.group(1)=='srom-tlumacz' and len(m.group(2))<=1024 else 'FRONTMATTER BAD')"
  EXPECT: FRONTMATTER OK
  EVIDENCE: FRONTMATTER OK

- [x] G2: every `references/…` and `scripts/…` path named in SKILL.md and the references exists — in this skill, or in srom-kanon / srom-produkcja for the files the text says are theirs (Kanon, kartoteka, handoff.md, srom-md.md)
  CHECK: ~/.venvs/srom/bin/python -c "import re,glob,os;K='.claude/skills/srom-tlumacz';H=os.path.expanduser('~/.claude/skills/');fs=[K+'/SKILL.md']+glob.glob(K+'/references/*.md');ps={p for f in fs for p in re.findall(r'\b((?:references|scripts)/[\w.-]+)',open(f,encoding='utf-8').read())};bad=[p for p in ps if not any(os.path.exists(os.path.join(d,p)) for d in (K,H+'srom-kanon',H+'srom-produkcja'))];own=sum(os.path.exists(os.path.join(K,p)) for p in ps);print(f'PATHS OK {len(ps)} ({own} in this skill)' if ps and not bad else f'MISSING {bad}')"
  EXPECT: /^PATHS OK \d+ \(\d+ in this skill\)$/m
  EVIDENCE: PATHS OK 14 (10 in this skill)

- [x] G3: the termbase checks pass from the skill (all checks, then the negative controls)
  CHECK: P=~/.venvs/srom/bin/python; T=~/.claude/skills/srom-tlumacz/scripts; $P $T/tlumacz-check_tb.py --schema --shape --vocab --precedent --evidence >/dev/null && $P $T/tlumacz-check_tb.py --selftest | tail -1
  EXPECT: selftest: 9/9 negative controls caught
  EVIDENCE: selftest: 9/9 negative controls caught

- [x] G4: the handoff contract test passes from the skill
  CHECK: ~/.venvs/srom/bin/python ~/.claude/skills/srom-tlumacz/scripts/tlumacz-test_handoff.py | tail -1
  EXPECT: /^HANDOFF CONTRACT (\d+)\/\1$/m
  EVIDENCE: HANDOFF CONTRACT 33/33

- [x] G5: the draft checker gives the same verdicts as before the move, and its negative controls still fail
  CHECK: P=~/.venvs/srom/bin/python; T=~/.claude/skills/srom-tlumacz/scripts; $P $T/tlumacz-draft_check.py --all; $P $T/tlumacz-draft_check.py --selftest | tail -1
  EXPECT: /^DRAFT ndiaye: leftover 0, marks 7=7, quotes –\nDRAFT ostendorf: leftover 0, marks 2=2, quotes 43\/43 \(0 bad class, 0 open rows unmatched\)\nDRAFT pahulich: leftover 0, marks 10=10, quotes –\nDRAFT tittel: leftover 0, marks 12=12, quotes 34\/34 \(0 bad class, 0 open rows unmatched\)\nselftest: 6\/6 negative controls caught$/m
  EVIDENCE: DRAFT tittel: leftover 0, marks 12=12, quotes 34/34 (0 bad class, 0 open rows unmatched) | selftest: 6/6 negative controls caught

- [x] G6: the scripts find the module's data from any working directory (called through the ~/.claude/skills link)
  CHECK: P=~/.venvs/srom/bin/python; T=~/.claude/skills/srom-tlumacz/scripts; cd "$(mktemp -d)" && $P $T/tlumacz-draft_check.py --all | grep -c '^DRAFT ' && $P $T/tlumacz-check_tb.py --schema --shape --vocab --precedent --evidence >/dev/null && echo TB-OK
  EXPECT: /^4\nTB-OK$/m
  EVIDENCE: 4 | TB-OK

- [x] G7: no parallel copies or dead files left at the module root or in `work/` (old script and asset paths, per-article checker copies, the superseded Kanon draft, the duplicate Dom DOCX)
  CHECK: ls tlumacz-*.py tlumacz_paths.py tlumacz-tb.tsv tlumacz-tb-schema.md tlumacz-rasa.md tlumacz-decisions.md kanon-12-2-przeklady-PROJEKT.md "Dom_Communities Stripped Mac copy.docx" work/*/leftover_en.py work/*/*_check.py 2>/dev/null | wc -l | tr -d ' '
  EXPECT: /^0$/m
  EVIDENCE: 0

- [x] G8: the commands in CLAUDE.md § Checks run as written and pass
  CHECK: ~/.venvs/srom/bin/python -c "import re,subprocess,os;t=open('CLAUDE.md',encoding='utf-8').read().split('## Checks',1)[1].split('\n## ',1)[0];cs=[l.strip() for l in t.splitlines() if l.startswith('    ~/')];ok=sum(subprocess.run(os.path.expanduser(c),shell=True,capture_output=True).returncode==0 for c in cs);print(f'CLAUDE CHECKS {ok}/{len(cs)} ok')"
  EXPECT: /CLAUDE CHECKS ([1-9]\d*)\/\1 ok/
  EVIDENCE: CLAUDE CHECKS 4/4 ok

- [x] G9: SKILL.md stays lean (≤ 160 lines; the Kanon is cited by §, not restated)
  CHECK: awk 'END{print (NR<=160)?"LEAN "NR:"LONG "NR}' .claude/skills/srom-tlumacz/SKILL.md
  EXPECT: /^LEAN \d+$/m
  EVIDENCE: LEAN 133

- [x] G10: the live documents call the scripts from the skill, never from the old root paths (PLAN status-log lines are history and exempt)
  CHECK: grep -nE '(python3?|/python) +tlumacz-' CLAUDE.md HANDOVER.md tlumacz-PLAN.md | grep -vE ':- [0-9]{2}\.[0-9]{2}\.2026' | wc -l | tr -d ' '
  EXPECT: /^0$/m
  EVIDENCE: 0

- [x] G11: leaves 1.4.2 and 1.4.3 are decided in the PLAN tree with their measured grounds
  CHECK: grep -cE '^ +- 1\.4\.(2|3) .*not built' tlumacz-PLAN.md
  EXPECT: /^2$/m
  EVIDENCE: 2

- [x] G12: srom-produkcja is told (new paths; no tb_check) in a committed E-item
  CHECK: echo "items $(grep -cE '^## E[0-9]+ — \[general\] srom-tlumacz is a skill' ../_handoffs/tlumacz-to-produkcja.md) uncommitted $(git -C ../_handoffs status --porcelain tlumacz-to-produkcja.md | wc -l | tr -d ' ')"
  EXPECT: items 1 uncommitted 0
  EVIDENCE: items 1 uncommitted 0

- [x] G13: walk-through — every step actually run on the four texts (intake and draft gates 1.5.2–1.5.5, the hand-back) has its place in SKILL.md, and every live ruling of HANDOVER § 3 sits in the skill, the termbase schema or the Kanon (manual)
  EVIDENCE: 03.10.2026 01:05. Gates 1.5.2a–1.5.5b mapped: src hashes, intake coverage, one quotes row per quotation, catalogue-backed claims → SKILL § The procedure (intake gates) and step 1; pair, front, build (Errors none + translator), leftover English, S-marks, Word round trip in a temp dir → step 3 (run as written on Ostendorf: CHECK OK, FRONT OK, build exit 0 / Errors none, DRAFT 0, 2=2, 43/43, round trip CHECK OK); re-read and HOUSE-term counts → step 4; MB items and E-items (1.5.2a G5–G6) → step 5; hand-back T26/T30 → step 6 and `references/outputs.md` § Back. HANDOVER § 3 (old text): scope + PL→EN keywords → Hard rules; vol. 18 precedent, LOCK, tie-break, floor, exclusions as queries → Terminology + schema; editing separate, translation-time §§ → step 1 (now with § 0, § 12.3) + Hard rules; neologisms → Terminology; § 12.2 rulings → Kanon § 12.2, § 7.1 (all adopted); kartoteka → step 1; Word master → intro; 27.09 rulings: urasowienie, gypsylorists → termbase C-0001, C-0005 + decision log; places per case → step 1; pronouns → step 1; error mapping diagnostic → step 4 + PLAN 1.3.4. HANDOVER § 8 facts: official names, *mniejszość etniczna* → step 1; urasowienie, subalterni → termbase rows. One gap found and closed: the intake gates were not named in SKILL.md (added).

- [x] G14: committed
  CHECK: git log --format=%s | grep -cE '^1\.4\.1: gates ALL MET'
  EXPECT: /^[1-9][0-9]*$/m
  EVIDENCE: 1
