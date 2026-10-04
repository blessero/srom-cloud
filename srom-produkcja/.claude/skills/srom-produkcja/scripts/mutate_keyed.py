#!/usr/bin/env python3
"""Mutation test of a keyed file: does `check.py --keyed` catch keying errors in THIS text?

    python3 mutate_keyed.py original.md keyed.md --refs refs.json [--refs more.json] [--max 40]

Makes mutants of keyed.md, each with one error a keyer could make, and runs `check.py --keyed original.md <mutant>`
on each; every mutant must fail. Mutations, taken from the citations in the notes:
  page+1   a page locator changed ("s. 40" -> "s. 41")
  nopage   a page locator dropped ("[@key, s. 40]" -> "[@key]")
  drop     one work dropped from a citation of several ("[@a; @b]" -> "[@b]")
  swap     a key replaced by another work's key whose author the original note does not name
Prints one line per mutant the check let through (MISSED …) and `MUTATIONS CAUGHT n/m`; exit 0 only if all were
caught. A missed mutant is a hole in the check for this text's citation style — fix check.py (with a test) or, if the
two works cannot be told apart from the original note (same author, same title opening), say so in the queries.
Run once per text after `check.py --keyed` says CHECK OK (SKILL.md step 4b); ~3 s per mutant."""
import argparse, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CITE = re.compile(r"\[(?:[^\[\]]|\{[^{}]*\})*?@[\w:.-]+(?:[^\[\]]|\{[^{}]*\})*\]")
KEY = re.compile(r"@([\w:.-]+)")
LOC = re.compile(r",\s?s\.\s?(\d+)")


def notes(text):
    """(label, start, end) of each note definition"""
    out = []
    for m in re.finditer(r"^\[\^([^\]]+)\]:", text, re.M):
        end = text.find("\n\n", m.end())
        out.append((m.group(1), m.start(), len(text) if end < 0 else end))
    return out


def note_of(nts, pos):
    return next((lab for lab, a, b in nts if a <= pos < b), "text")


def mutants(text, refs, orig_notes):
    out = []
    nts = notes(text)
    keys = sorted(refs)
    for m in CITE.finditer(text):
        lab, c, s0 = note_of(nts, m.start()), m.group(0), m.start()
        for lm in LOC.finditer(c):
            a, b = s0 + lm.start(1), s0 + lm.end(1)
            out.append(("page+1", lab, a, b, str(int(lm.group(1)) + 1)))
            end = c.find(";", lm.end())
            end = len(c) - 1 if end < 0 else end
            out.append(("nopage", lab, s0 + lm.start(), s0 + end, ""))
        parts = c[1:-1].split(";")                       # srom-md: no ";" inside braces
        if len(parts) > 1:
            for k in range(len(parts)):
                rest = ";".join(parts[:k] + parts[k + 1:]).strip()
                out.append(("drop", lab, s0, m.end(), "[" + rest + "]"))
        onote = orig_notes.get(lab, "").casefold()
        for km in KEY.finditer(c):
            other = next((k for k in keys[keys.index(km.group(1)) + 1:] + keys
                          if k != km.group(1) and not any((p.get("family") or p.get("literal") or "").casefold()[:5] in onote
                                                          for p in (refs[k].get("author") or refs[k].get("editor") or [])
                                                          if (p.get("family") or p.get("literal")))), None)
            if other:
                out.append(("swap", lab, s0 + km.start(1), s0 + km.end(1), other))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("original"); ap.add_argument("keyed")
    ap.add_argument("--refs", action="append", required=True)
    ap.add_argument("--max", type=int, default=40, help="at most this many mutants, spread over the text")
    a = ap.parse_args()
    text = open(a.keyed, encoding="utf-8").read()
    otext = open(a.original, encoding="utf-8").read()
    orig_notes = {lab: otext[s:e] for lab, s, e in notes(otext)}
    refs = {}
    for p in a.refs:
        refs.update({r["id"]: r for r in json.load(open(p, encoding="utf-8"))})
    ms = mutants(text, refs, orig_notes)
    if len(ms) > a.max:                                  # spread: every kind, evenly over the text
        step = len(ms) / a.max
        ms = [ms[int(i * step)] for i in range(a.max)]
    tmp, caught = tempfile.mkdtemp(), 0
    refargs = [x for p in a.refs for x in ("--refs", p)]
    for kind, lab, s, e, new in ms:
        mut = text[:s] + new + text[e:]
        path = os.path.join(tmp, "mutant.md")
        open(path, "w", encoding="utf-8").write(mut)
        r = subprocess.run([sys.executable, os.path.join(HERE, "check.py"), "--keyed", a.original, path, *refargs],
                           capture_output=True, text=True)
        if r.returncode != 0:
            caught += 1
        else:
            ctx = text[max(0, s - 30):e + 10].replace("\n", " ")
            print(f"MISSED note {lab} [{kind}]: …{ctx}… -> {new!r}")
    print(f"MUTATIONS CAUGHT {caught}/{len(ms)}")
    sys.exit(0 if caught == len(ms) else 1)


if __name__ == "__main__":
    main()
