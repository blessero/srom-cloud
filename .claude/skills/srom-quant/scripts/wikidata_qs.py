#!/usr/bin/env python3
"""
wikidata_qs.py — Studia Romologica on Wikidata, as QuickStatements (v1) commands MB pastes at
https://quickstatements.toolforge.org (logged in with his own Wikidata account; nothing is sent from here).

    python3 wikidata_qs.py journal                                  # create the journal item (once)
    python3 wikidata_qs.py articles srom_master_v3.csv --journal Q… [--check]
        one item per article with a final DOI (after the Crossref deposit): title, DOI, journal, volume, pages,
        date, language, licence, authors as name strings in order. --check asks Wikidata first and skips a DOI
        that already has an item.

Item IDs used (checked 30.09.2026): Q5633421 scientific journal, Q13442814 scholarly article, Q809 Polish,
Q36 Poland, Q2037434 Romani studies, Q20007257 CC BY 4.0. The publisher has no item: none is referenced.
"""
import csv, json, re, sys, urllib.parse, urllib.request

LICENCES = {"creativecommons.org/licenses/by/4.0": "Q20007257"}


def q(s):
    return '"' + (s or "").replace('"', "'").strip() + '"'


def journal():
    return "\n".join([
        "CREATE",
        'LAST\tLpl\t"Studia Romologica"', 'LAST\tLen\t"Studia Romologica"',
        'LAST\tDpl\t"polski rocznik naukowy poświęcony romologii"', 'LAST\tDen\t"Polish academic annual of Romani studies"',
        "LAST\tP31\tQ5633421", 'LAST\tP1476\tpl:"Studia Romologica"', 'LAST\tP236\t"1689-4758"',
        "LAST\tP407\tQ809", "LAST\tP495\tQ36", "LAST\tP921\tQ2037434",
        "LAST\tP571\t+2008-00-00T00:00:00Z/9", 'LAST\tP856\t"https://studiaromologica.pl"'])


def exists(doi):
    u = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "list": "search", "srsearch": f"haswbstatement:P356={doi.upper()}", "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "SROM wikidata_qs"}), timeout=40) as r:
        hits = json.load(r)["query"]["search"]
    return hits[0]["title"] if hits else None


def articles(csv_path, qid, check=False):
    out, skipped = [], []
    for r in csv.DictReader(open(csv_path, encoding="utf-8-sig")):
        doi = r.get("doi", "")
        if "XXXXX" in doi or not re.fullmatch(r"10\.\d+/[a-z0-9]{8}", doi):
            skipped.append(f"{r['article_id']}: no final DOI")
            continue
        if check:
            have = exists(doi)
            if have:
                skipped.append(f"{r['article_id']}: already {have}")
                continue
        y = r.get("pub_date_online", "")[:4] or r.get("year", "")
        cmd = ["CREATE", f"LAST\tLpl\t{q(r['title_pl'])}", f"LAST\tDpl\t\"artykuł naukowy opublikowany w {y} roku\"",
               f"LAST\tDen\t\"scholarly article published in {y}\"", "LAST\tP31\tQ13442814",
               f"LAST\tP1476\tpl:{q(r['title_pl'])}", f"LAST\tP356\t{q(doi.upper())}", f"LAST\tP1433\t{qid}",
               f"LAST\tP478\t{q(r.get('volume'))}", "LAST\tP407\tQ809"]
        if r.get("title_en"):
            cmd.append(f"LAST\tLen\t{q(r['title_en'])}")
        if r.get("pages_from") and r.get("pages_to"):
            cmd.append(f"LAST\tP304\t\"{r['pages_from']}-{r['pages_to']}\"")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("pub_date_online", "")):
            cmd.append(f"LAST\tP577\t+{r['pub_date_online']}T00:00:00Z/11")
        for k, v in LICENCES.items():
            if k in (r.get("license_url") or ""):
                cmd.append(f"LAST\tP275\t{v}")
        if r.get("landing_url", "").startswith("http"):
            cmd.append(f"LAST\tP953\t{q(r['landing_url'])}")
        for i, a in enumerate(x for x in (r.get("authors_struct") or "").split(";;") if x.strip()):
            given, surname = (p.strip() for p in a.split("|")[:2])
            cmd.append(f"LAST\tP2093\t{q(given + ' ' + surname)}\tP1545\t\"{i + 1}\"")
        out.append("\n".join(cmd))
    return "\n".join(out), skipped


def main():
    a = sys.argv[1:]
    if a[:1] == ["journal"]:
        print(journal())
    elif a[:1] == ["articles"] and "--journal" in a:
        text, skipped = articles(a[1], a[a.index("--journal") + 1], "--check" in a)
        print(text)
        for s in skipped:
            print("# skipped " + s, file=sys.stderr)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
