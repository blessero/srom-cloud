#!/usr/bin/env python3
"""
cover_page.py — the online edition's metadata page, put in front of the article's PDF (MB, 03.10.2026).

    python3 cover_page.py volumes/<vol>/srom_master_v3.csv <article_id> <article.pdf> --out <dir> [--proof]
        → <dir>/<pdf_file>   cover page + the article, ready to upload
    python3 cover_page.py volumes/<vol>/srom_master_v3.csv <article_id> --out <dir> [--proof]
        → <dir>/<article_id>_okladka.pdf   the cover page alone, to look at

One source: the master CSV row (master_schema.md). No InDesign: PyMuPDF draws the page at the journal's trim size
(165 × 235 mm) after MB's template (SROM_okladka_szablon_MB1.2.idml, 04.10.2026: IBM Plex Sans, SROM red, all other
type 88 % black = RGB 66 66 65), so it reads as a digital add-on, not a printed page. The final PDF also gets links (DOI, ORCID, licence,
the original's DOI, the journal's site), page labels (cover i; the article keeps its printed page numbers) and the
metadata of pdf_metadata.py (Info dictionary + XMP with PRISM).

One page, strictly (MB, 04.10.2026): the two abstract blocks (Polish, then English, each with its keywords) are not
frames of a fixed height. The Polish one starts under the citation, the English one follows it at the template's gap,
and the English one may grow down to ABSTRACT_BOTTOM (218 mm from the top; the footer starts below it). The keywords stand 14 pt (baseline to baseline) under the last line. The type is
7.2 pt in both; only if the text still does not fit, both go down to 7 pt (never below, never one without the other).
If it does not fit at 7 pt, the run stops and names the overflow. The header, footer and leading never change.
Texts without abstracts (reviews, chronicles) get the header alone.

A printed field holding a placeholder (10.XXXXX, todo…, TODO) or left empty stops the run, so a page with a fake DOI
is never written; --proof prints it as it stands, marks the page PODGLĄD and names the file *_proof.pdf.
"""
import argparse, csv, html, os, re, sys
from datetime import datetime, timezone

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_metadata import build as metadata, licence_name, placeholder  # noqa: E402

MM = 72 / 25.4
W, H = 165 * MM, 235 * MM                      # SROM trim size (InDesign template: 467.72 × 666.14 pt)
# geometry in pt, from MB's template (frames' top-left corners; text frames grow downwards)
LX, TX, RX = 17.0, 70.9, 433.7                 # label column · text column · right edge
LOGO = (70.9, 11.3, 184.3, 57.5)               # x0 y0 x1 y1
INFO_X, INFO_Y, JOURNAL_Y, TITLE_Y = 290.4, 12.5, 61.8, 95.8
FOOT, OA = 627.2, (17.0, 630.2, 62.2, 646.5)
BAR = 4.25                                     # red bars at both edges, full height
GAP = {"title_en": 7.3, "author": 7.2, "author2": 6, "translator": 6, "cite": 10.3, "original": 4,
       "abstract": 15.6, "abstract_en": 13.4, "journal": 13.1}   # frame to frame, as in the template
ABSTRACT_BOTTOM = 218 * MM                     # the English abstract may grow down to here (MB, 04.10.2026)
ABSTRACT_LEAD, KEYWORDS_GAP = 10, 4           # pt: leading of the abstracts; extra space above the keywords line
ABSTRACT_SIZES = (7.2, 7.0)                    # pt, both abstracts; 7.0 only when 7.2 does not fit
RED = (227 / 255, 0, 11 / 255)                 # "SROM red", RGB 227 0 11
INK = "#424241"                                # 88 % black (CMYK 0 0 0 88 → RGB 66 66 65, InDesign's conversion)
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "cover")
FONT_DIRS = [d for d in (os.environ.get("SROM_FONT_DIR"),                       # any folder holding the two .ttf files
                         os.path.expanduser("~/Library/Fonts/FontBase"), os.path.expanduser("~/Library/Fonts"), "/Library/Fonts",
                         os.path.expanduser("~/.local/share/fonts"), os.path.expanduser("~/.fonts"),   # Linux (Cowork's VM)
                         "/usr/share/fonts/truetype/ibm-plex", "/usr/share/fonts/truetype") if d]
FONTS = {"normal": "IBMPlexSans-Regular.ttf", "italic": "IBMPlexSans-Italic.ttf"}
SITE = "https://studiaromologica.pl"

# Polish names of the CC 4.0 licences (official Polish translation). The clause after the name is MB's for CC BY
# (template, 03.10.2026); the other licences point to the licence text until MB approves a wording (SYS-6).
CC_PL = {"by": "Uznanie autorstwa", "by-sa": "Uznanie autorstwa – Na tych samych warunkach",
         "by-nd": "Uznanie autorstwa – Bez utworów zależnych", "by-nc": "Uznanie autorstwa – Użycie niekomercyjne",
         "by-nc-sa": "Uznanie autorstwa – Użycie niekomercyjne – Na tych samych warunkach",
         "by-nc-nd": "Uznanie autorstwa – Użycie niekomercyjne – Bez utworów zależnych"}
CC_BY_CLAUSE = ("zezwalającej na nieograniczone używanie, rozpowszechnianie i kopiowanie w dowolnym medium "
                "pod warunkiem prawidłowego zacytowania oryginału")

CSS = """
@font-face {font-family: plex; src: url(%(normal)s);}
@font-face {font-family: plex; font-style: italic; src: url(%(italic)s);}
* {font-family: plex; margin: 0; padding: 0; color: #424241;}
p {margin: 0;}
.red {color: #e3000b;}
"""


def esc(s):
    return html.escape(s or "", quote=True)


def nbsp(s):
    """Kanon § 3.3: no line break after one-letter words, s. t. z. nr r. w. sygn. k. and initials, nor before %
    (InDesign does it by GREP style; the cover is not set in InDesign)."""
    s = re.sub(r"(?<![\w.])([aiouwzAIOUWZ]|[stzrwk]\.|nr|sygn\.|[A-ZĄĆĘŁŃÓŚŹŻ]\.) ", "\\1\u00a0", s or "")
    s = re.sub(r"(?<![\w.])([aiouwzAIOUWZ]|[A-ZĄĆĘŁŃÓŚŹŻ]\.) ", "\\1\u00a0", s)        # a second one-letter word in a row
    return s.replace(" %", "\u00a0%")


def pl(s):
    return esc(nbsp(s))


def font_dir():
    for d in FONT_DIRS:
        if all(os.path.exists(os.path.join(d, f)) for f in FONTS.values()):
            return d
    sys.exit(f"ABORT: IBM Plex Sans ({', '.join(FONTS.values())}) not found in {', '.join(FONT_DIRS)}.")


def authors(row):
    """[(name, affiliation, orcid)] from authors_struct; falls back to the display columns."""
    out = []
    for a in (row.get("authors_struct") or "").split(";;"):
        f = [x.strip() for x in a.split("|")] + ["", "", "", ""]
        if f[0] or f[1]:
            out.append((f"{f[0]} {f[1]}".strip(), f[2], f[3]))
    return out or [(row.get("authors_display", ""), row.get("affiliation_display", ""), row.get("orcid_display", ""))]


def translators(row):
    return [f"{f[0]} {f[1]}".strip() for f in ([x.strip() for x in t.split("|")] + ["", ""]
            for t in (row.get("translators_struct") or "").split(";;")) if f[0] or f[1]]


def date_pl(iso):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", iso or "")
    return f"{m.group(3)}.{m.group(2)}.{m.group(1)}" if m else (iso or "")      # Kanon § 3.5: dd.mm.rrrr


def keywords(s):
    return "; ".join(k.strip() for k in re.split(r"[;,]", s or "") if k.strip())   # Kanon § 1 pt 9: semicolon


def licence(row):
    """(short name, the footer sentence) from license_url; ("", "") if it is not a CC licence URL."""
    url = row.get("license_url", "")
    m = re.search(r"licenses/([a-z-]+)/(\d\.\d)", url)
    if not m:
        return "", ""
    code, ver = m.group(1), m.group(2)
    short = licence_name(url, row.get("license", ""))
    tail = CC_BY_CLAUSE if code == "by" else f"pełny tekst licencji: {url}"
    return short, f"Artykuł w otwartym dostępie na licencji Creative Commons {CC_PL.get(code, code.upper())} {ver} ({short}), {tail}."


def check(row):
    """What the page prints; a placeholder or a gap is a problem (fatal unless --proof)."""
    probs = []
    for k in ("title_pl", "title_en", "authors_display", "volume", "year", "pages"):
        if not row.get(k) or placeholder(row.get(k)):
            probs.append(f"{k} empty")
    if placeholder(row.get("doi")):
        probs.append(f"doi is a placeholder: {row.get('doi') or 'empty'}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.get("pub_date_online", "")):
        probs.append(f"pub_date_online not YYYY-MM-DD: {row.get('pub_date_online') or 'empty'}")
    if not licence(row)[0]:
        probs.append(f"license_url not a CC licence: {row.get('license_url') or 'empty'}")
    have = [k for k in ("abstract_pl", "abstract_en", "keywords_pl", "keywords_en") if row.get(k)]
    if have and len(have) < 4:
        probs.append("missing: " + ", ".join(sorted({"abstract_pl", "abstract_en", "keywords_pl", "keywords_en"} - set(have))))
    if row.get("is_translation") == "TAK" and not translators(row):
        probs.append("translation without translators_struct (Kanon § 12.2.3)")
    return probs


class Pen:
    """Writes HTML blocks on one page; put() returns the y below the block and fails rather than shrink the type."""

    def __init__(self, page, fdir):
        self.page, self.fdir = page, fdir
        self.arch = pymupdf.Archive(fdir)
        self.css = CSS % FONTS

    def put(self, x0, y, x1, body, bottom=None):
        r = pymupdf.Rect(x0, y, x1, bottom or H)
        spare, _ = self.page.insert_htmlbox(r, body, css=self.css, archive=self.arch, scale_low=1)
        if spare < 0:
            raise ValueError("does not fit")
        return r.y1 - spare - 2.0               # PyMuPDF's block is 2 pt taller than InDesign's frame (measured on MB's template)


def a(href, text):
    return f'<a href="{esc(href)}" style="color:#424241; text-decoration:none">{text}</a>'


def p(size, lead, body, cls="", extra=""):
    return f'<p{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} style="font-size:{size}pt; line-height:{lead}pt{extra}">{body}</p>'


def band(pen, row):
    """Logo, the journal block under it and the info block at the right; returns where the title may start."""
    for x in (0, W - BAR):
        pen.page.draw_rect(pymupdf.Rect(x, 0, x + BAR, H), color=None, fill=RED)
    box = pymupdf.Rect(*LOGO)
    pen.page.show_pdf_page(box, pymupdf.open(os.path.join(ASSETS, "sr_logo.pdf")), 0)
    pen.page.insert_link({"kind": pymupdf.LINK_URI, "from": box, "uri": SITE})
    short = licence(row)[0]
    doi_url = f"https://doi.org/{row.get('doi', '')}"
    info = [f'Strony: {esc(row.get("pages"))}' if row.get("pages") else "", a(doi_url, esc(doi_url)), esc(short),
            f'© {esc(row.get("year"))} {esc(", ".join(a[0] for a in authors(row)))}',
            f'Opublikowano online: {esc(date_pl(row.get("pub_date_online")))}']
    info = [s for s in info if s]
    font = pymupdf.Font(fontfile=os.path.join(pen.fdir, FONTS["normal"]))
    iw = max(font.text_length(html.unescape(re.sub(r"<[^>]+>", "", s)), 8) for s in info)
    ix = min(INFO_X, RX - iw - 1)                  # a long line (DOI, names) moves the block left, never wraps it
    right = pen.put(ix, INFO_Y, RX + 2, "".join(p(8, 10.5, s) for s in info))
    journal = [f'{esc(row.get("journal_title") or "Studia Romologica")} {esc(row.get("volume"))}/{esc(row.get("year"))}',
               f'ISSN: {esc(row.get("issn") or "1689-4758")}']
    left = pen.put(TX, JOURNAL_Y, TX + 143.3, "".join(p(8, 10.5, s) for s in journal))
    return max(TITLE_Y, left + GAP["journal"], right + GAP["journal"])


def header(pen, row, y):
    """Titles, authors, translator, citation, original; returns the y below."""
    y = pen.put(TX, y, RX, p(16, 19, pl(row.get("title_pl")), "red"))
    y = pen.put(TX, y + GAP["title_en"], RX, p(12, 16, esc(row.get("title_en"))))
    au = authors(row)
    for i, (name, aff, orcid) in enumerate(au):
        body = p(12.5, 15, esc(name), "red")
        if aff:
            body += p(9.5, 12, pl(aff))
        if orcid:
            body += p(9.5, 12, a(orcid, esc(orcid)))
        y = pen.put(TX, y + (GAP["author"] if i == 0 else GAP["author2"]), RX, body)
    tr = translators(row)
    if tr:
        y = pen.put(TX, y + GAP["translator"], RX, p(9.5, 12, f"Tłumaczenie: {esc(', '.join(tr))}"))
    cite = (f'<span class="red">Jak cytować:</span> {esc(", ".join(a[0] for a in au))}, <i>{pl(row.get("title_pl"))}</i>, '
            f'„{esc(row.get("journal_title") or "Studia Romologica")}”, {esc(row.get("year"))}, t.\u00a0{esc(row.get("volume"))}'
            + (f", s.\u00a0{esc(row.get('pages'))}" if row.get("pages") else "") + ".")
    y = pen.put(TX, y + GAP["cite"], RX, p(8, 10.5, cite))
    if row.get("is_translation") == "TAK" and (row.get("original_title") or row.get("original_source")):
        orig = ", ".join(x for x in (f'<i>{esc(row.get("original_title"))}</i>' if row.get("original_title") else "",
                                     esc(row.get("original_source"))) if x)
        od = row.get("original_doi", "")
        if od and not placeholder(od):
            orig = a(f"https://doi.org/{od}", orig)
        y = pen.put(TX, y + GAP["original"], RX, p(8, 10.5, f'<span class="red">Pierwodruk:</span> {orig}'))
    return y


def abstract(pen, row, key, y, size):
    """Label in the left column, abstract and keywords in the text column; the block is as tall as its text
    (down to ABSTRACT_BOTTOM at most); returns the y below."""
    label, kw = {"pl": ("Abstrakt", "Słowa kluczowe:"), "en": ("Abstract", "Keywords:")}[key]
    text = pl if key == "pl" else esc
    lead = ABSTRACT_LEAD
    pen.put(LX, y, TX - 4, p(9.5, 11.5, label, "red"))
    body = (p(size, lead, text(row.get("abstract_" + key)), extra="; text-align:justify")
            + p(size, lead, f'<span class="red">{kw}</span> {text(keywords(row.get("keywords_" + key)))}',
                extra=f"; text-align:justify; margin-top:{KEYWORDS_GAP}pt"))
    return pen.put(TX, y, RX, body, bottom=ABSTRACT_BOTTOM)


def footer(pen, row):
    oa = pymupdf.open(os.path.join(ASSETS, "open_access.pdf"))
    pen.page.show_pdf_page(pymupdf.Rect(*OA), oa, 0)
    lic = licence(row)[1]
    body = p(6, 8.5, a(row.get("license_url"), pl(lic)), extra="; letter-spacing:-0.01em") if lic else ""
    body += p(6, 8.5, f'Wydawca: {pl(row.get("publisher"))} · {a(SITE, SITE.split("//")[1])}',
              extra="; letter-spacing:-0.01em" + ("; margin-top:3pt" if lic else ""))
    pen.put(TX, FOOT, RX, body)


def page(row, size, fdir):
    doc = pymupdf.open()
    pen = Pen(doc.new_page(width=W, height=H), fdir)
    y = header(pen, row, band(pen, row))
    for i, k in enumerate(k for k in ("pl", "en") if row.get("abstract_" + k)):
        y = abstract(pen, row, k, y + (GAP["abstract"] if i == 0 else GAP["abstract_en"]), size)
    footer(pen, row)
    return doc


def cover(row, proof=False):
    """The cover as a one-page PyMuPDF document; the abstracts take 7.2 pt, then 7 pt, then the run stops."""
    fdir = font_dir()
    for size in ABSTRACT_SIZES:
        try:
            doc = page(row, size, fdir)
            break
        except ValueError:
            pass
    else:
        sys.exit(f"ABORT: {row.get('article_id')}: the cover does not fit on one page even at {ABSTRACT_SIZES[-1]} pt "
                 f"(abstracts {len(row.get('abstract_pl', ''))} + {len(row.get('abstract_en', ''))} characters, "
                 f"the English one may end at {ABSTRACT_BOTTOM / MM:.0f} mm). Shorten an abstract.")
    if proof:
        doc[0].insert_text((LX, 120), "PODGLĄD", fontsize=10, color=RED,
                           fontname="plex", fontfile=os.path.join(fdir, FONTS["normal"]))
    return doc, size


def xmp(meta, row):
    """XMP packet: Dublin Core, rights, and the PDF/PRISM fields of pdf_metadata.build()."""
    e = lambda s: html.escape(s or "", quote=False)
    props = "".join(f"<{k}>{e(v)}</{k}>" for _, k, v in meta["props"] if k != "dc:identifier")
    ident = next((v for _, k, v in meta["props"] if k == "dc:identifier"), "")
    creators = "".join(f"<rdf:li>{e(a[0])}</rdf:li>" for a in authors(row))
    subjects = "".join(f"<rdf:li>{e(k)}</rdf:li>" for k in meta["keywords"])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"
 xmlns:pdf="http://ns.adobe.com/pdf/1.3/" xmlns:prism="http://prismstandard.org/namespaces/basic/2.0/" xmlns:xmp="http://ns.adobe.com/xap/1.0/">
<dc:format>application/pdf</dc:format>
<dc:title><rdf:Alt><rdf:li xml:lang="x-default">{e(meta["title"])}</rdf:li></rdf:Alt></dc:title>
<dc:creator><rdf:Seq>{creators}</rdf:Seq></dc:creator>
<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{e(meta["subject"])}</rdf:li></rdf:Alt></dc:description>
<dc:subject><rdf:Bag>{subjects}</rdf:Bag></dc:subject>
<dc:language><rdf:Bag><rdf:li>{e(row.get("language") or "pl")}</rdf:li></rdf:Bag></dc:language>
<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{e(meta["notice"])}</rdf:li></rdf:Alt></dc:rights>
{f"<dc:identifier>{e(ident)}</dc:identifier>" if ident else ""}
<xmpRights:Marked>True</xmpRights:Marked><xmpRights:WebStatement>{e(meta["licenceUrl"])}</xmpRights:WebStatement>
<xmp:MetadataDate>{now}</xmp:MetadataDate>
{props}
</rdf:Description></rdf:RDF></x:xmpmeta>
<?xpacket end="w"?>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master"); ap.add_argument("article_id"); ap.add_argument("article_pdf", nargs="?")
    ap.add_argument("--out", default="."); ap.add_argument("--proof", action="store_true")
    a = ap.parse_args()
    rows = [{k.lstrip("\ufeff"): v for k, v in r.items()} for r in csv.DictReader(open(a.master, encoding="utf-8"))]
    row = next((r for r in rows if r["article_id"] == a.article_id), None)
    if row is None:
        sys.exit(f"ABORT: {a.article_id}: no such row in {a.master}")
    probs = check(row)
    if probs and not a.proof:
        sys.exit(f"ABORT: {a.article_id}: " + "; ".join(probs) + ". Fill the master CSV (or run with --proof).")
    doc, size = cover(row, a.proof)
    n = len(doc)
    os.makedirs(a.out, exist_ok=True)
    tag = "_proof" if a.proof else ""
    if not a.article_pdf:
        path = os.path.join(a.out, f"{a.article_id}_okladka{tag}.pdf")
        doc.save(path, garbage=4, deflate=True)
    else:
        art = pymupdf.open(a.article_pdf)
        r0 = art[0].rect
        if abs(r0.width - W) > 1 or abs(r0.height - H) > 1:
            probs.append(f"article page is {r0.width / MM:.1f} × {r0.height / MM:.1f} mm, not 165 × 235 "
                         "(export without bleed and marks)")
        span = [int(x) for x in (row.get("pages_from"), row.get("pages_to")) if (x or "").isdigit()]
        if len(span) == 2 and len(art) != span[1] - span[0] + 1:
            probs.append(f"article PDF has {len(art)} pages, the CSV says {span[0]}–{span[1]} ({span[1] - span[0] + 1})")
        art.insert_pdf(doc, start_at=0)                    # the article's bookmarks and links keep their pages
        first = int(row["pages_from"]) if (row.get("pages_from") or "").isdigit() else 1
        art.set_page_labels([{"startpage": 0, "prefix": "", "style": "r", "firstpagenum": 1},
                             {"startpage": n, "prefix": "", "style": "D", "firstpagenum": first}])
        meta, warn = metadata(row)
        art.set_metadata({"title": meta["title"], "author": meta["author"], "subject": meta["subject"],
                          "keywords": "; ".join(meta["keywords"]), "creator": "Studia Romologica (srom-quant cover_page.py)",
                          "producer": f"PyMuPDF {pymupdf.VersionBind}"})
        art.set_xml_metadata(xmp(meta, row))
        path = os.path.join(a.out, re.sub(r"\.pdf$", "", row.get("pdf_file") or a.article_id) + tag + ".pdf")
        art.save(path, garbage=3, deflate=True)
    print(f"written {path}"
          + "".join(f"\n!! {x}" for x in probs))
    print("RESULT: PROOF — not for upload" if a.proof else
          f"RESULT: CHECK — {len(probs)} warning(s) above before upload" if probs else "RESULT: OK")


if __name__ == "__main__":
    main()
