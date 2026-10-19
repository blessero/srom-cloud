#!/usr/bin/env python3
"""
split_volume.py — one PDF per article, cut from an archive volume PDF by the master CSV's page ranges
(back catalogue, C19, MB 19.10.2026: the old volumes cannot be re-exported from InDesign).

    python3 split_volume.py <master CSV> <volume.pdf> --out <dir> [--offset N] [--only <article_id> …]
        → <dir>/<article_id>.pdf for every row, then: cover_page.py <CSV> <article_id> <dir>/<article_id>.pdf --out …

Printed page → PDF page: `--offset N` (PDF index = printed page + N, 0-based), else found from the folios: the
first line of a page that is or starts with a number, or the last one that is or ends with one, is its printed page; the offset is the one most pages agree
on (at least 5 pages and 80 % of the folios read, or the run stops). A row's range must lie inside the volume.

The pages are copied as they are (pikepdf): content, fonts and text layer unchanged. A volume's structure tree
(tags) does not follow the pages into the new file; /Lang (else `language`, else pl) and DisplayDocTitle are set.
Last line: RESULT: <n> article(s) written · offset <N> (<from folios k/m | given>).
"""
import argparse, csv, os, re, sys
from collections import Counter

import pikepdf
import pymupdf


def find_offset(path):
    d = pymupdf.open(path)
    votes, read = Counter(), 0
    for i, page in enumerate(d):
        lines = [l.strip() for l in page.get_text().splitlines() if l.strip()]
        if not lines:
            continue
        for cand, rx in ((lines[0], r"(\d{1,4})(?:\s.*)?"), (lines[-1], r"(?:.*\s)?(\d{1,4})")):
            m = re.fullmatch(rx, cand) if len(cand) < 90 else None   # a folio alone, or opening / closing the running head
            if m:
                votes[i - int(m.group(1))] += 1
                read += 1
                break
    if not votes:
        sys.exit("ABORT: no folios found; give --offset")
    off, n = votes.most_common(1)[0]
    if n < 5 or n < 0.8 * read:
        sys.exit(f"ABORT: folios disagree (best offset {off}: {n} of {read} pages); give --offset")
    return off, f"from folios {n}/{read}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master"); ap.add_argument("volume_pdf"); ap.add_argument("--out", required=True)
    ap.add_argument("--offset", type=int); ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.master, encoding="utf-8-sig")))
    if a.only:
        rows = [r for r in rows if r["article_id"] in a.only]
    off, how = (a.offset, "given") if a.offset is not None else find_offset(a.volume_pdf)
    src = pikepdf.open(a.volume_pdf)
    os.makedirs(a.out, exist_ok=True)
    done = 0
    for r in rows:
        try:
            pf, pt = int(r["pages_from"]), int(r["pages_to"])
        except (ValueError, KeyError):
            sys.exit(f"ABORT: {r.get('article_id')}: pages_from/pages_to not numbers")
        i0, i1 = pf + off, pt + off
        if i0 < 0 or i1 >= len(src.pages) or i0 > i1:
            sys.exit(f"ABORT: {r['article_id']}: pages {pf}–{pt} → PDF pages {i0 + 1}–{i1 + 1}, outside 1–{len(src.pages)}")
        dst = pikepdf.new()
        for i in range(i0, i1 + 1):
            dst.pages.append(src.pages[i])
        dst.Root.Lang = pikepdf.String(str(src.Root.get("/Lang", "")) or (r.get("language") or "pl"))
        dst.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
        with dst.open_metadata(set_pikepdf_as_editor=False) as m:
            m["dc:title"] = r.get("title_pl", "")
        dst.docinfo["/Title"] = r.get("title_pl", "")
        path = os.path.join(a.out, r["article_id"] + ".pdf")
        dst.save(path)
        print(f"{r['article_id']}: printed {pf}–{pt} = PDF {i0 + 1}–{i1 + 1} ({i1 - i0 + 1} pages) → {path}")
        done += 1
    print(f"RESULT: {done} article(s) written · offset {off} ({how})")


if __name__ == "__main__":
    main()
