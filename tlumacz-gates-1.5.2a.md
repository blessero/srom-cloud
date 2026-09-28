# Gates: 1.5.2a Pilot article intake — Ndiaye, "Black Roma" (T12)

Scope: receive the source, answer T11 (front matter both ways), survey what the article needs (quotation rules, Polish editions, terminology, group names), and put the blocking questions to MB. The draft is leaf 1.5.2b.

- [x] G1: the four source files in `work/ndiaye/src/` are identical to srom-typeset's
  CHECK: cd "../srom-typeset/work/ndiaye" && shasum -a 256 -c "../../../srom-tlumacz/work/ndiaye/src/manifest.sha256" | grep -c ': OK$'
  EXPECT: /^4$/m
  EVIDENCE: 4

- [x] G2: T11 tested on this side (front-matter cases in the contract test)
  CHECK: python3 tlumacz-test_handoff.py
  EXPECT: /^HANDOFF CONTRACT (\d+)\/\1$/m
  EVIDENCE: GAP CLOSED ok  E4: numbers from added citation keys not reported | HANDOFF CONTRACT 23/23

- [x] G3: the Polish header data for Ndiaye is well formed
  CHECK: python3 tlumacz-front_check.py work/ndiaye/src/ndiaye_src_front.md work/ndiaye/ndiaye_front_pl.md
  EXPECT: /^FRONT OK$/m
  EVIDENCE: FRONT OK

- [x] G4: intake file covers procedure features, Polish editions, terminology, plan, questions
  CHECK: grep -c '^## [1-5]\. ' work/ndiaye/ndiaye_intake.md
  EXPECT: /^5$/m
  EVIDENCE: 5

- [x] G5: blocking questions put to MB in one item
  CHECK: grep -c '^## D11 ' ../_handoffs/MB-decisions.md
  EXPECT: /^1$/m
  EVIDENCE: 1

- [x] G6: receipt and front-matter format sent to srom-typeset
  CHECK: grep -c -E '^## E14 |^- T12 — 28.09.2026 status: received' ../_handoffs/tlumacz-to-typeset.md
  EXPECT: /^2$/m
  EVIDENCE: 2

- [x] G7: every Polish-edition claim in the intake is backed by a catalogue or text check (manual)
  EVIDENCE: BN data.bn.org.pl queries 28.09.2026: PIW 1988 Molier volume "Skąpiec ; Pan de Pourceaugnac ; … ; Szelmostwa Skapena" (matched also by title "Chory z urojenia" + author Żeleński); "Małżeństwo z musu" (PIW 1988), "Wartogłów" (PIW 1988), "Mieszczanin szlachcicem"; "Pomniejsze uczucia" (Hong, Zano, Tajfuny 2024); "Historia szaleństwa w dobie klasycyzmu" (PIW 1987); "Wielki łańcuch bytu" (1999, 2009); "Nowele przykładne" (1913, 1949); Patterson only in English. Text: `research/boy_skapen.txt` source line "Molier, Dzieła, tom szósty … Warszawa 1922"; „Cyganie” l. 1947, 3940; „naszyjnik” l. 4381. Convention: ISAP WDU19520020009. Unconfirmed items are labelled "to confirm" in the intake (story title in Nowele 1976; PIW 1988 series title; Phormio, Aethiopica).
