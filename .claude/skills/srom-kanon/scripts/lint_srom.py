#!/usr/bin/env python3
"""
lint_srom.py — check a manuscript against the Studia Romologica Kanon (v1.6; references/kanon-redakcyjny.md).

Covers only mechanically detectable rules. The judgment checks in RULES.md §J
still have to be done by reading. WARN items may be legitimate — judge each.

Usage:
    python3 lint_srom.py article.txt              # Polish article (default)
    python3 lint_srom.py article.txt --lang en    # English online version only
    python3 lint_srom.py article.txt --json
    cat article.txt | python3 lint_srom.py -

Exit code 1 if any ERROR was found, else 0.
"""

import argparse
import json
import re
import sys
import unicodedata

ENDASH = "\u2013"
EMDASH = "\u2014"
SUPERSCRIPTS = "\u00b9\u00b2\u00b3\u2074-\u2079\u2070"
ROMAN_MONTH = r"(?:XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)"
YEAR = r"(?:1[5-9]|20)\d{2}"

# (id, severity, pattern, message, langs|None, flags)
RULES = [
    # --- forbidden back-references (§7.3) ---------------------------------
    ("ABBR-OPCIT", "ERROR", r"\bop\.\s*cit\.",
     "op. cit. is forbidden — use the short title: Nazwisko, *Skrócony tytuł…*, s. N.", None, re.I),
    ("ABBR-DZCYT", "ERROR", r"\bdz\.\s*cyt\.",
     "dz. cyt. is forbidden — use the short title.", None, re.I),
    ("ABBR-LOCCIT", "ERROR", r"\bloc\.\s*cit\.",
     "loc. cit. is forbidden — use the short title with a locator.", None, re.I),
    ("ABBR-IDEM", "ERROR", r"\b(?:idem|eadem|iidem|eaedem)\b",
     "idem/eadem are forbidden — repeat the surname.", None, re.I),
    ("ABBR-TENZE", "ERROR", r"\b(?:tenże|taż|ciż)\b",
     "tenże/taż are forbidden — repeat the surname.", None, re.I),
    ("ABBR-TAMZE", "ERROR", r"\btamże\b",
     "tamże is forbidden — the only cross-reference is *Ibidem*.", None, re.I),
    ("ABBR-STR", "ERROR", r"\bstr\.",
     "str. is not used — the page abbreviation is s.", None, re.I),
    ("ABBR-IBID", "WARN", r"\bibid\.",
     "Use the full form *Ibidem*, italic.", None, re.I),
    ("ABBR-VIDE", "WARN", r"\b(?:vide\b|cf\.|etc\.)",
     "vide / cf. / etc. are not used — zob., por.", None, re.I),

    # --- labels (§7.2, §12) -----------------------------------------------
    ("W-BRACKETS", "ERROR", r"\[(?:w|in):\]",
     "w: (PL) / in: (EN) without square brackets.", None, 0),
    ("TRANSLATOR", "ERROR", r"\bprzeł\.",
     "Translator label is tłum.", ["pl"], 0),
    ("LABEL-FOREIGN", "ERROR", r"\bHrsg\.|\béd\.|\bsous la dir\.|под\s+ред\.",
     "Apparatus labels are always Polish (red.), whatever the cited work's language.", None, 0),
    ("LABEL-EN-IN-PL", "WARN", r"\((?:eds?)\.\)|\bed\.\s+[A-ZŁŚŻŹĆŃÓ]\.|\btrans\.\s|\bet al\.",
     "English label in a Polish article — red., tłum., i in.", ["pl"], 0),
    ("ROMAN-EDVOL", "ERROR", r"\b(?:wyd|t|z)\.\s*[IVXLC]+\b",
     "Editions, volumes, issues take arabic numerals: wyd. 3, t. 2, z. 2.", None, 0),

    # --- dates (§3.5) -----------------------------------------------------
    ("DATE-ROMAN-MONTH", "ERROR", r"\b\d{1,2}\s+" + ROMAN_MONTH + r"\s+" + YEAR + r"\b",
     "Apparatus dates are dd.mm.rrrr (04.03.1937); body dates in words.", None, 0),
    ("DATE-UNPADDED", "WARN", r"(?<![\d.])(?:\d\.\d{1,2}|\d{1,2}\.\d)\." + YEAR + r"\b",
     "Zero-pad day and month: 04.03.1937.", None, 0),
    ("DATE-R-AFTER", "WARN", r"\b\d{2}\.\d{2}\." + YEAR + r"\s*r\.",
     "No r. after a numeric date: 04.03.1937.", None, 0),
    ("ACCESS-DATE", "ERROR",
     r"\[(?:dostęp|accessed):(?!\s\d{2}\.\d{2}\.\d{4}\])[^\]]*\]",
     "Access date format: [dostęp: 18.03.2025].", None, 0),

    # --- author-date residue ----------------------------------------------
    ("YEARLETTER", "ERROR", r"\b" + YEAR + r"[a-d]\b",
     "Year letters (2012a) belong to author-date systems — remove.", None, 0),
    ("PARENCITE", "WARN",
     r"\([A-ZŁŚŻŹĆŃÓĄĘ][a-ząćęłńóśżź]+,?\s+" + YEAR + r"(?:[,:]\s*s?\.?\s*\d+)?\)",
     "Author-date parenthesis? This journal uses footnotes. (Ignore if it is a place-year in prose.)", None, 0),

    # --- journal and imprint (§7.2, §9) -----------------------------------
    ("JOURNAL-COMMA", "ERROR", r"[\u201d\"]\s+" + YEAR + r"\b",
     "Comma after the journal title: „Tytuł”, 1947, t. 1, z. 2, s. 310.", None, 0),
    ("BIB-COLON", "ERROR",
     r"\b(?:Kraków|Warszawa|Tarnów|Poznań|Wrocław|Gdańsk|Łódź|Lublin|Katowice|Toruń|"
     r"Olsztyn|Rzeszów|Szczecin|Białystok|Moskva|Kyïv|London|New York|Berlin|Paris|"
     r"Budapest|Praha|Sofiia|Beograd|Wien|Roma|Madrid|Istanbul)\s*:",
     "No colon after place of publication: Wydawnictwo, Miejsce rok.", None, 0),
    ("PLACE-POLONISED", "WARN",
     r"\b(?:Londyn|Nowy Jork|Paryż|Monachium|Filadelfia|Waszyngton|Wiedeń|Rzym|"
     r"Budapeszt|Sztokholm|Stambuł|Genewa|Bruksela|Mediolan|Bukareszt|Kolonia|"
     r"Lipsk|Moskwa|Kijów|Sankt Petersburg|Mińsk|Sofia|Belgrad)\s+" + YEAR + r"\b",
     "Imprint place as on the title page, not Polonised (London; Moskva). Ignore in body prose.", None, 0),
    ("BIB-DOIURL", "WARN", r"https?://(?:dx\.)?doi\.org/",
     "In print, DOI as `DOI: 10.xxxx/yyyy`, without the https://doi.org/ prefix.", None, 0),

    # --- Cyrillic (§9.6) --------------------------------------------------
    ("CYRILLIC", "WARN", r"[\u0400-\u04FF]{2,}",
     "Cyrillic script: body → Polish transcription (PWN/KSNG); apparatus → ALA-LC.", None, 0),
    ("TIEBAR", "ERROR", "\u0361",
     "ALA-LC without tie-bars: ts, iu, ia.", None, 0),
    ("ISO9-SCIRC", "ERROR", "\u015d",
     "ŝ is ISO 9 (щ) — ALA-LC uses shch (sht in Bulgarian).", None, 0),
    ("ISO9-VOWELS", "WARN", r"[\u00e2\u00fb\u00ea]",
     "â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.", None, 0),

    # --- dashes, ellipses, ranges (§3) ------------------------------------
    ("RANGE-HYPHEN", "ERROR", r"(?:\bs\.\s*\d+\s*-\s*\d+|\b" + YEAR + r"\s*-\s*" + YEAR + r"\b)",
     "Ranges take an unspaced en dash: s. 15–20, 1939–1945.", None, 0),
    ("RANGE-SHORT", "WARN",
     r"(?:\bs\.\s*\d{3,}" + ENDASH + r"\d{1,2}\b|\b" + YEAR + ENDASH + r"\d{2}\b)",
     "Elided range — write both numbers in full: s. 115–128, 1939–1945.", None, 0),
    ("EMDASH", "ERROR", EMDASH, "Em dash is not used — en dash.", ["pl"], 0),
    ("ELLIPSIS-DOTS", "ERROR", r"(?<!\.)\.\.\.(?!\.)",
     "Use the single character … ; omissions in quotes as […].", None, 0),
    ("OMISSION-ROUND", "ERROR", r"\(\s*(?:\.\.\.|\u2026)\s*\)",
     "Omissions in quotations: […], never (...).", None, 0),

    # --- quotation marks (§3.1) -------------------------------------------
    ("QUOTE-STRAIGHT", "ERROR", r"\"",
     "Straight quote — use „ ”. (If it stands for a hard sign, use ʺ U+02BA.)", None, 0),
    ("QUOTE-EN-IN-PL", "WARN", "\u201c",
     "English opening quote in a Polish article — use „ ”.", ["pl"], 0),
    ("QUOTE-PL-IN-EN", "WARN", "\u201e",
     "Polish opening quote in the English version — use \u201c\u201d.", ["en"], 0),

    # --- note marker (§7.1) -----------------------------------------------
    # Allowed after an abbreviation's own period: r. w. s. t. z. k. i in. itd. itp.
    ("NOTE-AFTERDOT", "ERROR",
     r"(?<![\s\u00a0][rwstzk])(?<!\bin)(?<!itd)(?<!itp)\.\s*(?:[" + SUPERSCRIPTS + r"]|\[\d{1,3}\])",
     "Note marker goes before the closing period.", None, 0),
    ("NOTE-BEFOREQUOTE", "WARN", r"[" + SUPERSCRIPTS + r"]\s*[\u201d\u201c]",
     "Note marker goes after the closing quotation mark.", None, 0),

    # --- spacing ----------------------------------------------------------
    ("SPACE-DOUBLE", "WARN", r"(?<=\S) {2,}(?=\S)",
     "Multiple spaces — single space.", None, 0),
    ("SPACE-BEFOREPUNCT", "ERROR", r"(?<=\w)\s+[,;:.!?](?=\s|$)",
     "Space before punctuation.", None, 0),
]

NEEDS_RAW = {"BIB-DOIURL"}          # must see URLs
SEVERITY_ORDER = {"ERROR": 0, "WARN": 1}

COMPILED = [(rid, sev, re.compile(pat, flags), msg, langs)
            for rid, sev, pat, msg, langs, flags in RULES]


def mask_urls(line):
    """Same-length placeholder: keeps columns, avoids fake matches inside URLs."""
    return re.sub(r"https?://[^\s\]]+", lambda m: "U" * len(m.group(0)), line)


def find_issues(text, lang):
    issues = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        masked = mask_urls(raw)
        for rid, sev, rx, msg, langs in COMPILED:
            if langs and lang not in langs:
                continue
            line = raw if rid in NEEDS_RAW else masked
            for m in rx.finditer(line):
                issues.append({
                    "line": lineno, "col": m.start() + 1, "rule": rid,
                    "severity": sev, "message": msg,
                    "excerpt": raw[max(0, m.start() - 30):m.end() + 30].strip(),
                })
    return issues


def counts_report(text):
    """Non-positional counts; the editor interprets them by zone (§J)."""
    return {
        "apparatus_year_forms (1943 r.)": len(re.findall(r"\b\d{4}\s*r\.", text)),
        "prose_year_forms (1943 roku)": len(re.findall(r"\b\d{4}\s+rok", text)),
        "apparatus_century_forms (XX w.)": len(re.findall(r"\b[IVXLC]+\s*w\.", text)),
        "prose_century_forms (XX wieku)": len(re.findall(r"\b[IVXLC]+\s+wiek", text)),
        "i_in": len(re.findall(r"\bi\s+in\.", text)),
        "ibidem": len(re.findall(r"\bIbidem\b", text)),
        "ascii_apostrophe_inside_word (soft sign?)": len(re.findall(r"[a-z]'[a-z]", text)),
    }


def render_text(issues, counts, path):
    out = [f"SROM canon check — {path}", "=" * 60]
    if not issues:
        out.append("No mechanical issues found.")
    else:
        current = None
        for i in sorted(issues, key=lambda i: (SEVERITY_ORDER[i["severity"]], i["line"], i["col"])):
            if i["severity"] != current:
                current = i["severity"]
                out += ["", f"--- {current} ---"]
            out.append(f"{i['line']}:{i['col']}  [{i['rule']}] {i['message']}")
            if i["excerpt"]:
                out.append(f"        … {i['excerpt']} …")
    out += ["", "--- counts (interpret by zone; RULES.md §J) ---"]
    out += [f"  {k}: {v}" for k, v in counts.items()]
    out += ["", "Not checkable here:",
            "  · Ibidem legality (same page) — proofs.",
            "  · Short-title consistency; note↔bibliography coverage.",
            "  · Metryczki anonymisation — editor's call.",
            "  · Initials in notes / full names in bibliography.",
            "  · Surnames must NOT be capitalised in the CSV.",
            "  · Missing source data: flag it, never reconstruct."]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Check a manuscript against the Studia Romologica canon.")
    ap.add_argument("path", help="file to check, or - for stdin")
    ap.add_argument("--lang", default="pl", choices=["pl", "en"],
                    help="pl (default); en only for the English online version")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    text = unicodedata.normalize("NFC", text)
    issues = find_issues(text, args.lang)
    counts = counts_report(text)

    if args.json:
        print(json.dumps({"file": args.path, "lang": args.lang, "issues": issues, "counts": counts},
                         ensure_ascii=False, indent=2))
    else:
        print(render_text(issues, counts, args.path))
    return 1 if any(i["severity"] == "ERROR" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
