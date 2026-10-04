#!/usr/bin/env python3
"""Zizek output check: are the anchors verbatim, is the card complete, do the DOIs exist?

Rule 2 (anchors verbatim) is the rule a model breaks without noticing; this makes it mechanical.
Run it on every card and deep-review file before trusting it, and on all cards before `block`.

Usage:
  python3 "$Z/check.py" <file.md> [more.md ...] [--text path.txt] [--online]

  The text is found from the header line "text: text/<slug>.txt" (cards and deep files both carry it),
  relative to the volume folder; --text overrides it.
  --online  also look up every DOI under "## Sources" at Crossref (published works only - never
            use it on anything that would send manuscript text out; DOIs are safe).

Anchors = quoted spans of 4+ words ("…", “…”, „…”) outside the Sources section. Matching is on words,
ignoring case, punctuation and page markers; "…" / "..." inside a quote splits it into fragments.
  FOUND    every word, in order, in the text
  CLOSE    near-match (note numbers, running heads, a changed word) - compare the two and fix the anchor
  MISSING  not in the text: a misquote, a paraphrase in quotes, or a quote from another source
Cards (files under cards/) are also checked for sections, scores 1-5, verdict and length.
Exit code 1 if anything is MISSING or a card is structurally incomplete.
"""
import json
import re
import sys
import unicodedata
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

QUOTE = re.compile(r'"([^"\n]+)"|“([^”\n]+)”|„([^”"\n]+)[”"]')
WORD = re.compile(r"\w+")
CARD_SECTIONS = ["## 1. Claim", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7.", "## 8.", "## Sources"]
VERDICTS = ("CORE", "STRONG", "CONDITIONAL", "OUT")


def words(s: str):
    s = unicodedata.normalize("NFKC", s).replace("­", "")
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)  # line-end hyphenation the extractor left
    return [w.casefold() for w in WORD.findall(s)]


def load_text(path: Path):
    t = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"^=== page \d+ ===$", " ", t, flags=re.M)
    t = re.sub(r"^# (source|extracted):.*$", " ", t, flags=re.M)
    return words(t)


def locate(frag, tw, index):
    n = len(frag)
    for i in index.get(frag[0], ()):
        if tw[i:i + n] == frag:
            return "FOUND", None
    best, where = 0.0, None
    cands = set(index.get(frag[0], ())) | {i - n + 1 for i in index.get(frag[-1], ())}
    for i in cands:
        for j in (i, i - 1, i + 1):  # allow one inserted/dropped word at the start
            if j < 0:
                continue
            r = SequenceMatcher(None, frag, tw[j:j + n + 2], autojunk=False).ratio()
            if r > best:
                best, where = r, j
    if best >= 0.75:
        return "CLOSE", " ".join(tw[where:where + n + 2])
    return "MISSING", None


def check_anchors(md_lines, tw):
    index = {}
    for i, w in enumerate(tw):
        index.setdefault(w, []).append(i)
    res = []
    for ln, line in enumerate(md_lines, 1):
        if line.startswith("## Sources"):
            break
        for m in QUOTE.finditer(line):
            q = next(g for g in m.groups() if g)
            frags = [words(f) for f in re.split(r"…|\.\.\.", q)]
            frags = [f for f in frags if f]
            if sum(len(f) for f in frags) < 4:
                continue
            status, near = "FOUND", None
            for f in frags:
                s, nr = locate(f, tw, index)
                if s != "FOUND":
                    status, near = s, nr
                    if s == "MISSING":
                        break
            res.append((ln, status, q, near))
    return res


def check_card(text: str):
    probs = []
    for h in CARD_SECTIONS:
        if h not in text:
            probs.append(f"section missing: {h}")
    m = re.search(r"## 6\..*?\n\|.*?\n\|[-| ]+\|\n\|([^\n]+)\|", text, flags=re.S)
    if not m:
        probs.append("scores table not found in section 6")
    else:
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) != 3 or not all(c in "12345" and c for c in cells):
            probs.append(f"scores not three values 1-5: {cells}")
    v = re.search(r"## 7\.[^\n]*\n+([^\n]+)", text)
    if not v or not v.group(1).lstrip("*").startswith(VERDICTS):
        probs.append("verdict line does not start with CORE / STRONG / CONDITIONAL / OUT")
    body = text.split("## Sources")[0]
    body = "\n".join(l for l in body.splitlines() if not l.startswith("|"))
    body = body.split("## 1. Claim", 1)[-1]
    n = len(WORD.findall(body))
    note = "" if 600 <= n <= 1300 else "  <- outside 600-1,300: trim, or move depth to a deep review"
    return probs, f"length {n} words (sections 1-8, tables excluded){note}"


def check_dois(text: str):
    src = text.split("## Sources", 1)
    if len(src) < 2:
        return ["no Sources section"]
    out = []
    for doi in sorted(set(re.findall(r"10\.\d{4,9}/[^\s)\]>,;]+", src[1]))):
        doi = doi.rstrip(".")
        try:
            req = urllib.request.Request(f"https://api.crossref.org/works/{doi}",
                                         headers={"User-Agent": "Zizek-check/1.0 (mailto:srom@local)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                msg = json.load(r)["message"]
            title = (msg.get("title") or ["?"])[0]
            year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
            out.append(f"  ok       {doi} — {title[:90]} ({year})")
        except urllib.error.HTTPError as e:
            out.append(f"  NOT REGISTERED at Crossref ({e.code}) {doi} — check DataCite/publisher before trusting")
        except Exception as e:  # network down etc.
            out.append(f"  ?        {doi} — lookup failed: {e}")
    return out or ["  (no DOIs in Sources)"]


def main(argv):
    online = "--online" in argv
    argv = [a for a in argv if a != "--online"]
    text_override = None
    if "--text" in argv:
        i = argv.index("--text")
        text_override = Path(argv[i + 1])
        del argv[i:i + 2]
    if not argv:
        sys.exit(__doc__)
    bad = False
    for f in map(Path, argv):
        md = f.read_text(encoding="utf-8")
        print(f"== {f}")
        tp = text_override
        if tp is None:
            m = re.search(r"text:\s*(text/[^\s·|]+\.txt)", md)
            vol = f.parent.parent
            tp = vol / m.group(1) if m else None
        if tp is None or not tp.exists():
            print(f"  no text found (header 'text: text/<slug>.txt' missing or wrong) - use --text")
            bad = True
        else:
            res = check_anchors(md.splitlines(), load_text(tp))
            for ln, status, q, near in res:
                if status != "FOUND":
                    print(f"  {status:8} line {ln}: \"{q}\"")
                    if near:
                        print(f"           text has: {near}")
            counts = {s: sum(r[1] == s for r in res) for s in ("FOUND", "CLOSE", "MISSING")}
            print(f"  anchors: {len(res)} checked — {counts['FOUND']} found, {counts['CLOSE']} close, "
                  f"{counts['MISSING']} missing")
            bad |= counts["MISSING"] > 0
        if f.parent.name == "cards":
            probs, length = check_card(md)
            for p in probs:
                print(f"  CARD     {p}")
            print(f"  {length}")
            bad |= bool(probs)
        if online:
            print("\n".join(check_dois(md)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
