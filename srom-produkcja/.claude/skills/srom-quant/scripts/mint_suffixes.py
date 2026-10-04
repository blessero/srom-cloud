#!/usr/bin/env python3
"""
mint_suffixes.py — fill the DOI suffixes of one volume's master CSV.

    python3 mint_suffixes.py volumes/19/srom_master_v3.csv --prefix 10.12345 [--dry-run]

For every row whose doi_suffix is empty or a placeholder (todo0001 …) it mints an opaque random [a-z0-9]{8}
(Python `secrets`), unique across every volumes/*/srom_master*.csv. Then, for every row, it sets `doi` to
<prefix>/<suffix> and swaps the old DOI for the new one inside `landing_url`. A suffix that is already final is never
changed: suffixes freeze at import. A row whose DOI carries a different real prefix stops the run.

Nothing is written unless every check passes. Rewrites the CSV in place, byte-for-byte except the cells it fills
(UTF-8 with BOM, CRLF, as the file already is). Run validate_master.py afterwards.
"""
import csv, glob, os, re, secrets, string, sys

ALPHABET = string.ascii_lowercase + string.digits
FINAL_RE = re.compile(r"^[a-z0-9]{8}$")
PLACEHOLDER_RE = re.compile(r"^todo\d*$")
PREFIX_RE = re.compile(r"^10\.\d{4,9}$")


def mint(taken):
    while True:
        s = "".join(secrets.choice(ALPHABET) for _ in range(8))
        if s not in taken and not PLACEHOLDER_RE.match(s):
            taken.add(s)
            return s


def other_suffixes(path):
    """Final suffixes of the other volumes' masters (the parent folder of the volume folder holds them all)."""
    taken = set()
    for p in glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(path))), "*", "srom_master*.csv")):
        if os.path.abspath(p) == os.path.abspath(path):
            continue
        for r in csv.DictReader(open(p, encoding="utf-8-sig", newline="")):
            taken.add(r.get("doi_suffix", ""))
    return taken


def run(path, prefix, dry=False):
    if not PREFIX_RE.match(prefix):
        sys.exit(f"ABORT: prefix '{prefix}' is not of the form 10.NNNNN (4-9 digits).")
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("ABORT: empty CSV.")
    cols = list(rows[0].keys())
    for need in ("doi_suffix", "doi", "landing_url"):
        if need not in cols:
            sys.exit(f"ABORT: column '{need}' missing.")

    taken = other_suffixes(path) | {r["doi_suffix"] for r in rows if FINAL_RE.match(r["doi_suffix"]) and not PLACEHOLDER_RE.match(r["doi_suffix"])}
    minted = changed = 0
    for r in rows:
        old_doi, suf = r["doi"], r["doi_suffix"]
        m = re.match(r"^(10\.[^/]+)/", old_doi)
        if m and "XXXXX" not in m.group(1) and m.group(1) != prefix:
            sys.exit(f"ABORT: {r['article_id']} already has prefix {m.group(1)}, not {prefix}. Prefix changes are done by hand.")
        if not suf or PLACEHOLDER_RE.match(suf):
            suf = mint(taken)
            r["doi_suffix"] = suf
            minted += 1
        elif not FINAL_RE.match(suf):
            sys.exit(f"ABORT: {r['article_id']}: doi_suffix '{suf}' is neither a placeholder nor a final [a-z0-9]{{8}}.")
        new_doi = f"{prefix}/{suf}"
        if old_doi != new_doi:
            if old_doi and old_doi in r["landing_url"]:
                r["landing_url"] = r["landing_url"].replace(old_doi, new_doi)
            elif r["landing_url"] and not r["landing_url"].rstrip("/").endswith(suf):
                print(f"NOTE: {r['article_id']}: landing_url does not contain the old DOI; left as it is: {r['landing_url']}")
            r["doi"] = new_doi
            changed += 1

    for r in rows:
        print(f"{r['article_id']}  {r['doi']}")
    print(f"{minted} suffix(es) minted, {changed} row(s) changed" + (" (dry run, nothing written)" if dry else ""))
    if dry or not changed:
        return
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if "--prefix" not in argv:
        sys.exit(__doc__)
    prefix = argv[argv.index("--prefix") + 1]
    args = [a for a in args if a != prefix]
    if len(args) != 1:
        sys.exit(__doc__)
    run(args[0], prefix, "--dry-run" in argv)


if __name__ == "__main__":
    main(sys.argv[1:])
