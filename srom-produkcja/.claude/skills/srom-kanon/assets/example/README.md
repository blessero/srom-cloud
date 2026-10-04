# Example: the Kanon linter on a paragraph of a translation draft

Input: one paragraph of the vol. 19 Pahulich draft translation (`srom-tlumacz/work/pahulich/pahulich_pl.md`, the paragraph on Thomas Browne and Pushkin), which quotes a Russian title in Cyrillic.

Expected: no ERROR, one WARN `[CYRILLIC]` (Kanon § 9.6: Cyrillic in the body is given in Polish transcription, in the apparatus in ALA-LC) — a WARN is a judgment call to read, not an automatic fix; then the year and century form counts for the reader to interpret by zone (RULES.md § J). Exit code 0 (only ERRORs give 1).

Command (run in this folder, `python3` with `srom-produkcja/requirements.txt` installed):

`python3 ../../scripts/lint_srom.py input/pahulich_akapit.md > expected/lint.txt; echo "exit $?" >> expected/lint.txt`

Produced by the command: expected/lint.txt
