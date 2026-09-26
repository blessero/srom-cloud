#!/usr/bin/env python3
"""
make_style_setup.py — renders indesign/srom_style_setup.jsx from indesign/style_spec.json and checks that
config/styles.json names only styles the spec defines.   python3 make_style_setup.py
"""
import argparse, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = json.load(open(os.path.join(ROOT, "indesign", "style_spec.json"), encoding="utf-8"))
tpl = open(os.path.join(ROOT, "indesign", "srom_style_setup.jsx.tpl"), encoding="utf-8").read()
_ap = argparse.ArgumentParser()
_ap.add_argument("--out-dir", help="write the JSX and the style sheet here (default: into the skill itself)")
_a, _ = _ap.parse_known_args()
out = os.path.join(_a.out_dir or os.path.join(ROOT, "indesign"), "srom_style_setup.jsx")
open(out, "w", encoding="utf-8").write(tpl.replace("/*SPEC*/", json.dumps(spec, ensure_ascii=True)))
SHEET = os.path.join(_a.out_dir or os.path.join(ROOT, "references"), "style-sheet.md")


PROPS_PL = {"appliedFont": "krój", "fontStyle": "odmiana", "pointSize": "stopień", "leading": "interlinia",
            "firstLineIndent": "wcięcie 1. wiersza", "leftIndent": "wcięcie lewe", "spaceBefore": "odstęp przed",
            "spaceAfter": "odstęp po", "justification": "wyrównanie", "capitalization": "wersaliki", "hyphenation": "dzielenie",
            "tracking": "światło", "keepWithNext": "z następnym (wiersze)", "gridAlignment": "siatka", "dropCapCharacters": "inicjał (znaki)",
            "dropCapLines": "inicjał (wiersze)", "bulletChar": "punktor", "sameParaStyleSpacing": "odstęp w obrębie stylu", "appliedLanguage": "język"}
SKIP = {"hyphenateAfterFirst", "hyphenateBeforeLast", "hyphenateWordsLongerThan", "hyphenateLadderLimit", "hyphenateCapitalizedWords"}


def fmt(props):
    out = []
    for k, v in props.items():
        if k in SKIP:
            continue
        if k == "bulletChar":
            v = chr(v)
        if isinstance(v, bool):
            v = "tak" if v else "nie"
        out.append(f"{PROPS_PL.get(k, k)} {v}")
    return "; ".join(out) or "—"


def style_sheet(sp):
    L = ["# SROM — arkusz stylów (house style v2)", "",
         "Generated from `indesign/style_spec.json` by `scripts/make_style_setup.py`; do not edit by hand. Values in pt; only what",
         "differs from the parent style is listed (inheritance does the rest). " + sp["_about"], "",
         f"**Podstawa** (root of every text style): {fmt(sp['base']['props'])}.", "",
         "GREP styles in Podstawa (inherited by all text styles) — character style *Bez podziału*:", ""]
    L += [f"- `{g['expr']}` — {g['note']}" for g in sp["base"]["grep"]]
    for g in sp["groups"]:
        L += ["", f"## {g['name']}", "", "| styl | na bazie | wartości (różnice) | zastępuje | uwagi |", "|---|---|---|---|---|"]
        for st in g["styles"]:
            L.append(f"| **{st['name']}** | {st.get('basedOn', '(bez zmian)')} | {fmt(st['props']) if not g.get('keep_as_is') else 'bez zmian'} | "
                     f"{', '.join(st.get('old', [])) or '—'} | {st.get('note', '')} |")
    L += ["", "## Style znakowe", "", "| styl | wartości | zastępuje | uwagi |", "|---|---|---|---|"]
    L += [f"| **{c['name']}** | {fmt(c['props'])} | {', '.join(c.get('old', [])) or '—'} | {c.get('note', '')} |" for c in sp["character"]]
    L += ["", f"Bez zmian (przypisy): {', '.join(sp['char_keep'])}.", "",
          "## Usuwane (pozostałości importów z Worda) → zastępowane stylem " + sp["leftovers"]["replace_with"], "",
          ", ".join(sp["leftovers"]["names"]) + "; znakowe: " + ", ".join(sp["char_leftovers"]) + "."]
    return "\n".join(L) + "\n"


def para_names(sp):
    return [sp["base"]["name"]] + [s["name"] for g in sp["groups"] for s in g["styles"]]


if __name__ == "__main__":
    cfg = json.load(open(os.path.join(ROOT, "config", "styles.json"), encoding="utf-8"))
    pn, cn = set(para_names(spec)), {c["name"] for c in spec["character"]}
    bad = [v for k, v in cfg["paragraph"].items() if not k.startswith("_") and v not in pn]
    bad += [v for k, v in cfg["character"].items() if not k.startswith("_") and v not in cn]
    open(SHEET, "w", encoding="utf-8").write(style_sheet(spec))
    print(f"written {out} + {SHEET}")
    print("SPEC OK" if not bad else f"SPEC FAIL: config names not in the spec: {bad}")
    sys.exit(1 if bad else 0)
