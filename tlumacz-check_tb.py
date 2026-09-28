#!/usr/bin/env python3
"""tlumacz-check_tb.py — integrity checks for the srom-tlumacz termbase.

  --schema     header columns vs. fields defined in the schema doc (both directions)
  --shape      every row has all columns; concept_id unique and well-formed; HOUSE rows dated;
               pl_house empty only for OPEN; an English form shared by two rows needs `sense` in both
  --vocab      controlled values in domain / status / pl_standing
  --precedent  every «quote» cited for SRom 18/2025 occurs in the vol. 18 text (whitespace-normalised);
               the cited line is informative only — a moved line is a WARN, a missing quote an error.
               Two cite forms: `l. N: «…»` (old text extraction) and `md <art>: «…»` (clean text,
               sources/vol18-md/<art>_pl.md, from leaf 1.3.1)
  --evidence   ESTABLISHED rows carry >= 2 sources, or "MB verified dd.mm.yyyy" (MB's own survey);
               every `TR <key>: «…»` quote occurs in the training file named for <key> in
               training/sources.tsv (whitespace-normalised); every CANDIDATE row has at least one (leaf 1.3.5)
  --selftest   corrupts temporary copies and confirms each check above fails on them

Paths resolved by tlumacz_paths.py (./, sources/, ../sources, ../_shared, /mnt/project); override with
--tb-file, --schema-file, --v18-file. Exit 1 on any failure.
"""
import re, argparse, csv, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


sys.path.insert(0, HERE)
from tlumacz_paths import source as _source


def locate(name, override, *alts):
    if override:
        return override
    return _source(name, *alts) or os.path.join(HERE, name)


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\r", "")).strip()


def load_tb(path):
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        rows = list(r)
    header, body = rows[0], [x for x in rows[1:] if any(c.strip() for c in x)]
    return header, body


def schema_fields(text):
    block = text.split("## Fields", 1)[1].split("\n### ", 1)[0]
    return re.findall(r"^\| `([a-z_]+)` \|", block, flags=re.M)


def vocab(text, name):
    block = text.split(f"### `{name}`", 1)[1].split("\n#", 1)[0]
    if name == "domain":
        line = [l for l in block.splitlines() if "·" in l][0]
        return {v.strip() for v in line.split("·")}
    return set(re.findall(r"^- \*\*([A-Z-]+)\*\*", block, flags=re.M))


def run_checks(a):
    header, raw = load_tb(a.tb_file)
    schema = open(a.schema_file, encoding="utf-8").read()
    ok = True
    width_ok = all(len(r) == len(header) for r in raw)
    rows = [dict(zip(header, r)) for r in raw if len(r) == len(header)]

    if a.schema:
        fields = schema_fields(schema)
        d = sum(c in fields for c in header); p = sum(f in header for f in fields)
        print(f"columns: {d}/{len(header)} defined; schema fields: {p}/{len(fields)} present")
        for c in header:
            if c not in fields: print("  undefined column:", c)
        for f in fields:
            if f not in header: print("  missing column:", f)
        ok &= d == len(header) and p == len(fields)

    if a.shape:
        errs = []
        for i, r in enumerate(raw, 2):
            if len(r) != len(header):
                errs.append(f"line {i}: {len(r)} fields, header has {len(header)}")
        ids = [r.get("concept_id", "") for r in rows]
        for cid in sorted({x for x in ids if ids.count(x) > 1}):
            errs.append(f"duplicate concept_id {cid}")
        for r in rows:
            cid = r.get("concept_id", "")
            if not re.fullmatch(r"C-\d{4}", cid): errs.append(f"malformed concept_id {cid!r}")
            if r.get("status") == "HOUSE" and not re.match(r"\d{2}\.\d{2}\.\d{4} ", r.get("decided", "")):
                errs.append(f"{cid}: HOUSE without dated decision")
            if not r.get("pl_house") and r.get("status") != "OPEN":
                errs.append(f"{cid}: empty pl_house on a non-OPEN row")
        forms = {}
        for r in rows:
            for v in {x.strip().lower() for x in r.get("en_variants", "").split(" | ") if x.strip()}:
                forms.setdefault(v, []).append(r)
        for v, rs in forms.items():
            if len(rs) > 1 and any(not x.get("sense", "").strip() for x in rs):
                errs.append(f"English form {v!r} shared by {', '.join(x['concept_id'] for x in rs)} without `sense` on each")
        for e in errs: print("  " + e)
        print(f"shape: {len(raw)} rows, {len(errs)} problem(s)")
        ok &= not errs and width_ok

    if a.vocab:
        bad = [(r["concept_id"], c, r.get(c)) for c in ("domain", "status", "pl_standing")
               for r in rows if r.get(c) not in vocab(schema, c)]
        for b in bad: print("  invalid:", *b)
        print("vocab: all rows valid" if not bad else f"vocab: {len(bad)} invalid value(s)")
        ok &= not bad

    if a.precedent:
        if not os.path.exists(a.v18_file):
            print("precedent: vol. 18 text not found at", a.v18_file); return False
        text = open(a.v18_file, encoding="utf-8", errors="replace").read().replace("\r", "")
        flat, lines = norm(text), text.split("\n")
        house18 = [r for r in rows if r["status"] == "HOUSE" and "SRom 18/2025" in r["precedent"]]
        verified = 0
        for r in house18:
            cites = re.findall(r"l\. (\d+): «(.+?)»", r["precedent"])
            mdcites = re.findall(r"md (\w+): «(.+?)»", r["precedent"])
            good = bool(cites or mdcites)
            for art, q in mdcites:
                f = os.path.join(os.path.dirname(a.v18_file), "vol18-md", f"{art}_pl.md")
                if not os.path.exists(f):
                    f = os.path.join(HERE, "sources", "vol18-md", f"{art}_pl.md")
                if not (os.path.exists(f) and norm(q) in norm(open(f, encoding="utf-8").read())):
                    good = False; print(f"  {r['concept_id']}: quote not found in {art}_pl.md: «{q}»")
            for n, q in cites:
                if norm(q) not in flat:
                    good = False; print(f"  {r['concept_id']}: quote not found: «{q}»")
                else:
                    n = int(n)
                    if not (0 < n <= len(lines) and q in lines[n - 1]):
                        where = next((i + 1 for i, l in enumerate(lines) if q in l), "spans lines")
                        print(f"  WARN {r['concept_id']}: «{q}» cited at l. {n}, found at l. {where}")
            verified += good
        print(f"precedent verified: {verified}/{len(house18)}")
        ok &= bool(house18) and verified == len(house18)

    if a.evidence:
        est = [r for r in rows if r["pl_standing"] == "ESTABLISHED"]
        short = [r["concept_id"] for r in est
                 if len([s for s in r["evidence"].split(" | ") if s.strip()]) < 2
                 and not re.search(r"^MB verified \d{2}\.\d{2}\.\d{4}$", r["evidence"].strip())]
        if short:
            print("  fewer than 2 sources:", *short)
        print(f"established rows: {len(est)}, all with >=2 sources" if not short
              else f"established rows: {len(short)} under-evidenced")
        ok &= not short

        tdir = os.path.join(os.path.dirname(os.path.abspath(a.tb_file)), "training")
        if not os.path.isfile(os.path.join(tdir, "sources.tsv")):
            tdir = os.path.join(HERE, "training")
        tfiles = {}
        if os.path.isfile(os.path.join(tdir, "sources.tsv")):
            with open(os.path.join(tdir, "sources.tsv"), encoding="utf-8") as f:
                for rec in csv.DictReader(f, delimiter="\t"):
                    tfiles[rec["key"]] = os.path.join(tdir, rec["file"])
        texts, n_q, bad_q = {}, 0, []
        for r in rows:
            for key, q in re.findall(r"TR (\w+): «(.+?)»", r["evidence"]):
                n_q += 1
                if key not in texts:
                    fp = tfiles.get(key)
                    texts[key] = norm(open(fp, encoding="utf-8").read()) if fp and os.path.isfile(fp) else None
                if texts[key] is None or norm(q) not in texts[key]:
                    bad_q.append(f"{r['concept_id']}: TR {key}: «{q}»")
        for b in bad_q: print("  training quote not found:", b)
        print(f"training quotes verified: {n_q - len(bad_q)}/{n_q}")
        cand = [r for r in rows if r["status"] == "CANDIDATE"]
        bare = [r["concept_id"] for r in cand if not re.search(r"TR \w+: «.+?»", r["evidence"])]
        if bare: print("  CANDIDATE rows without a training quote:", *bare)
        print(f"candidate rows: {len(cand)}, each with a verified training quote" if not (bare or bad_q)
              else f"candidate rows: {len(bare)} without a quote, {len(bad_q)} quote(s) not found")
        ok &= not bad_q and not bare
    return ok


def selftest(a):
    """Each corruption must make its check fail (exit 1)."""
    cases = [
        ("--schema", lambda h, rs: (h[:-1], [r[:-1] for r in rs])),
        ("--shape", lambda h, rs: (h, rs + [rs[0]])),                                  # duplicate id
        ("--shape", lambda h, rs: (h, [rs[0][:5]] + rs[1:])),                           # short row
        ("--shape", lambda h, rs: (h, rs + [["C-9999"] + rs[0][1:]])),                  # shared form, no sense
        ("--vocab", lambda h, rs: (h, [r[:h.index("status")] + ["LOCKED"] + r[h.index("status") + 1:] for r in rs])),
        ("--precedent", lambda h, rs: (h, [[c.replace("«", "«xq") for c in r] for r in rs])),
        ("--evidence", lambda h, rs: (h, [r[:h.index("evidence")] + [""] + r[h.index("evidence") + 1:] for r in rs])),
        ("--evidence", lambda h, rs: (h, [[c.replace("TR taradejna: «", "TR taradejna: «xq") for c in r] for r in rs])),   # training quote altered
        ("--evidence", lambda h, rs: (h, [r[:h.index("evidence")] + [re.sub(r"TR \w+: «.+?»", "", r[h.index("evidence")])]
                                          + r[h.index("evidence") + 1:] for r in rs])),                           # CANDIDATE without quote
    ]
    header, raw = load_tb(a.tb_file)
    caught = 0
    for flag, corrupt in cases:
        d = tempfile.mkdtemp()
        h, rs = corrupt(list(header), [list(r) for r in raw])
        p = os.path.join(d, "tb.tsv")
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join("\t".join(r) for r in [h] + rs) + "\n")
        res = subprocess.run([sys.executable, os.path.abspath(__file__), flag, "--tb-file", p,
                              "--schema-file", a.schema_file, "--v18-file", a.v18_file],
                             capture_output=True, text=True)
        caught += res.returncode == 1
        if res.returncode != 1: print(f"  NOT CAUGHT: {flag}")
        shutil.rmtree(d)
    print(f"selftest: {caught}/{len(cases)} negative controls caught")
    return caught == len(cases)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in ("schema", "shape", "vocab", "precedent", "evidence", "selftest"):
        ap.add_argument("--" + f, action="store_true")
    ap.add_argument("--tb-file"); ap.add_argument("--schema-file"); ap.add_argument("--v18-file")
    a = ap.parse_args()
    a.tb_file = locate("tlumacz-tb.tsv", a.tb_file)
    a.schema_file = locate("tlumacz-tb-schema.md", a.schema_file)
    a.v18_file = locate("Studia_Romologica_nr_18_2025.txt", a.v18_file, "Studia_Romologica_nr_18_2025.pdf")
    ok = selftest(a) if a.selftest else run_checks(a)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
