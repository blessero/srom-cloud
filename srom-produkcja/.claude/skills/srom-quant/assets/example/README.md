# Example: pre-deposit check of the master CSV

Input: the header and the first two rows (Ostendorf, Fotta) of the vol. 18 master CSV (`srom-produkcja/volumes/18/srom_master_v3.csv`) as it stands before any Crossref deposit.

Expected: blocking errors for what is still missing before a deposit — the placeholder DOI prefix `10.XXXXX` and the online publication date `2025-12-TODO` — and exit code 1; warnings that both translated articles have no `translators_struct` yet (a real gap of the vol. 18 CSV). With the Crossref prefix, `mint_suffixes.py` and the real date clear the errors (SKILL.md, deployment sequence).

Command (run in this folder, `python3` with `srom-produkcja/requirements.txt` installed):

`python3 ../../scripts/validate_master.py input/srom_master_v3_wycinek.csv > expected/validate.txt; echo "exit $?" >> expected/validate.txt`

Produced by the command: expected/validate.txt
