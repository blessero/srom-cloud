#!/usr/bin/env python3
"""
pdf_enhance.py — bookmarks and live links for an online PDF that InDesign did not give them (back catalogue, C19,
MB 19.10.2026: old volumes cannot be re-exported; vol. 17 was re-exported without a TOC style).

    python3 pdf_enhance.py <in.pdf> [--out <out.pdf>] [--no-bookmarks] [--no-links] [--dry-run]

Run it on the finished file (after cover_page.py): it only adds an outline and link annotations. Page content
streams, fonts, the text layer, tags, page labels, Info and XMP are not touched; the file is saved the way
cover_page.py saves it (PyMuPDF, garbage=4, object streams). Without --out the input is replaced.

Bookmarks. Level 1: „Strona metadanych” for the cover page (when page 1 carries „Jak cytować:”), then the article's
title (the PDF title, else the first heading) on its first page. Level 2: the headings, found by type: a line set
larger than the body text (≥ 1.08 ×), or a short bold line, or one of the house section words in capitals
(WSTĘP, WPROWADZENIE, ZAKOŃCZENIE, PODSUMOWANIE, BIBLIOGRAFIA, STRESZCZENIE, SUMMARY …). Running heads (top margin),
folios, footnotes (type smaller than the body), pull quotes (»…«) and the title repeated in capitals under
STRESZCZENIE / SUMMARY are left out. An existing
outline is kept and nothing is added (InDesign's own bookmarks win).

Links. URLs (http, https, www.) and DOIs (10.NNNN/…, also as doi.org addresses) in the text get a link annotation
over the words; a URL broken over two lines gets one link on each part (a repeated hyphen at the break, the Polish
convention, is counted once). Areas already under a link are left alone. Trailing punctuation is not part of a URL.

Last line: RESULT: bookmarks <n> (<added|kept>) · links <n> added · pages <n>.
"""
import argparse, os, re, shutil, sys, tempfile
from collections import Counter

import pymupdf

SECTION_WORDS = {"WSTĘP", "WPROWADZENIE", "UWAGI WSTĘPNE", "ZAKOŃCZENIE", "PODSUMOWANIE", "WNIOSKI", "BIBLIOGRAFIA",
                 "LITERATURA", "ŹRÓDŁA", "ŹRÓDŁA PIERWOTNE", "ŹRÓDŁA ARCHIWALNE", "ŹRÓDŁA INTERNETOWE", "PUBLIKACJE",
                 "OPRACOWANIA", "STRESZCZENIE", "SUMMARY", "ABSTRACT", "ANEKS", "ZAŁĄCZNIK", "ZAŁĄCZNIKI", "PODZIĘKOWANIA"}
TOP_MARGIN = 45            # pt: running heads and folios live above this
URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>„”\"]+|(?<![\w/.])10\.\d{4,9}/[^\s<>„”\"]+", re.I)
TRAIL = ".,;:)]}»”’'!?"


def lines_of(page):
    """[(text, size, bold, bbox, words)] per line; size and bold from the line's longest span."""
    out = []
    d = page.get_text("dict", flags=pymupdf.TEXT_PRESERVE_WHITESPACE)
    for b in d["blocks"]:
        for ln in b.get("lines", []):
            spans = [s for s in ln["spans"] if s["text"].strip()]
            if not spans:
                continue
            main = max(spans, key=lambda s: len(s["text"].strip()))
            text = "".join(s["text"] for s in ln["spans"]).strip()            # a soft hyphen at the end is kept for joining
            bold = bool(main["flags"] & 16) or "Bold" in main["font"] or "Black" in main["font"]
            out.append((text, round(main["size"], 1), bold, pymupdf.Rect(ln["bbox"])))
    return out


def body_size(doc, first):
    c = Counter()
    for page in doc.pages(first):
        for text, size, bold, r in lines_of(page):
            c[size] += len(text)
    return c.most_common(1)[0][0] if c else 10.0


def is_cover(page):
    return "Jak cytować:" in page.get_text()


def headings(doc, first, body):
    """[(level, title, page index)] — level 2 headings of the article pages."""
    out = []
    for pno in range(first, len(doc)):
        page = doc[pno]
        ls = lines_of(page)
        i = 0
        while i < len(ls):
            text, size, bold, r = ls[i]
            if r.y1 <= TOP_MARGIN or re.fullmatch(r"[\divxlcIVXLC.\s–-]*", text) or size < body * 0.95:
                i += 1
                continue
            if (bold or size >= body * 1.08) and text[:1] in "»«„\"“":
                # a pull quote set large or bold: it opens with a quotation mark and the lines of the same type close it
                close = r"[«»]\W?$" if text[:1] in "»«" else r"[”\"]\W?$"       # » … «  or  „ … ”
                k = i
                while k < len(ls) - 1 and k - i < 8 and not re.search(close, ls[k][0]) \
                        and ls[k + 1][1] == size and ls[k + 1][2] == bold:
                    k += 1
                if re.search(close, ls[k][0]):
                    i = k + 1
                    continue
                if text[:1] in "»«":            # a speaker's name in a transcript („» Adam Bartosz”): not a heading
                    i += 1
                    continue
            caps = text.upper() == text and any(ch.isalpha() for ch in text)
            if caps and (text.startswith("(") or len(re.findall(r"[^\W\d_]", text)) < 4):   # „(ZOMO)28.”: an abbreviation, not a heading
                caps = False
            word = re.sub(r"[:.\s\u00ad]+$", "", text).upper() in SECTION_WORDS
            big = size >= body * 1.08
            goes_on = i + 1 < len(ls) and ls[i + 1][1] == size and ls[i + 1][2] == bold      # a heading over several lines
            short_bold = bold and len(text) <= 90 and not text.startswith("(") \
                and (not text.endswith((",", ";", ".")) or goes_on)
            if word or big or short_bold or (caps and len(text) <= 60 and size >= body):
                # a heading set larger or bold may run over two or three lines of the same size and weight;
                # a heading recognised by its words or capitals is one line
                parts, j = [text], i + 1
                while (big or short_bold) and j < len(ls) and len(parts) < 3 and ls[j][1] == size and ls[j][2] == bold \
                        and ls[j][3].y0 - ls[j - 1][3].y1 < size * 0.8:
                    parts.append(ls[j][0]); j += 1
                title = re.sub(r"\s+", " ", " ".join(parts).replace("\u00ad ", "").replace("\u00ad", "")).strip()
                title = re.sub(r"(?<=[a-ząćęłńóśźż])- (?=[a-ząćęłńóśźż])", "", title)    # a line-end hyphen of an old export
                title = re.sub(r"(?<=[^\d\s])\d{1,3}(?=\.?$)", "", title).strip().rstrip(":,;").strip()   # a note marker, a colon or comma at the end
                after_abstract = bool(out) and re.sub(r"[:.\s]+$", "", out[-1][1]).upper() in ("STRESZCZENIE", "SUMMARY", "ABSTRACT", "ABSTRAKT") \
                    and out[-1][2] in (pno, pno - 1)
                if after_abstract and caps and not word:                     # the title repeated in capitals under STRESZCZENIE / SUMMARY
                    i = j
                    continue
                if 2 <= len(title) <= 250 and not re.fullmatch(r"[\W\d]+", title):
                    out.append((2, title, pno, size))
                i = j
                continue
            i += 1
    # drop the article title itself (the largest type on the first article page) — it is level 1
    on_first = [s for _, _, p, s in out if p == first]
    if on_first and max(on_first) >= body * 1.3:
        top = max(on_first)
        out = [h for h in out if not (h[2] == first and h[3] == top)]
    return [(lv, t, p) for lv, t, p, _ in out]


def url_spans(page):
    """[(uri, [Rect, …])] for URLs and DOIs on the page; a URL broken over lines (up to three) is followed into the
    next line of its own text block: after a soft hyphen (dropped), or when it ends open (- / _ ? = & % # ~) and the
    next line starts with a word that can belong to a URL (a repeated hyphen at the break counts once)."""
    words = page.get_text("words")             # x0 y0 x1 y1 word block line wno
    lines = {}
    for w in words:
        lines.setdefault((w[5], w[6]), []).append(w)
    for k in lines:
        lines[k].sort(key=lambda w: w[7])
    keys = sorted(lines)

    def next_line(key):
        if (key[0], key[1] + 1) in lines:
            return (key[0], key[1] + 1)
        later = [k for k in keys if k[0] == key[0] + 1]
        return later[0] if later else None

    found, used = [], set()
    for key in keys:
        ws = lines[key]
        for wi, w in enumerate(ws):
            if (key, wi) in used:
                continue
            raw = w[4]
            m = URL_RE.search(raw.replace("\u00ad", ""))
            if not m:
                continue
            tok = raw.replace("\u00ad", "")[m.start():]
            rects = [pymupdf.Rect(w[:4])]
            cur, last_raw = key, raw
            for _ in range(3):                  # follow the URL into the next line(s)
                if wi != len(lines[cur]) - 1 and cur == key:
                    break
                soft = last_raw.endswith("\u00ad")
                nk = next_line(cur)
                if nk is None:
                    break
                nw = lines[nk][0]
                cont = nw[4].replace("\u00ad", "")
                dot = tok.endswith(".") and re.match(r"[a-z]{2,6}/", cont)    # „www.berghahnbooks.” + „com/title/…”
                if not (soft or dot or re.search(r"[-/_?=&%#~]$", tok)):
                    break
                if not re.fullmatch(r"[\w\-./?=&%#~:+]+[.,;:)]?", cont) or re.match(r"[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]", cont) \
                        or re.fullmatch(r"[A-ZĄĆĘŁŃÓŚŹŻ\-]{2,}[,.]?", cont):
                    break
                tok = tok + (cont[1:] if tok.endswith("-") and cont.startswith("-") else cont)
                rects.append(pymupdf.Rect(nw[:4]))
                used.add((nk, 0))
                cur, last_raw = nk, nw[4]
                if len(lines[nk]) > 1:          # the URL ended inside that line
                    break
            tok = re.sub(r"(?<=[a-z])\.\d{1,3}$", "", tok)     # „www.romowie.com.54”: full stop and a note marker
            tok = tok.rstrip(TRAIL)
            if len(tok) < 8:
                continue
            if tok.lower().startswith("www."):
                uri = "https://" + tok
            elif re.match(r"10\.\d{4,9}/", tok):
                uri = "https://doi.org/" + tok
            else:
                uri = tok
            found.append((uri, rects))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("--out")
    ap.add_argument("--no-bookmarks", action="store_true"); ap.add_argument("--no-links", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    npages = len(doc)
    cover = len(doc) > 1 and is_cover(doc[0])
    first = 1 if cover else 0
    n_bm, bm_state, n_links = 0, "none", 0

    if not a.no_bookmarks:
        if doc.get_toc():
            n_bm, bm_state = len(doc.get_toc()), "kept"
        else:
            body = body_size(doc, first)
            hs = headings(doc, first, body)
            title = (doc.metadata or {}).get("title") or (hs[0][1] if hs else os.path.basename(a.pdf))
            items = ([(1, "Strona metadanych", 0)] if cover else []) + [(1, title, first)] + hs
            if a.dry_run:
                for lv, t, p in items:
                    print(f"{'  ' * (lv - 1)}{t}  → p. {p + 1}")
            else:
                doc.set_toc([[lv, t, p + 1] for lv, t, p in items])
                doc.xref_set_key(doc.pdf_catalog(), "PageMode", "/UseOutlines")
            n_bm, bm_state = len(items), "added"

    if not a.no_links:
        for pno, page in enumerate(doc):
            have = [pymupdf.Rect(l["from"]) for l in page.get_links()]
            for uri, rects in url_spans(page):
                for r in rects:
                    if any(r.intersects(x) for x in have):
                        continue
                    if a.dry_run:
                        print(f"link p. {pno + 1}: {uri}")
                    else:
                        page.insert_link({"kind": pymupdf.LINK_URI, "from": r, "uri": uri})
                    have.append(r)
                    n_links += 1

    if not a.dry_run:
        out = a.out or a.pdf
        tmp = os.path.join(tempfile.mkdtemp(), "enhanced.pdf")     # outside the folder: it may not allow deleting files
        doc.save(tmp, garbage=4, deflate=True, use_objstms=1)
        doc.close()
        shutil.copyfile(tmp, out)                                  # overwrites in place (no delete, no rename)
    print(f"RESULT: bookmarks {n_bm} ({bm_state}) · links {n_links} added · pages {npages}")


if __name__ == "__main__":
    main()
