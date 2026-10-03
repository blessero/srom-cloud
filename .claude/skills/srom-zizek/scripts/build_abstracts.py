#!/usr/bin/env python3
"""Build context/srom-abstracts.tsv from MB's compendium (deterministic, no LLM).

Source: _sources/Studia_Romologica_Kompendium*.md  (vols 1-18, one uniform entry per item).
Kept: articles, materials and reviews/opinions. Dropped as noise: events, conferences' reports, publication
lists, obituaries, memorial notes (see NOISE). Columns: vol, year, theme, part, kind (article|review), authors,
title_pl, title_en, pages, keywords, abstract_pl, abstract_en.
Zizek greps this file; it is too big to load whole. Re-run after the compendium changes.

Usage: python3 "$Z/build_abstracts.py" [<zizek-workspace>]   (default: the current folder, i.e. run it from
       workspace/srom-zizek; it reads <root>/_sources/ and writes <root>/context/srom-abstracts.tsv)
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SRC = next((ROOT / "_sources").glob("Studia_Romologica_Kompendium*.md"))
OUT = ROOT / "context" / "srom-abstracts.tsv"
COLS = ["vol", "year", "theme", "part", "kind", "authors", "title_pl", "title_en", "pages", "keywords", "abstract_pl", "abstract_en"]
EVENT_PART = re.compile(r"Informacje|Wydarzenia|Wspomnienia|nekrolog|Nekrolog", re.I)
REVIEW_PART = re.compile(r"Recenzj|Opinie", re.I)
NOISE = re.compile(r"nekrolog|wspomnienie|pożegnanie|in memoriam|\(\d{4}\s*[–-]\s*\d{4}\)|wydawnictwa|publikacje o tematyce|"
                   r"sprawozdanie|konferencj|kongres|sympozjum|wystawa|jubileusz|gratulacj|list do redakcji|^o autorach|noty o", re.I)
ENTRY = re.compile(r"^- \*\*(.+?)\*\* — (.*)$")
FIELD = re.compile(r"^\s+- \*\*(Słowa kluczowe \((?:PL|EN)\)|Abstrakt \((?:PL|EN)\)):\*\*\s*(.*)$")


def split_titles(s):
    pages = ""
    m = re.search(r"\(s\.\s*([^)]*)\)\s*$", s)
    if m:
        pages, s = m.group(1), s[:m.start()].strip()
    parts = re.findall(r"\*([^*]+)\*", s)
    pl = parts[0].strip() if parts else s.strip()
    en = parts[1].strip() if len(parts) > 1 else ""
    return pl, en, pages


def words(s):
    return {w for w in re.findall(r"\w{4,}", s.lower())}


def fill_from_recovered(kept):
    """_sources/spis-recovered.tsv = abstracts of vols 1-13 from MB's older 'Spis total' table (the compendium
    lacks most article abstracts for vols 2-11). Fills only empty abstract_pl, matched by volume + title words."""
    f = ROOT / "_sources" / "spis-recovered.tsv"
    if not f.exists():
        return
    rec = list(csv.DictReader(open(f, encoding="utf-8"), delimiter="\t"))
    for r in kept:
        if r["abstract_pl"]:
            continue
        a = words(r["title_pl"])
        best, score = None, 0
        for x in rec:
            if int(x["vol"]) != r["vol"] or not x["abstract_pl"]:
                continue
            b = words(x["title_pl"])
            s = len(a & b) / max(1, len(a | b))
            if s > score:
                best, score = x, s
        if best and score >= 0.5:
            r["abstract_pl"] = best["abstract_pl"]


def fill_from_supplements(kept):
    """_sources/vol*.md = MB's extracts (keywords/abstracts) for vols 2-11, 14. Formats vary slightly, so parse by field
    labels; match to rows by volume + title words; fill only empty keywords / abstracts."""
    for f in sorted((ROOT / "_sources").glob("vol*.md")):
        vol, cur, items = 0, None, []
        for line in f.read_text(encoding="utf-8").splitlines():
            if (m := re.search(r"(?:Tom|nr)\s+(\d+)\s*/\s*\d{4}", line)) and re.match(r"\s*#", line):
                vol = int(m.group(1))
            elif re.match(r"^\s*(#+\s*)?\d+\.\s", line) and not re.search(r"\*\*(Tytuł|Strony|Słowa|Keywords|Abstrakt)", line):
                cur = dict(vol=vol, title="", kw_pl="", kw_en="", ab_pl="", ab_en="")
                items.append(cur)
            elif cur and (m := re.search(r"\*\*(Tytuł|Słowa kluczowe \(PL\)|Słowa kluczowe \(EN\)|Keywords \(EN\)|Abstrakt \(PL\)|Abstrakt \(EN\)):?\*\*:?\s*(.*)", line)):
                k, v = m.group(1), m.group(2).strip()
                key = {"Tytuł": "title", "Słowa kluczowe (PL)": "kw_pl", "Słowa kluczowe (EN)": "kw_en", "Keywords (EN)": "kw_en",
                       "Abstrakt (PL)": "ab_pl", "Abstrakt (EN)": "ab_en"}[k]
                cur[key] = v
        for it in items:
            a = words(it["title"])
            best, score = None, 0
            for r in kept:
                if r["vol"] != it["vol"]:
                    continue
                b = words(r["title_pl"])
                s = len(a & b) / max(1, len(a | b))
                if s > score:
                    best, score = r, s
            if best and score >= 0.5:
                if not best["keywords"] and it["kw_pl"]:
                    best["keywords"] = it["kw_pl"] + (" || " + it["kw_en"] if it["kw_en"] else "")
                if not best["abstract_pl"] and it["ab_pl"]:
                    best["abstract_pl"] = it["ab_pl"]
                if not best["abstract_en"] and it["ab_en"]:
                    best["abstract_en"] = it["ab_en"]


def main():
    rows, vol, year, theme, part = [], 0, 0, "", ""
    cur = None
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if (m := re.match(r"^## Tom (\d+)/(\d{4})", line)):
            vol, year, theme, part, cur = int(m.group(1)), int(m.group(2)), "", "", None
        elif (m := re.match(r"^\*\*Temat przewodni:\*\*\s*\*?(.*?)\*?\s*$", line)) and vol:
            theme = m.group(1)
        elif line.startswith("## Uwagi"):
            vol = 0
        elif (m := re.match(r"^### (.*)", line)):
            part, cur = m.group(1).strip(), None
        elif vol and (m := ENTRY.match(line)):
            pl, en, pages = split_titles(m.group(2))
            cur = dict(vol=vol, year=year, theme=theme, part=part, authors=m.group(1), title_pl=pl, title_en=en,
                       pages=pages, keywords=[], abstract_pl="", abstract_en="")
            rows.append(cur)
        elif cur and (m := FIELD.match(line)):
            k, v = m.groups()
            if k.startswith("Słowa"):
                cur["keywords"].append(v.strip())
            elif k == "Abstrakt (PL)":
                cur["abstract_pl"] = v.strip()
            else:
                cur["abstract_en"] = v.strip()
    kept, dropped = [], 0
    for r in rows:
        is_review = bool(REVIEW_PART.search(r["part"]))
        event_only = bool(EVENT_PART.search(r["part"])) and not is_review
        if event_only or NOISE.search(r["title_pl"] + " " + r["title_en"]):
            dropped += 1
            continue
        r["kind"] = "review" if is_review else "article"
        r["keywords"] = " || ".join(k for k in r["keywords"] if k)
        kept.append(r)
    fill_from_recovered(kept)
    fill_from_supplements(kept)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, COLS, delimiter="\t")
        w.writeheader()
        w.writerows(kept)
    for v in sorted({r["vol"] for r in kept}):
        rs = [r for r in kept if r["vol"] == v]
        print(f"vol {v:2d}: {sum(r['kind'] == 'article' for r in rs):2d} articles, {sum(r['kind'] == 'review' for r in rs):2d} reviews | "
              f"abstract {sum(bool(r['abstract_pl']) for r in rs):2d}/{len(rs)} | keywords {sum(bool(r['keywords']) for r in rs):2d}/{len(rs)}")
    print(f"parsed {len(rows)}, kept {len(kept)}, dropped {dropped} as events/obituaries/lists -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
