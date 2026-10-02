#!/usr/bin/env python3
"""
make_style_setup.py — renders indesign/srom_style_setup.jsx, indesign/srom_final_pass.jsx and references/style-sheet.md from indesign/style_spec.json
and checks that config/styles.json names only styles the spec defines.   python3 make_style_setup.py [--out-dir DIR]
"""
import argparse, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = json.load(open(os.path.join(ROOT, "indesign", "style_spec.json"), encoding="utf-8"))
tpl = open(os.path.join(ROOT, "indesign", "srom_style_setup.jsx.tpl"), encoding="utf-8").read()
_ap = argparse.ArgumentParser()
_ap.add_argument("--out-dir", help="write the JSX and the style sheet here (default: into the skill itself)")
_a, _ = _ap.parse_known_args()
out = os.path.join(_a.out_dir or os.path.join(ROOT, "indesign"), "srom_style_setup.jsx")
SHEET = os.path.join(_a.out_dir or os.path.join(ROOT, "references"), "style-sheet.md")

PL = {"appliedFont": "krój", "fontStyle": "odmiana", "pointSize": "stopień", "leading": "interlinia", "tracking": "światło",
      "firstLineIndent": "wcięcie akapitowe", "leftIndent": "wcięcie z lewej", "spaceBefore": "odstęp przed", "spaceAfter": "odstęp po",
      "justification": "wyrównanie", "capitalization": "wersaliki", "hyphenation": "dzielenie", "gridAlignment": "siatka",
      "dropCapCharacters": "inicjał (znaki)", "dropCapLines": "inicjał (wiersze)", "appliedLanguage": "język", "position": "położenie",
      "composer": "składacz", "ruleBelow": "linia pod", "ruleBelowLineWeight": "grubość linii", "ruleBelowOffset": "odsunięcie linii",
      "noBreak": "bez podziału", "sameParaStyleSpacing": "odstęp między akapitami tego stylu", "desiredLetterSpacing": "odstęp liter (pożądany)"}
VALS = {"LEFT_JUSTIFIED": "justowanie", "LEFT_ALIGN": "do lewej", "RIGHT_ALIGN": "do prawej", "CENTER_ALIGN": "do środka",
        "CENTER_JUSTIFIED": "justowanie, ostatni wiersz do środka", "AWAY_FROM_BINDING_SIDE": "od grzbietu", "TO_BINDING_SIDE": "do grzbietu", "ALIGN_BASELINE": "tak",
        "NONE": "nie", "ALL_CAPS": "tak", "NORMAL": "nie", "SMALL_CAPS": "kapitaliki", "CAP_TO_SMALL_CAP": "wersaliki → kapitaliki",
        "SUPERSCRIPT": "indeks górny"}
TEKST_DETAIL = {"kerningMethod", "autoLeading", "hyphenateAfterFirst", "hyphenateBeforeLast", "hyphenateCapitalizedWords",
                "hyphenateLadderLimit", "hyphenateWordsLongerThan", "hyphenationZone", "minimumWordSpacing", "desiredWordSpacing",
                "maximumWordSpacing", "minimumLetterSpacing", "maximumLetterSpacing", "minimumGlyphScaling", "desiredGlyphScaling",
                "maximumGlyphScaling", "diacriticPosition", "leftIndent", "rightIndent", "spaceBefore", "spaceAfter"}


def num(v):
    if isinstance(v, float):
        mm = v / 72 * 25.4
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return s + (f" ({mm:.1f} mm)" if abs(v) > 2.5 and k_is_len[0] else "")
    return str(v)


k_is_len = [False]
LEN = {"firstLineIndent", "leftIndent", "spaceBefore", "spaceAfter", "ruleBelowOffset"}


def fmt(props, skip=()):
    out = []
    for k, v in props.items():
        if k in skip:
            continue
        k_is_len[0] = k in LEN
        if isinstance(v, bool):
            v = "tak" if v else "nie"
        elif isinstance(v, str):
            v = VALS.get(v, v)
        else:
            v = num(v)
        out.append(f"{PL.get(k, k)} {v}")
    return "; ".join(out) or "—"


def style_sheet(sp):
    d = sp["document"]
    L = ["# SROM — arkusz stylów (v3)", "",
         "Generated from `indesign/style_spec.json` by `scripts/make_style_setup.py`; do not edit by hand. Values in pt (mm where it",
         "helps); each style lists only what differs from the style it is based on. The values are vol. 18's own (templates 03_Ellis and",
         "09_Konferencja, read in InDesign); deliberate changes are listed under each style.", "",
         "## Dokument", "",
         f"- Siatka bazowa: co {d['grid']['baselineDivision']:.4f} pt od {d['grid']['baselineStart']:.3f} pt (22 mm) od góry strony — jak w 18 tomach.",
         f"- Przypisy (Footnote Options): styl *{d['footnotes']['footnoteTextStyle']}*; numer w tekście w indeksie górnym "
         f"({d['text']['superscriptSize']} % / {d['text']['superscriptPosition']} %); po numerze w przypisie kropka + półfiret; "
         f"{d['footnotes']['spacer']:.2f} pt nad pierwszym przypisem; linia {d['footnotes']['ruleLineWeight']} pt × "
         f"{d['footnotes']['ruleWidth'] / 72 * 25.4:.0f} mm; numeracja od nowa w każdej sekcji; "
         f"długi przypis {'może przejść' if not d['footnotes']['noSplitting'] else 'nie przechodzi'} na następną stronę.",
         f"- Kapitaliki {d['text']['smallCap']} %. [Basic Paragraph]: Cambria, polski.", ""]
    t = next(p for p in sp["paragraph"] if p["name"] == "Tekst")
    L += [f"**Tekst** (podstawa wszystkich stylów): {fmt(t['props'], TEKST_DETAIL)}.", "",
          f"Justowanie i dzielenie Tekstu (dziedziczą je wszystkie style, o ile nie zmieniają): {fmt({k: v for k, v in t['props'].items() if k in TEKST_DETAIL})}.", "",
          "Style GREP w Tekście (dziedziczone) — styl znakowy *Bez podziału*:", ""]
    L += [f"- `{g['expr']}` — {g['note']}" for g in t["grep"]]
    for g in sp["groups"]:
        title = "Na wierzchu (zestaw roboczy, od najczęstszych)" if g["name"] == "" else f"Folder „{g['name']}”"
        L += ["", f"## {title}", "", "| styl | na bazie | wartości (różnice) | zastępuje (tom 18) | uwagi |", "|---|---|---|---|---|"]
        for st in sp["paragraph"]:
            if st["group"] != g["name"] or st["name"] == "Tekst":
                continue
            extra = []
            if st.get("bullet"):
                extra.append(f"punktor „{chr(st['bullet']['char'])}” + tab")
            for tb in st.get("tabs", []):
                extra.append(f"tabulator {tb['position']:.2f} pt" + (f" z kropkami" if tb["leader"] else ""))
            for n in st.get("nested", []):
                extra.append(f"styl zagnieżdżony *{n['style']}* przez inicjał")
            for gr in st.get("grep", []):
                extra.append(f"GREP `{gr['expr']}` → *{gr['style']}*")
            olds = st.get("old", []) + [f"{k} (z linią)" for k in st.get("old_if", {})]
            note = st.get("note", "") + "".join(f" **Zmiana:** {c}." for c in st.get("changes", []))
            L.append(f"| **{st['name']}** | {st['basedOn'] or '—'} | {'; '.join([fmt(st['props'])] + extra)} | {', '.join(olds) or '—'} | {note} |")
    L += ["", "Zmiany w Tekście: " + "; ".join(t.get("changes", [])) + ".", "",
          "## Style znakowe", "", "| styl | wartości | zastępuje | uwagi |", "|---|---|---|---|"]
    L += [f"| **{c['name']}** | {fmt(c['props'])} | {', '.join(c.get('old', [])) or '—'} | {c.get('note', '')} |" for c in sp["character"]]
    L += ["", "## Porządki (skrypt)", "",
          "Skrypt usuwa **wszystkie** dotychczasowe style akapitowe i znakowe dokumentu. Tekst w starym stylu dostaje nowy według kolumny",
          f"„zastępuje”; nieznane style akapitowe → *{sp['para_fallback']}*, znakowe → brak stylu. Wbudowane [Basic Paragraph] i [None] zostają."]
    return "\n".join(L) + "\n"


def para_names(sp):
    return [s["name"] for s in sp["paragraph"]]


def validate(sp):
    errs = []
    pn, cn = para_names(sp), [c["name"] for c in sp["character"]]
    if len(set(pn)) != len(pn) or len(set(cn)) != len(cn):
        errs.append("duplicate style name")
    if set(pn) & set(cn):
        errs.append(f"one name for a paragraph and a character style (Word forbids it): {set(pn) & set(cn)}")
    seen = set()
    groups = [g["name"] for g in sp["groups"]]
    for p in sp["paragraph"]:
        if p["basedOn"] and p["basedOn"] not in seen:
            errs.append(f"{p['name']}: based on {p['basedOn']}, which is not defined before it")
        if p.get("next") and p["next"] not in pn:
            errs.append(f"{p['name']}: next style {p['next']} undefined")
        if p["group"] not in groups:
            errs.append(f"{p['name']}: unknown group {p['group']}")
        for r in p.get("grep", []) + p.get("nested", []):
            if r["style"] not in cn:
                errs.append(f"{p['name']}: GREP/nested character style {r['style']} undefined")
        seen.add(p["name"])
    fpn = spec.get("final_pass", {})
    for key in ("headings", "short_last_line", "lists", "skip_styles"):
        errs += [f"final_pass.{key}: {n} undefined" for n in fpn.get(key, []) if n not in pn]
    olds = [o for p in sp["paragraph"] for o in p.get("old", [])]
    dup = {o for o in olds if olds.count(o) > 1}
    if dup:
        errs.append(f"old style mapped twice: {dup}")
    return errs


if __name__ == "__main__":
    open(out, "w", encoding="utf-8").write(tpl.replace("/*SPEC*/", json.dumps(spec, ensure_ascii=True)))
    fp = open(os.path.join(ROOT, "indesign", "srom_final_pass.jsx.tpl"), encoding="utf-8").read()
    open(os.path.join(os.path.dirname(out), "srom_final_pass.jsx"), "w", encoding="utf-8").write(
        fp.replace("/*CONF*/", json.dumps(spec["final_pass"], ensure_ascii=True)))
    cfg = json.load(open(os.path.join(ROOT, "config", "styles.json"), encoding="utf-8"))
    pn, cn = set(para_names(spec)), {c["name"] for c in spec["character"]}
    bad = [v for k, v in cfg["paragraph"].items() if not k.startswith("_") and v not in pn]
    bad += [v for k, v in cfg["character"].items() if not k.startswith("_") and v not in cn]
    bad += [v for v in cfg.get("template_extra", {}).get("paragraph", []) if v not in pn]
    bad += [v for v in cfg.get("template_extra", {}).get("character", []) if v not in cn]
    errs = validate(spec)
    open(SHEET, "w", encoding="utf-8").write(style_sheet(spec))
    print(f"written {out} + {SHEET}")
    print("SPEC OK" if not bad and not errs else f"SPEC FAIL: config names not in the spec: {bad}; spec errors: {errs}")
    sys.exit(1 if bad or errs else 0)
