# Gates: 1.4.2a Shared draft checker (replaces the per-article copies)

Opened 29.09.2026 14:16 [general]. From leaf 1.3.2 findings L1: four copies of the same checks (`ndiaye/leftover_en.py`,
`ostendorf/ost_check.py`, `pahulich/pah_check.py`, `tittel/tit_check.py`) have drifted (word lists 11 vs 16,
case-sensitive vs not, title-note block checked or skipped; Tittel's docstring names the wrong gates; Tittel's
quotes sheet is never checked). One tool: `tlumacz-draft_check.py <id>`. The old copies stay (closed gates cite
them); new articles use the shared tool. Drafts are read, never written.

Checks (strictest of the variants): leftover English in body paragraphs *and* the title-note block (16 function words,
case-insensitive; italics, comments, citation tokens removed); `DO SPRAWDZENIA: S<n>` in `<id>_pl.md` = `- S<n>` lines
in `<id>_uwagi.md`; quotes sheet (if present): classes valid (PLAN OUT-QUOTES), every detected quotation's note has a
row, every open row names an S-item that exists in text and notes sheet (PLAN OUT-QUOTES: "every open row has exactly
one comment in pl.md and one open line in the notes sheet").

- [x] G1: the shared checker runs on all four drafts
  CHECK: python3 tlumacz-draft_check.py --all | grep -c '^DRAFT '
  EXPECT: /^4$/m

- [x] G2: on the real drafts it agrees with the old copies: leftover 0 everywhere; marks 7/2/10/12; Ostendorf quotes 43/43
  CHECK: python3 tlumacz-draft_check.py --all | grep -E '^DRAFT '
  EXPECT: /^DRAFT ndiaye: leftover 0, marks 7=7, quotes –\nDRAFT ostendorf: leftover 0, marks 2=2, quotes 43\/43 .*\nDRAFT pahulich: leftover 0, marks 10=10, quotes –\nDRAFT tittel: leftover 0, marks 12=12, quotes .*$/m

- [x] G3: negative controls on temporary copies: English sentence in the body, English in the title-note block, an
  S-mark missing from the notes sheet, a quotes row removed, a bad class, an open row naming a missing S-item
  CHECK: python3 tlumacz-draft_check.py --selftest | tail -1
  EXPECT: /^selftest: 6\/6 negative controls caught$/m

- [x] G4: PLAN contract lists the tool; HANDOVER tells new articles to use it
  CHECK: grep -c 'tlumacz-draft_check.py' tlumacz-PLAN.md HANDOVER.md
  EXPECT: /tlumacz-PLAN.md:[1-9]\nHANDOVER.md:[1-9]/m

- [x] G5: committed
  CHECK: git log -1 --format=%s
  EXPECT: /1\.4\.2a/
