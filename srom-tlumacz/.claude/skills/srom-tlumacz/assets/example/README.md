# Example: TRANS (stage 2): frozen English source → Polish SROM-MD

Input: the opening of Noémie Ndiaye, "Black Roma" (*Renaissance Quarterly* 75, 2022) as srom-produkcja froze it (`srom-tlumacz/work/ndiaye/src/ndiaye_src.md`: the heading, the first paragraph with notes 1–3, the block quotation with note 4), and the refs.json entries cited.

Expected: `ndiaye_pl_wycinek.md`, the same passage in the vol. 19 draft translation (`ndiaye_pl.md`, before MB's Word edit): paragraph for paragraph, citation tokens and note markers unchanged, the block quotation kept as a block. The translation itself is the model's work and is not reproduced by a command; the command is the hand-off check that every translation must pass (`CHECK OK`: same paragraphs, headings, note markers and citation keys as the source).

Command (run in this folder; `P` = the Python of SKILL.md, `T` = this skill's `scripts/`):

`P=python3; T=../../scripts; $P "$($P $T/tlumacz_paths.py srom-produkcja)/scripts/check.py" --pair input/ndiaye_src_wycinek.md expected/ndiaye_pl_wycinek.md --refs input/refs.json > expected/check_pair.txt`

Produced by the command: expected/check_pair.txt
