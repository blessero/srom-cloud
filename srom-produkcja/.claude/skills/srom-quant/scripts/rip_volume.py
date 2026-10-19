#!/usr/bin/env python3
"""
rip_volume.py — a back volume's draft master CSV from its printed pages (back catalogue, C19, MB 19.10.2026;
generalised from workspace volumes/17/rip_v17.py of 18.10.2026).

    python3 rip_volume.py <volume folder>/volume.json [--out <volume folder>/srom_master_v3.csv]

volume.json holds what a person reads off the contents page and the colophon (titles, authors, sections, page
ranges, the volume's dates and licence); the script reads the rest from the PDF: the Polish and English abstracts
and keywords (the STRESZCZENIE / SUMMARY blocks at the end of an article), the bio notes („Noty o autorach”), and
fills ORCIDs from volumes/autorzy.tsv. Nothing is invented: what the print does not give stays empty.

Sources, per article: its own InDesign export when volume.json names one (`article_pdfs`: soft hyphens there are
marked, so line-end hyphenation is undone exactly), else the volume PDF (`volume_pdf`, page = printed page +
`page_offset`). In the volume PDF a hyphen at a line end is ambiguous: the joined word is kept when the volume uses it
elsewhere, the hyphen when the volume writes the word with one, else the line-end hyphen is dropped and the join is
listed („not confirmed”) for a reader to check. `keep_hyphen` lists words read on the page.

Suffixes freeze once minted: a re-run keeps every final suffix already in the output CSV (by article_id); new rows
get todoNNNN placeholders for mint_suffixes.py. A re-run lists every filled cell it changes („cells changed against the
previous …”): corrections belong in volume.json (`bio_text`, `keep_hyphen`, or any CSV column as an
article key, which wins over what the PDF gives), not the CSV.

volume.json (all keys but `articles` are volume defaults an article may override):
  volume, year, signature, issue_theme, publisher, pub_date_print (YYYY or YYYY-MM-DD), pub_date_online,
  license (CC-BY-NC … or NONE), license_url, copyright_holder, volume_pdf, page_offset, notes_pages [first, last],
  article_pdfs {"001": "path"}, keep_hyphen [..], site, pdf_dir_url,
  articles: [{id, section (I–IV), from, to, title_pl, title_en, display, authors [[given, surname, affiliation, orcid|null]],
              bio (a name as „Noty o autorach” prints it) | bio_text, short (file name part), translators [[…]],
              is_translation, original_title, original_source, original_doi, + any default}]
  orcid null = look it up in autorzy.tsv (one person with that given name and surname and an ORCID), "" = none.
Last line: RESULT: <n> rows · abstracts <k> · bios <b> · ORCIDs from the register <o> · unconfirmed joins <u>.
"""
import argparse, csv, json, os, re, sys, unicodedata

import pymupdf

TOP = 30                                   # pt: a line starting above this is a running head or folio
COLS = ['article_id', 'doi_suffix', 'doi', 'landing_url', 'pdf_url', 'journal_title', 'issn', 'volume', 'year', 'issue_signature',
        'issue_theme', 'publisher', 'pub_date_online', 'pub_date_print', 'editorial_period', 'section_nr', 'section_label', 'seq',
        'title_pl', 'title_en', 'authors_display', 'authors_struct', 'affiliation_display', 'orcid_display', 'abstract_pl',
        'abstract_en', 'keywords_pl', 'keywords_en', 'bio_note', 'pages', 'pages_from', 'pages_to', 'pdf_file', 'language',
        'license', 'license_url', 'is_translation', 'original_title', 'original_source', 'original_doi', 'translators_struct',
        'copyright_holder']
PREFIX, SITE = "10.68100", "https://studiaromologica.pl"
MARK_PL = r"STRESZCZENIE|ABSTRAKT"
MARK_EN = r"SUMMARY|ABSTRACT"
KW_PL = r"Słowa kluczowe|Słowa-klucze"
KW_EN = r"Keywords|Key words|Key-words"


def page_text(page, top=TOP):
    """The page's text without the running head and folio: lines that start above `top` (InDesign puts them at
    18–20 pt; the text frame starts at about 43 pt; line boxes are taller than the type, so the line's top is measured)."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        ls = ["".join(s["text"] for s in l["spans"]) for l in b.get("lines", []) if l["bbox"][1] >= top]
        if ls:
            out.append("\n".join(ls))
    return "\n".join(out)


class Joiner:
    def __init__(self, voc, keep):
        self.voc, self.keep, self.unsure = voc, set(keep), []

    def __call__(self, s):
        s = s.replace("\u00ad\n", "").replace("\u00ad", "")          # marked soft hyphens: exact
        def j(m):
            x, y = m.group(1), m.group(2)
            if y.startswith("-"):                                    # repeated hyphen (Polish convention): a real one
                return x + y
            if (x + "-" + y) in self.keep: return x + "-" + y
            if (x + y) in self.voc or (x + y).lower() in self.voc: return x + y
            if (x + "-" + y) in self.voc: return x + "-" + y
            if y[:1].islower():
                self.unsure.append(x + "-|" + y); return x + y
            return x + "-" + y
        s = re.sub(r"(\w+)-\s*\n\s*(-?\w+)", j, s)
        s = s.replace("\xa0", " ")
        return re.sub(r"\s+", " ", s).strip()


def caps(line):
    letters = [c for c in line if c.isalpha()]
    return bool(letters) and all(c == c.upper() for c in letters)


def abstract_block(text, mark, kw, other_mark, names, J):
    """(abstract, keywords) of the block that starts with `mark`; ("", "") when there is none."""
    m = re.search(rf"(?m)^\s*(?:{mark})\s*:?\s*$", text)
    if not m:
        return "", ""
    rest = text[m.end():]
    stop = re.search(rf"(?m)^\s*(?:{other_mark})\s*:?\s*$", rest)
    if stop:
        rest = rest[:stop.start()]
    k = re.search(rf"(?:{kw})\s*:", rest)
    body, kws = (rest[:k.start()], rest[k.end():]) if k else (rest, "")
    lines = body.strip("\n").split("\n")
    i = 0
    while i < len(lines) and (not lines[i].strip() or caps(lines[i]) or any(n and n in lines[i] for n in names)):
        i += 1
    kws = re.split(r"\n\s*\n", kws.strip())[0] if kws.strip() else ""
    return J("\n".join(lines[i:])), J(kws)


def bios(text, J):
    """{first line of an entry (name as printed): bio without the contact line} from „Noty o autorach”.
    An entry starts at a line „[Dr |Dr hab. |Prof. ]Name Surname – …” that follows the end of the previous entry
    (a „Kontakt:” line, or the notes' heading); its text ends at its own „Kontakt:” line."""
    out, cur, who, open_ = {}, [], None, True
    for line in text.split("\n"):
        m = re.match(r"((?:(?:Dr hab\.|Dr|Prof\.|Prof\. dr hab\.)\s+)?[A-ZŁŚŻŹĆ][\w'-]+(?:\s+(?:[a-z]{1,3}\s+)?[A-ZŁŚŻŹĆ][\w'.-]+){1,4}"
                     r"(?:\s+i\s+(?:dr\s+)?[A-ZŁŚŻŹĆ][\w'-]+(?:\s+[A-ZŁŚŻŹĆ][\w'-]+){1,3})?)\s+–\s+(.*)", line)
        if m and open_:
            if who and cur:
                out[who] = cur
            who, cur, open_ = m.group(1), [m.group(2)], False
            continue
        if line.startswith("Kontakt:"):
            if who:
                out[who] = cur
            who, cur, open_ = None, [], True
            continue
        if who:
            cur.append(line)
    if who and cur:
        out[who] = cur
    res = {}
    for k, v in out.items():
        b = J("\n".join(v))
        res[k] = b[:1].upper() + b[1:]
    return res


def register(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig"), delimiter="\t")) if os.path.exists(path) else []
    return rows


def words(s):
    return re.findall(r"[^\W\d_]+(?:['-][^\W\d_]+)*", unicodedata.normalize("NFC", s or "").casefold())


def orcid_for(given, surname, reg):
    """The register's ORCID for one person: the first given name and every word of the surname must be whole words
    of `osoba` (review 20.10.2026: substring matching gave „Ann” Anna Piotrowska's ORCID); one hit or none."""
    want = words(given)[:1] + words(surname)
    if not words(surname):
        return ""
    hits = {r["orcid"].strip() for r in reg if r.get("orcid", "").startswith("https://orcid.org/")
            and all(w in words(r.get("osoba")) for w in want)}
    return hits.pop() if len(hits) == 1 else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config"); ap.add_argument("--out")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.config))
    C = json.load(open(a.config, encoding="utf-8"))
    out = a.out or os.path.join(base, "srom_master_v3.csv")
    rel = lambda p: (lambda q: q if not q or os.path.isabs(q) else os.path.normpath(os.path.join(base, q)))(os.path.expanduser(os.path.expandvars(p or "")))
    vol = pymupdf.open(rel(C["volume_pdf"]))
    off = int(C.get("page_offset", 0))
    vtext = [page_text(p) for p in vol]
    voc = set(re.findall(r"\w+(?:-\w+)*", " ".join(re.sub(r"\w+-\n\w+", " ", t) for t in vtext)))
    J = Joiner(voc, C.get("keep_hyphen", []))
    reg = register(os.path.join(os.path.dirname(base), "autorzy.tsv"))
    np = C.get("notes_pages")
    BIO = bios("\n".join(vtext[p + off] for p in range(np[0], np[1] + 1)), J) if np else {}

    keep, before = {}, {}
    if os.path.exists(out):
        for old in csv.DictReader(open(out, encoding="utf-8-sig")):
            before[old["article_id"]] = old
            if re.fullmatch(r"[a-z0-9]{8}", old.get("doi_suffix", "")):
                keep[old["article_id"]] = old["doi_suffix"]

    rows, n_abs, n_bio, n_reg = [], 0, 0, 0
    for n, art in enumerate(C["articles"], 1):
        g = lambda k, d="": art.get(k, C.get(k, d))
        aid = f"SROM-{C['volume']}-{C['year']}-{art['id']}"
        src = (art.get("pdf") or C.get("article_pdfs", {}).get(art["id"]))
        if src:
            d = pymupdf.open(rel(src))
            text = "\n".join(page_text(p) for p in d)
        else:
            text = "\n".join(vtext[p + off] for p in range(art["from"], art["to"] + 1))
        names = [art.get("display", "")] + [f"{x[0]} {x[1]}" for x in art.get("authors", [])] + [x[1] for x in art.get("authors", [])]
        ab_pl, kw_pl = abstract_block(text, MARK_PL, KW_PL, MARK_EN, names, J)
        ab_en, kw_en = abstract_block(text, MARK_EN, KW_EN, MARK_PL, names, J)
        n_abs += bool(ab_pl or ab_en)
        authors = []
        for x in art.get("authors", []):
            given, surname, aff = x[0], x[1], x[2] if len(x) > 2 else ""
            orc = x[3] if len(x) > 3 else None
            if orc is None:
                orc = orcid_for(given, surname, reg); n_reg += bool(orc)
            authors.append((given, surname, aff, orc or ""))
        bio = art.get("bio_text", "")
        if not bio and art.get("bio"):
            hits = [v for k, v in BIO.items() if art["bio"] in k]
            bio = hits[0] if len(hits) == 1 else ""
        n_bio += bool(bio)
        affs = []
        for au in authors:
            if au[2] and au[2] not in affs: affs.append(au[2])
        suf = keep.get(aid, f"todo{n:04d}")
        pdf_file = f"SROM_{C['volume']}_{C['year']}_{art['short']}.pdf"
        lic = g("license")
        rows.append({
            'article_id': aid, 'doi_suffix': suf, 'doi': f"{PREFIX}/{suf}", 'landing_url': f"{SITE}/articles/{PREFIX}/{suf}/",
            'pdf_url': f"{SITE}/wp-content/uploads/archive/{C['volume']}-{C['year']}/{pdf_file}",
            'journal_title': 'Studia Romologica', 'issn': '1689-4758', 'volume': str(C['volume']), 'year': str(C['year']),
            'issue_signature': C.get('signature', f"SROM·{C['volume']}·{C['year']}"), 'issue_theme': g('issue_theme'),
            'publisher': g('publisher'), 'pub_date_online': g('pub_date_online'), 'pub_date_print': str(g('pub_date_print')),
            'editorial_period': g('editorial_period'), 'section_nr': art['section'], 'section_label': f"Część {art['section']}",
            'seq': str(n), 'title_pl': art['title_pl'], 'title_en': art.get('title_en', ''),
            'authors_display': art.get('display', ''), 'authors_struct': " ;; ".join("|".join(au) for au in authors),
            'affiliation_display': " / ".join(affs), 'orcid_display': " ; ".join(au[3] for au in authors if au[3]),
            'abstract_pl': ab_pl, 'abstract_en': ab_en, 'keywords_pl': kw_pl,
            'keywords_en': "; ".join(k.strip() for k in re.split(r"[;,]", kw_en) if k.strip()),
            'bio_note': bio, 'pages': f"{art['from']}–{art['to']}", 'pages_from': str(art['from']), 'pages_to': str(art['to']),
            'pdf_file': pdf_file, 'language': g('language', 'pl'), 'license': lic,
            'license_url': "" if lic == "NONE" else g('license_url'),
            'is_translation': art.get('is_translation', ''), 'original_title': art.get('original_title', ''),
            'original_source': art.get('original_source', ''), 'original_doi': art.get('original_doi', ''),
            'translators_struct': " ;; ".join("|".join(t) for t in art.get('translators', [])),
            'copyright_holder': g('copyright_holder')})
        rows[-1].update({k: str(art[k]) for k in COLS if k in art and k not in ('doi_suffix', 'doi', 'landing_url')})  # an article key wins (a correction)
    # a re-run rewrites the CSV from volume.json and the PDFs: name every filled cell it changes, so a hand edit made
    # in the CSV is seen before it is lost (put lasting corrections into volume.json; review 20.10.2026)
    changed = [f"{r['article_id'][-3:]}:{k}" for r in rows for k, v in r.items()
               if k not in ("doi_suffix", "doi", "landing_url")          # the suffix is kept; these follow it
               and (before.get(r["article_id"], {}).get(k) or "") not in ("", v)]
    if changed:
        print(f"cells changed against the previous {os.path.basename(out)}: {len(changed)}: " + ", ".join(changed[:30])
              + (" …" if len(changed) > 30 else ""))
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    if J.unsure:
        print("joins not confirmed by the volume's own vocabulary:", ", ".join(J.unsure))
    print(f"bio entries read: {len(BIO)}" + (f" ({', '.join(sorted(BIO))})" if BIO else ""))
    print(f"written {out}")
    print(f"RESULT: {len(rows)} rows · abstracts {n_abs} · bios {n_bio} · ORCIDs from the register {n_reg} · unconfirmed joins {len(J.unsure)}")


if __name__ == "__main__":
    main()
