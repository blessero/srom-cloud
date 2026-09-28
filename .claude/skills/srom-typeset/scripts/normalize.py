#!/usr/bin/env python3
"""
normalize.py — deterministic typographic normalisation of SROM-MD (kanon §3, §4.1, §7.1).

Only UNAMBIGUOUS transformations are applied; every change is logged (line, rule, before → after).
Anything that needs judgement is reported as FLAG and left untouched.
Idempotent: a second run must report 0 changes.

Usage:
    python3 normalize.py in.md -o out.md --log normalize_log.md
"""
import argparse
import re
import sys

UP = "A-ZĄĆĘŁŃÓŚŹŻ"
LO = "a-ząćęłńóśźż"
PH_OPEN, PH_CLOSE = "\ue000", "\ue001"

# abbreviations after which a note marker stays AFTER the period (kanon §7.1)
ABBR_END = {"r", "w", "s", "t", "z", "nr", "k", "itd", "itp", "in", "n", "tzw", "np", "ok", "wyd", "red",
            "tłum", "oprac", "cz", "sygn", "zesp", "tabl", "il", "ur", "zm", "ob", "l", "d", "op", "f", "ark", "zv",
            "wg", "m.in", "p.n.e", "n.e", "jw", "etc", "al", "ds", "hab", "dr", "prof", "ks", "św", "gen", "płk"}

MASKS = [
    re.compile(r"<!--.*?-->", re.S),                               # editor comments
    re.compile(r"https?://[^\s\]\)>]+"),                          # URLs
    re.compile(r"\b10\.\d{4,9}/[^\s\]\)>]+"),                     # DOIs
    re.compile(r"ISBN[\s:]*[\dX][\d\- X]{8,16}[\dX]"),            # ISBNs
    re.compile(r"(?<=\])\{[^{}\n]*\}"),                             # [span]{attrs}
    re.compile(r"(?<![\w@])@[\w:.#$%&\-+?<>~/]*\w"),                # citation keys
    re.compile(r"`[^`\n]*`"),                                       # code
]


class Normalizer:
    def __init__(self):
        self.log = []      # (line, rule, before, after)
        self.flags = []    # (line, rule, excerpt)

    # ---------------------------------------------------------------- masking
    def mask(self, s):
        store = []

        def rep(m):
            store.append(m.group(0))
            return f"{PH_OPEN}{len(store) - 1}{PH_CLOSE}"
        for rx in MASKS:
            s = rx.sub(rep, s)
        return s, store

    @staticmethod
    def unmask(s, store):
        return re.sub(PH_OPEN + r"(\d+)" + PH_CLOSE, lambda m: store[int(m.group(1))], s)

    # ---------------------------------------------------------------- helpers
    def sub(self, rule, rx, repl, s, ln, flags=0):
        def wrap(m):
            new = m.expand(repl) if isinstance(repl, str) else repl(m)
            if new != m.group(0):
                self.log.append((ln, rule, m.group(0), new))
            return new
        return re.sub(rx, wrap, s, flags=flags)

    def flag(self, ln, rule, excerpt):
        self.flags.append((ln, rule, excerpt.strip()[:90]))

    # ---------------------------------------------------------------- quotes
    OPEN_CTX = set(" \t([{–—/\u00a0" + PH_CLOSE)

    def quotes(self, s, ln):
        dq = "\"“”„‟«»"
        idx = [i for i, ch in enumerate(s) if ch in dq]
        if not idx:
            return s
        roles = []
        for i in idx:
            ch = s[i]
            prev = s[i - 1] if i > 0 else " "
            nxt = s[i + 1] if i + 1 < len(s) else " "
            if ch in "„‟":
                role = "o"
            elif prev in self.OPEN_CTX or (prev in dq and roles and roles[-1] == "o"):
                role = "o"
            elif nxt.isspace() or nxt in ".,;:!?)]–…*_" or nxt in dq or nxt in "[" + PH_OPEN or i + 1 == len(s):
                role = "c"
            elif prev in "*_":
                role = "o"
            else:
                role = "?"
            roles.append(role)
        if "?" in roles:
            self.flag(ln, "QUOTE-AMBIG", s[max(0, idx[roles.index('?')] - 30): idx[roles.index('?')] + 30])
            return s
        depth, out, ok = 0, [], True
        for r in roles:
            if r == "o":
                depth += 1
                if depth > 2:
                    ok = False
                out.append("„" if depth == 1 else "»")
            else:
                if depth == 0:
                    ok = False
                    break
                out.append("”" if depth == 1 else "«")
                depth -= 1
        if not ok or depth != 0:
            self.flag(ln, "QUOTE-UNBALANCED", s)
            return s
        chars = list(s)
        for i, new in zip(idx, out):
            if chars[i] != new:
                self.log.append((ln, "QUOTE", chars[i], new))
                chars[i] = new
        return "".join(chars)

    # ---------------------------------------------------------------- per line
    def line(self, raw, ln, in_note):
        s, store = self.mask(raw)
        lead = re.match(r"^[ \t]*", s).group(0)
        body = s[len(lead):]

        # whitespace
        body = self.sub("ZW", r"[\u200b\u200c\u200d\ufeff\u00ad]", "", body, ln)
        body = self.sub("NBSP", r"[\u00a0\u2007\u2009\u202f\t]", " ", body, ln)
        body = self.sub("SPACES", r"(?<=\S) {2,}", " ", body, ln)
        body = self.sub("TRAIL", r" +$", "", body, ln)

        # ellipsis and omissions (§3.5, §4.1)
        # English spaced dots (". . .", ". . . ." at a sentence end) mark an omission in a quotation -> […] (logged: check)
        body = self.sub("OMISSION-SPACED", r"(?<=\S)\. \. \. \.(?= |$)", ". […]", body, ln)     # full stop + omission
        body = self.sub("OMISSION-SPACED", r" ?(?<!\[)\. \. \.(?= |$|[,;:!?”’)])", " […]", body, ln)
        body = self.sub("ELLIPSIS", r"\.\.\.", "…", body, ln)
        body = self.sub("OMISSION", r"[\(\[]\s*…\s*[\)\]]", "[…]", body, ln)

        # quotes (§3.1)
        body = self.quotes(body, ln)

        # dashes (§3.2)
        body = self.sub("EMDASH-RANGE", r"(?<=\d)\s*—\s*(?=\d)", "–", body, ln)
        body = self.sub("EMDASH", r"^—\s*|\s*—\s*", lambda m: "– " if m.start() == 0 else " – ", body, ln)
        body = self.sub("HYPHEN-PAUSE", r"(?<=\S) - (?=\S)", " – ", body, ln)
        # unspaced digit-digit: range, except postal-code shape NN-NNN (flag)
        for m in re.finditer(r"(?<![\w/.\-–])\d{2}-\d{3}(?![\w/.\-–])", body):
            self.flag(ln, "POSTCODE-OR-RANGE", m.group(0))
        body = self.sub("RANGE", r"(?<![\w/.\-–])(\d{1,4})-(\d{1,4})(?![\w/.\-–])",
                        lambda m: m.group(0) if re.fullmatch(r"\d{2}-\d{3}", m.group(0)) else f"{m.group(1)}–{m.group(2)}",
                        body, ln)
        # spaced range only in unambiguous contexts: page/folio labels, or year–year
        body = self.sub("RANGE-SPACED", r"(\b(?:s|k|l|ark)\. \d{1,4}) ?[–-] ?(\d{1,4})\b", r"\1–\2", body, ln)
        body = self.sub("RANGE-YEARS", r"\b((?:1[5-9]|20)\d{2}) [–-] ((?:1[5-9]|20)\d{2})\b", r"\1–\2", body, ln)
        # abbreviated range written in full (Kanon § 3.2): 214–31 -> 214–231, 1544–45 -> 1544–1545 (logged)
        body = self.sub("RANGE-FULL", r"(?<![\w/.\-–])(\d{2,4})–(\d{1,3})(?![\w/\-–]|\.\d)",
                        lambda m: m.group(1) + "–" + m.group(1)[:len(m.group(1)) - len(m.group(2))] + m.group(2)
                        if len(m.group(2)) < len(m.group(1)) and int(m.group(1)[:len(m.group(1)) - len(m.group(2))] + m.group(2)) > int(m.group(1))
                        else m.group(0), body, ln)
        for m in re.finditer(rf"[{LO}]–[{LO}]", body):
            self.flag(ln, "ENDASH-IN-WORD", body[max(0, m.start() - 20): m.end() + 20])
        if not in_note and re.match(r"[–—] ", body):
            self.flag(ln, "DASH-PARAGRAPH", body[:60])

        # spaces around punctuation/brackets
        body = self.sub("SPACE-BEFORE-PUNCT", r"(?<=\S) +(?=[,.;:!?)\]”«])", "", body, ln)
        body = self.sub("SPACE-AFTER-OPEN", r"([(\[„»]) +", r"\1", body, ln)

        # note markers / citations: after closing quote or paren, before . , ; : (§4.1, §7.1)
        mark = r"(\[\^[^\]\s]+\]|\[[^\[\]]*" + PH_OPEN + r"\d+" + PH_CLOSE + r"[^\[\]]*\])"
        body = self.sub("MARK-AFTER-QUOTE", mark + r"([”«)])", r"\2\1", body, ln)

        def move(m):
            word, punct, mk = m.group(1), m.group(2), m.group(3)
            core = re.sub(r"^.*?([\w.]+)$", r"\1", word)
            if punct == "." and core.lower().rstrip(".") in ABBR_END:
                return m.group(0)
            if punct == "." and re.fullmatch(rf"[{UP}]", core):
                return m.group(0)  # initial
            return f"{word}{mk}{punct}"
        body = self.sub("MARK-BEFORE-PUNCT", r"(\S+?)([.,;:])" + mark, move, body, ln)
        # main text only: a citation typed after the sentence punctuation would put the note marker after it.
        # In notes "; [@b]" and the definition head "[^1]: [@a]" are normal.
        for m in (re.finditer(r"[.;:] " + mark, body) if not in_note else ()):
            self.flag(ln, "CITE-AFTER-PUNCT", self.unmask(body[max(0, m.start() - 30): m.end()], store))
        for m in re.finditer(r"\[\^[^\]\s]+\]\[\^[^\]\s]+\]", body):
            self.flag(ln, "DOUBLE-MARKER", m.group(0))

        # initials without space (§7.2)
        body = self.sub("INITIALS", rf"\b([{UP}])\. (?=[{UP}]\.)", r"\1.", body, ln)

        # apparatus labels (notes only; never touch quotations in body text)
        if in_note:
            body = self.sub("LABEL-STR", r"\bstr\. ", "s. ", body, ln)
            body = self.sub("LABEL-SS", r"\bss\. ", "s. ", body, ln)
            body = self.sub("LABEL-PRZEL", r"\bprzeł\. ", "tłum. ", body, ln)
            body = self.sub("LABEL-W", r"\[w:\]", "w:", body, ln)
            body = self.sub("LABEL-IBID", r"\b[Ii]bid\.(?=[\s,])", "*Ibidem*", body, ln)
            if re.search(r"\b(?:op\.\s*cit|dz\.\s*cyt|tamże|tenże|taż|idem|eadem)\b", body, re.I):
                self.flag(ln, "BACKREF-FORBIDDEN", body[:90])

        # apostrophe between letters in body text -> ’ ; in notes only flag (may be ALA-LC soft sign ʹ)
        if in_note:
            for m in re.finditer(rf"[{LO}{UP}]'[{LO}{UP}]", body):
                self.flag(ln, "APOSTROPHE-OR-SOFTSIGN", body[max(0, m.start() - 20): m.end() + 20])
        else:
            body = self.sub("APOSTROPHE", rf"(?<=[{LO}{UP}])'(?=[{LO}{UP}])", "’", body, ln)

        return self.unmask(lead + body, store)

    def run(self, text):
        lines = text.split("\n")
        out, in_yaml, in_def, fence = [], False, False, None
        for n, raw in enumerate(lines, 1):
            # fenced blocks (interlinear examples, kanon §5.3) are verbatim: alignment spaces must survive
            fm = re.match(r"^\s*(`{3,}|~{3,})", raw)
            if fence is None and fm:
                fence = fm.group(1)
                out.append(raw)
                continue
            if fence is not None:
                out.append(raw)
                if raw.strip().startswith(fence):
                    fence = None
                continue
            if n == 1 and raw.strip() == "---":
                in_yaml = True
                out.append(raw)
                continue
            if in_yaml:
                out.append(raw)
                if raw.strip() in ("---", "..."):
                    in_yaml = False
                continue
            if raw.startswith(":::"):
                out.append(raw)
                continue
            if re.match(r"\[\^[^\]]+\]:", raw):
                in_def = True
            elif raw.strip() and not raw.startswith("    "):
                in_def = False
            in_note = in_def or "^[" in raw
            out.append(self.line(raw, n, in_note) if raw.strip() else "")
        return "\n".join(self.note_fullstop(out))

    def note_fullstop(self, out):
        """a note ends with a full stop (…, ?, ! count; so does one inside a closing quote): an obvious slip in the
        source ("…: Mills, 3") is corrected and logged"""
        ends = []                          # index of the last non-empty line of each note
        cur = None
        for i, raw in enumerate(out):
            if re.match(r"\[\^[^\]]+\]:", raw):
                if cur is not None:
                    ends.append(cur)
                cur = i
            elif cur is not None and raw.strip():
                if raw.startswith("    "):
                    cur = i
                else:
                    ends.append(cur)
                    cur = None
        if cur is not None:
            ends.append(cur)
        for i in ends:
            t = out[i].rstrip()
            core = t.rstrip("”’»«)]*_")
            if core and core[-1] not in ".!?…" and not t.endswith("-->"):
                self.log.append((i + 1, "NOTE-FULLSTOP", t[-30:], t[-30:] + "."))
                out[i] = t + "."
        return out

    def report(self):
        r = [f"# normalize.py — {len(self.log)} change(s), {len(self.flags)} flag(s)", ""]
        by = {}
        for ln, rule, a, b in self.log:
            by.setdefault(rule, 0)
            by[rule] += 1
        r.append("## Changes by rule")
        r += [f"- {k}: {v}" for k, v in sorted(by.items())] or ["- none"]
        r += ["", "## Flags (need a decision — text left unchanged)"]
        r += [f"- L{ln} **{rule}**: `{ex}`" for ln, rule, ex in self.flags] or ["- none"]
        r += ["", "## Change log"]
        r += [f"- L{ln} {rule}: `{a}` → `{b}`" for ln, rule, a, b in self.log]
        return "\n".join(r) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--log", required=True)
    a = ap.parse_args()
    text = open(a.src, encoding="utf-8").read()
    nz = Normalizer()
    res = nz.run(text)
    open(a.out, "w", encoding="utf-8").write(res)
    open(a.log, "w", encoding="utf-8").write(nz.report())
    print(f"normalize: {len(nz.log)} changes, {len(nz.flags)} flags -> {a.log}")


if __name__ == "__main__":
    main()
