#!/usr/bin/env python3
"""tlumacz-front_check.py — checks <id>_front_pl.md (Polish header data, Kanon § 12.2.2; handoff.md "Back", T11).

Usage: python3 tlumacz-front_check.py <id>_src_front.md <id>_front_pl.md
Last line: FRONT OK  or  FRONT ERRORS n   (exit 0 / 1). Warnings never fail.

Format of <id>_front_pl.md (sections in this order, headings exactly as here):
    # Tytuł           Polish title, no final full stop
    # Podtytuł        Polish subtitle; "—" when the original title has no subtitle
    # Abstrakt        Polish abstract (a translation of the original's)
    # Słowa kluczowe  5–10, "; " between them, no final full stop
    # Keywords        "jak w oryginale" when the original has keywords; otherwise 5–10 English keywords drafted
                      by the translator, followed by the line "<!-- do zatwierdzenia przez autora -->"
The English title and abstract are not repeated: they stay as in the original (Kanon § 12.2.2).
"""
import re, sys

SECTIONS = ["Tytuł", "Podtytuł", "Abstrakt", "Słowa kluczowe", "Keywords"]
APPROVE = "<!-- do zatwierdzenia przez autora -->"


def sections(text):
    out, cur = {}, None
    order = []
    for line in text.splitlines():
        m = re.match(r"^# (.+?)\s*$", line)
        if m:
            cur = m.group(1); order.append(cur); out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return order, {k: "\n".join(v).strip() for k, v in out.items()}


def src_parts(text):
    """Title = first non-empty line; keywords = a line starting 'Keywords' (any case), if any."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0] if lines else ""
    kw = any(re.match(r"^\*?keywords?\b", l, re.I) for l in lines)
    return title, kw


def keywords(v, errors, label):
    if v.endswith("."):
        errors.append(f"{label}: no final full stop (Kanon § 1 pkt 9)")
    items = [k.strip() for k in v.split(";")]
    if any(not k for k in items):
        errors.append(f"{label}: empty item — separator is '; '")
    if not 5 <= len(items) <= 10:
        errors.append(f"{label}: {len(items)} keywords, need 5–10 (Kanon § 1 pkt 9)")
    if "," in v and len(items) < 5:
        errors.append(f"{label}: commas used as separators? (separator is '; ')")


def check(src_text, pl_text):
    errors, warnings = [], []
    order, s = sections(pl_text)
    if order != SECTIONS:
        errors.append(f"sections {order} — expected {SECTIONS}")
        return errors, warnings
    title, src_has_kw = src_parts(src_text)
    has_sub = ":" in title
    if not s["Tytuł"] or "\n" in s["Tytuł"]:
        errors.append("Tytuł: one non-empty line")
    if s["Tytuł"].endswith("."):
        errors.append("Tytuł: no final full stop")
    if has_sub and s["Podtytuł"] in ("", "—"):
        errors.append(f"Podtytuł: the original title has a subtitle ({title!r}) — keep title and subtitle apart")
    if not has_sub and s["Podtytuł"] != "—":
        errors.append("Podtytuł: the original has no subtitle — write '—'")
    if ":" in s["Tytuł"] or "." in s["Tytuł"].rstrip("."):
        warnings.append("Tytuł: contains ':' or '.' — is the subtitle still inside the title?")
    if not s["Abstrakt"]:
        errors.append("Abstrakt: empty")
    elif len(s["Abstrakt"]) > 1000:
        warnings.append(f"Abstrakt: {len(s['Abstrakt'])} characters > 1000 — shortened by the editors (Kanon § 12.2.2)")
    keywords(s["Słowa kluczowe"], errors, "Słowa kluczowe")
    kw = s["Keywords"]
    if src_has_kw:
        if kw != "jak w oryginale":
            errors.append("Keywords: the original has keywords — write 'jak w oryginale' (they stay as the author's)")
    else:
        if APPROVE not in kw:
            errors.append(f"Keywords: the original has none — drafted ones need the line {APPROVE!r}")
        keywords(kw.replace(APPROVE, "").strip(), errors, "Keywords")
    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    e, w = check(open(sys.argv[1], encoding="utf-8").read(), open(sys.argv[2], encoding="utf-8").read())
    for x in w: print("warning:", x)
    for x in e: print("error:", x)
    print("FRONT OK" if not e else f"FRONT ERRORS {len(e)}")
    sys.exit(1 if e else 0)
