#!/usr/bin/env python3
"""measure131.py — runnable checks for tlumacz-gates-1.3.1.md (run from the srom-tlumacz folder).

  seed        every pl_attested form of kartoteka-seed.tsv occurs in at least one of the cited Polish articles,
              and the source_form (or a variant) in at least one of the cited English articles (skipped for
              rows flagged SV: attested only in a revised source version we do not hold)
  coverage    every name on HARVEST has a seed row (source_form or en_variants)
  candidates  tb-candidates.tsv merged into a temporary copy of tlumacz-tb.tsv passes tlumacz-check_tb.py
"""
import csv, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, "sources", "vol18-md")
# Group names harvested from the capitalised-token counts of the four English texts (27.09.2026)
HARVEST = ["Roma", "Rom", "Gypsies", "Romanies", "Romani Americans", "Ciganos", "Calon", "Gitanos", "Bohémiens",
           "Tsiganes", "Zigeuner", "Travellers", "Sinti", "Manush", "Kale", "Kaale", "Romanichels", "Boyash",
           "Rudari", "Ashkali", "Egyptians", "Yenish", "Dom", "Lom", "Bosha", "Garachi", "Karachi", "Parsi",
           "Lyuli", "Dzhugi", "Nawar", "Ghajar", "Mutrib", "Abdal", "Gurbati", "Halabi"]


def rows(p): return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
def text(art, lang): return re.sub(r"\s+", " ", open(os.path.join(MD, f"{art}_{lang}.md"), encoding="utf-8").read())
def split(v): return [x.strip() for x in v.split("|") if x.strip()]


def seed():
    R = rows(os.path.join(HERE, "kartoteka-seed.tsv")); n = ok = 0
    for r in R:
        arts = r["articles"].split()
        for form in split(r["pl_attested"]):
            n += 1
            if any(re.search(rf"(?<!\w){re.escape(form)}(?!\w)", text(a, "pl")) for a in arts): ok += 1
            else: print(f"  PL form not found: {form} in {arts}")
        en = [r["source_form"]] + split(r["en_variants"])
        if "SV" not in r["flag"] and not any(re.search(rf"(?<!\w){re.escape(e)}(?!\w)", text(a, "en")) for a in arts for e in en):
            n += 1; print(f"  EN form not found: {en} in {arts}")
    print(f"seed: {ok}/{n} forms found")


def coverage():
    R = rows(os.path.join(HERE, "kartoteka-seed.tsv"))
    have = {x for r in R for x in [r["source_form"]] + split(r["en_variants"]) for x in [x] + x.split()}
    miss = [h for h in HARVEST if h not in have]
    print(f"coverage: all {len(HARVEST)} harvested names have a row" if not miss else f"coverage: missing {miss}")


def candidates():
    """Changed rows replace their concept_id, new rows are appended; the merge must pass check_tb, and every
    `md <art>: «…»` quote in a candidate row is verified here too (check_tb checks quotes of HOUSE rows only)."""
    tb = os.path.join(ROOT, "tlumacz-tb.tsv"); cand = os.path.join(HERE, "tb-candidates.tsv")
    base, C = rows(tb), rows(cand); H = list(base[0].keys())
    ids = {r["concept_id"] for r in C}
    merged = [r for r in base if r["concept_id"] not in ids] + C
    d = tempfile.mkdtemp(); m = os.path.join(d, "tb.tsv")
    with open(m, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=H, delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(merged)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tlumacz-check_tb.py"), "--tb-file", m,
                        "--schema", "--shape", "--vocab", "--precedent", "--evidence"], capture_output=True, text=True)
    print(r.stdout.strip())
    bad = 0
    for row in C:
        for art, q in re.findall(r"md (\w+): «(.+?)»", row["precedent"]):
            if re.sub(r"\s+", " ", q) not in text(art, "pl"):
                bad += 1; print(f"  {row['concept_id']}: quote not found in {art}_pl.md: «{q}»")
    ok = r.returncode == 0 and not bad
    print(f"candidates: valid, {len(C)} rows, precedent ok" if ok else f"candidates: INVALID ({bad} quote(s) missing)")


if __name__ == "__main__":
    {"seed": seed, "coverage": coverage, "candidates": candidates}[sys.argv[1]]()
