#!/usr/bin/env python3
"""Zizek text extraction: PDF / DOCX / MD / TXT -> plain text with page markers.

Deterministic on purpose: never let an LLM "clean" a text we are about to judge,
it smooths over exactly the inconsistencies we are looking for.

Usage:
  python3 "$Z/extract.py" <volume-folder> <file-or-folder> [more ...] [--pages 45-80]

  <volume-folder>  e.g. volumes/19-2026  (text goes to <volume-folder>/text/<slug>.txt)
  --pages A-B      PDF only, 1-based inclusive; use it for one chapter of a book

Prints one line per file for pool.md: slug | pages | words | language guess | warnings.
Existing .txt files are overwritten (the source file is the truth, the .txt is derived).
"""
import datetime
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import fitz  # PyMuPDF

SKIP = {".ds_store", "thumbs.db"}
STOP = {
    "pl": " i w na z się nie że do jest o to od przez oraz jak po także który która które ".split(),
    "en": " the of and to in is that for as with by this which are was on ".split(),
    "es": " el la de que y en los las del se por con una para como ".split(),
    "ca": " el la de i que en els les del per amb una com al és ".split(),
    "de": " der die und das den zu in ist nicht mit von sich des auf für ".split(),
    "fr": " le la les de et des en que un une du pour dans est qui ".split(),
}


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:48].rstrip("-") or "text"


def guess_lang(text: str) -> str:
    words = re.findall(r"[a-ząćęłńóśźżàèéíòóúüçñ']+", text[:40000].lower())
    if len(words) < 50:
        return "?"
    scores = {k: sum(w in v for w in words) for k, v in STOP.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > len(words) * 0.03 else "?"


def pdf_text(path: Path, pages):
    doc = fitz.open(path)
    first, last = (1, len(doc)) if pages is None else pages
    last = min(last, len(doc))
    flags = fitz.TEXT_DEHYPHENATE | fitz.TEXT_PRESERVE_WHITESPACE
    out = []
    for i in range(first - 1, last):
        out.append(f"\n=== page {i + 1} ===\n")
        out.append(doc[i].get_text("text", flags=flags))
    return "".join(out), last - first + 1


def docx_text(path: Path):
    # pandoc keeps footnotes (as numbered notes at the end); python-docx would drop them
    r = subprocess.run(["pandoc", str(path), "-t", "plain", "--wrap=none"],
                       capture_output=True, text=True, check=True)
    return r.stdout, None


def extract(path: Path, textdir: Path, pages, used: set):
    ext = path.suffix.lower()
    if ext == ".pdf":
        body, npages = pdf_text(path, pages)
    elif ext == ".docx":
        body, npages = docx_text(path)
    elif ext in (".md", ".txt"):
        body, npages = path.read_text(encoding="utf-8", errors="replace"), None
    else:
        return None
    words = len(re.findall(r"\w+", body))
    warn = []
    if npages and words / npages < 50:
        warn.append("NO/THIN TEXT LAYER - needs OCR")
    if npages and npages > 80 and pages is None:
        warn.append("book-length - card a chapter with --pages")
    slug = slugify(path.stem)
    if pages:
        slug += f"-p{pages[0]}-{pages[1]}"
    if slug in used:  # same name, different format (e.g. .docx and .pdf of one text)
        slug += "-" + ext.lstrip(".")
    used.add(slug)
    header = (f"# source: {path}\n# extracted: {datetime.date.today()} by srom-zizek extract.py"
              f"{' pages %d-%d' % pages if pages else ''}\n")
    (textdir / f"{slug}.txt").write_text(header + body, encoding="utf-8")
    return slug, npages, words, guess_lang(body), "; ".join(warn)


def main(argv):
    pages = None
    if "--pages" in argv:
        i = argv.index("--pages")
        a, b = argv[i + 1].split("-")
        pages = (int(a), int(b))
        del argv[i:i + 2]
    if len(argv) < 2:
        sys.exit(__doc__)
    textdir = Path(argv[0]) / "text"
    textdir.mkdir(parents=True, exist_ok=True)
    files = []
    for arg in argv[1:]:
        p = Path(arg)
        files += sorted(f for f in p.iterdir() if f.is_file()) if p.is_dir() else [p]
    used = set()
    for f in files:
        if f.name.lower() in SKIP:
            continue
        try:
            r = extract(f, textdir, pages, used)
        except Exception as e:  # report and go on; one bad file must not stop a batch
            print(f"{f.name} | ERROR {e}")
            continue
        if r:
            slug, npages, words, lang, warn = r
            print(f"{slug} | {npages or '-'} pp | {words} w | {lang} | {warn} | {f.name}")
        else:
            print(f"{f.name} | skipped (unsupported type)")


if __name__ == "__main__":
    main(sys.argv[1:])
