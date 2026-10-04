"""Builds <skill>/assets/example/ for the four SROM skills from short real excerpts of the workspace, and produces the
expected output by running the shipped tools (with the SROM venv). Each README carries the command and the list of
produced files that tools/check_examples.py re-runs and compares."""
import json, os, re, shutil, subprocess, sys

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(M, "build/srom-cowork/plugin/srom/skills")
WS = os.path.join(M, "build/srom-cowork/workspace")
PY = os.path.expanduser("~/.venvs/srom/bin/python")


def excerpt(src, out, idx, nohead=False):
    r = subprocess.run([sys.executable, os.path.join(M, "tools/excerpt.py")] + (["--no-head"] if nohead else []) +
                       [src, out] + [str(i) for i in idx], capture_output=True, text=True, check=True)
    return set(r.stdout.split())


def refs_subset(files, keys, out):
    refs = [r for f in files for r in json.load(open(f, encoding="utf-8"))]
    json.dump([r for r in refs if r["id"] in keys], open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def fresh(skill):
    d = os.path.join(SK, skill, "assets", "example")
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d + "/input"); os.makedirs(d + "/expected")
    return d


def readme(d, title, body, command, produced):
    open(os.path.join(d, "README.md"), "w", encoding="utf-8").write(
        f"# Example: {title}\n\n{body}\n\n"
        f"Command (run in this folder, `python3` with the bundle's requirements):\n\n`{command}`\n\n"
        f"Produced by the command: {', '.join(produced)}\n")
    subprocess.run(["sh", "-c", command.replace("python3 ", PY + " ")], cwd=d, check=False)
    for p in produced:  # no machine path in the shipped expected output
        f = os.path.join(d, p)
        if os.path.exists(f) and not f.endswith(".docx"):
            t = open(f, encoding="utf-8").read()
            for r in sorted({SK, os.path.realpath(SK)}, key=len, reverse=True): t = t.replace(r + "/", "<skills>/")
            open(f, "w", encoding="utf-8").write(t)


# ---------------------------------------------------------------- srom-produkcja: INJECT build of a real passage
d = fresh("srom-produkcja")
W = os.path.join(WS, "srom-produkcja/work/ostendorf")
keys = excerpt(f"{W}/pl/ostendorf_pl.md", f"{d}/input/ostendorf_pl_wycinek.md", [9, 15, 18])
refs_subset([f"{W}/refs.json", f"{W}/pl/ostendorf_refs_tlum.json"], keys, f"{d}/input/refs.json")
cmd = "python3 ../../scripts/build.py input/ostendorf_pl_wycinek.md --refs input/refs.json --out expected"
stems = ["ostendorf_pl_wycinek" + s for s in (".txt", "_report.md", "_pytania.md", "_pytania.csv", "_citations.json",
                                               "_postimport.jsx", "_ibidem.jsx", "_gwiazdki.jsx", "_doi.jsx", ".docx")]
readme(d, "INJECT build (stage 3) of a translated passage",
       "Input: three paragraphs of the vol. 19 Ostendorf translation (`srom-produkcja/work/ostendorf/pl/ostendorf_pl.md`, the "
       "take-back of the delivered draft: paragraphs \"Aby to pokazać…\", \"Rasa nie wyłoniła się…\", \"Choć transatlantyckie…\"), "
       "with its translator front matter and title note, and the refs.json entries those paragraphs cite (16 works).\n\n"
       "Expected: `build.py` prints `PASS`; the DOCX carries only named styles, real footnotes with first citations and short "
       "forms from the CSL, the title note as an asterisk note at the end, a Polish bibliography; the report "
       "(`_report.md`), the query sheet (`_pytania.md/.csv`), the bibliography for Crossref (`_citations.json`) and the "
       "InDesign scripts. `.txt` is the DOCX's text, the readable view of what InDesign will receive.",
       cmd, ["expected/" + s for s in stems])

# ---------------------------------------------------------------- srom-tlumacz: source paragraphs -> translation
d = fresh("srom-tlumacz")
TW = os.path.join(WS, "srom-tlumacz/work/ndiaye")
k1 = excerpt(f"{TW}/src/ndiaye_src.md", f"{d}/input/ndiaye_src_wycinek.md", [1, 2, 6], nohead=True)
k2 = excerpt(f"{TW}/ndiaye_pl.md", f"{d}/expected/ndiaye_pl_wycinek.md", [3, 4, 8], nohead=True)
refs_subset([f"{TW}/src/refs.json"], k1 | k2, f"{d}/input/refs.json")
cmd = ("python3 ../../../srom-produkcja/scripts/check.py --pair input/ndiaye_src_wycinek.md expected/ndiaye_pl_wycinek.md "
       "--refs input/refs.json > expected/check_pair.txt")
readme(d, "TRANS (stage 2): frozen English source → Polish SROM-MD",
       "Input: the opening of Noémie Ndiaye, \"Black Roma\" (*Renaissance Quarterly* 75, 2022) as srom-produkcja froze it "
       "(`srom-tlumacz/work/ndiaye/src/ndiaye_src.md`: the heading, the first paragraph with notes 1–3, the block "
       "quotation with note 4), and the refs.json entries cited.\n\n"
       "Expected: `ndiaye_pl_wycinek.md`, the same passage in the vol. 19 draft translation (`ndiaye_pl.md`, before MB's "
       "Word edit): paragraph for paragraph, citation tokens and note markers unchanged, the block quotation kept as "
       "a block. The translation itself is the model's work and is not reproduced by a command; "
       "the command is the hand-off check that every translation must pass (`CHECK OK`: same paragraphs, headings, note "
       "markers and citation keys as the source).",
       cmd, ["expected/check_pair.txt"])

# ---------------------------------------------------------------- srom-kanon: the linter on a real paragraph
d = fresh("srom-kanon")
L = open(f"{WS}/srom-tlumacz/work/pahulich/pahulich_pl.md", encoding="utf-8").read().split("\n")
par = [l for l in L if "Цыганка" in l]
assert len(par) == 1
open(f"{d}/input/pahulich_akapit.md", "w", encoding="utf-8").write(par[0] + "\n")
cmd = "python3 ../../scripts/lint_srom.py input/pahulich_akapit.md > expected/lint.txt; echo \"exit $?\" >> expected/lint.txt"
readme(d, "the Kanon linter on a paragraph of a translation draft",
       "Input: one paragraph of the vol. 19 Pahulich draft translation (`srom-tlumacz/work/pahulich/pahulich_pl.md`, the "
       "paragraph on Thomas Browne and Pushkin), which quotes a Russian title in Cyrillic.\n\n"
       "Expected: no ERROR, one WARN `[CYRILLIC]` (Kanon § 9.6: Cyrillic in the body is given in Polish transcription, in "
       "the apparatus in ALA-LC) — a WARN is a judgment call to read, not an automatic fix; then the year and century "
       "form counts for the reader to interpret by zone (RULES.md § J). Exit code 0 (only ERRORs give 1).",
       cmd, ["expected/lint.txt"])

# ---------------------------------------------------------------- srom-quant: pre-deposit check of the master CSV
d = fresh("srom-quant")
rows = open(f"{WS}/srom-produkcja/volumes/18/srom_master_v3.csv", encoding="utf-8-sig").read().split("\n")
open(f"{d}/input/srom_master_v3_wycinek.csv", "w", encoding="utf-8-sig").write("\n".join(rows[:3]) + "\n")
cmd = ("python3 ../../scripts/validate_master.py input/srom_master_v3_wycinek.csv > expected/validate.txt; "
       "echo \"exit $?\" >> expected/validate.txt")
readme(d, "pre-deposit check of the master CSV",
       "Input: the header and the first two rows (Ostendorf, Fotta) of the vol. 18 master CSV "
       "(`srom-produkcja/volumes/18/srom_master_v3.csv`) as it stands before any Crossref deposit.\n\n"
       "Expected: blocking errors for what is still missing before a deposit — the placeholder DOI prefix `10.XXXXX` and "
       "the online publication date `2025-12-TODO` — and exit code 1; warnings that both translated articles have no "
       "`translators_struct` yet (a real gap of the vol. 18 CSV). With the Crossref prefix, `mint_suffixes.py` and the "
       "real date clear the errors (SKILL.md, deployment sequence).",
       cmd, ["expected/validate.txt"])
print("EXAMPLES WRITTEN")
