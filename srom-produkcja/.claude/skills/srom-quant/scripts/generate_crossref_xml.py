#!/usr/bin/env python3
"""
generate_crossref_xml.py — Studia Romologica
CSV (srom_master_v3.csv) -> Crossref deposit XML (schema 5.4.0), one file per volume.

Usage:
    python3 generate_crossref_xml.py srom_master_v3.csv [output.xml]
    python3 generate_crossref_xml.py --ror srom_master_v3.csv      # fill volumes/ror.tsv from ROR (see below)

References (<citation_list>, Kanon § 13.1): volumes/<vol>/citations/<article_id>.json — the build's
<stem>_citations.json (srom-produkcja build.py), copied there at INJECT. An article without one is deposited
without references (listed on screen); references can be added later by a redeposit.
Affiliations: each institution of an affiliation ("A; B", "A / B") is its own <institution>; its ROR ID comes from
volumes/ror.tsv (institution as written in authors_struct, TAB, https://ror.org/…, ROR name, source). --ror adds
the institutions not yet in the file, with ROR's own confident match ("chosen") or empty: check the file before
a deposit.

Before first use, fill in the CONFIG block (prefix, depositor, e-mail).
Upload the result at https://doi.crossref.org (admin tool) or test first at
https://test.crossref.org with the same credentials.
"""
import csv, sys, html, datetime, pathlib, json, re, urllib.parse, urllib.request

# ---------------- CONFIG ----------------
DEPOSITOR_NAME  = "Studia Romologica / Komitet Opieki nad Zabytkami Kultury Zydowskiej w Tarnowie"
DEPOSITOR_EMAIL = "michalbartosz@studiaromologica.pl"   # deposit reports go here
REGISTRANT      = "Komitet Opieki nad Zabytkami Kultury Żydowskiej w Tarnowie"
JOURNAL_TITLE   = "Studia Romologica"
ISSN_PRINT      = "1689-4758"
LANG_DEFAULT    = "pl"
# -----------------------------------------

E = lambda s: html.escape((s or "").strip(), quote=True)

def parse_authors(s):
    """'Given|Surname|Affiliation|ORCID ;; ...' -> list of dicts"""
    out = []
    for a in (s or "").split(";;"):
        a = a.strip()
        if not a: continue
        given, surname, aff, orcid = (p.strip() for p in a.split("|"))
        out.append(dict(given=given, surname=surname, aff=aff, orcid=orcid))
    return out

ROR = {}   # institution as written -> ROR ID (volumes/ror.tsv)


def institutions(aff):
    """'Wydział Historii, Gonzaga University; Instytut …' -> one entry per institution"""
    return [x.strip() for x in re.split(r";\s+|\s+/\s+", aff or "") if x.strip()]


def load_ror(csv_path):
    f = pathlib.Path(csv_path).resolve().parent.parent / "ror.tsv"
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines()[1:]:
            c = ln.split("\t")
            if len(c) > 1 and c[1].startswith("https://ror.org/"):
                ROR[c[0].strip()] = c[1].strip()
    return f


def citations_xml(csv_path, article_id):
    f = pathlib.Path(csv_path).resolve().parent / "citations" / f"{article_id}.json"
    if not f.exists():
        return "", False
    out = ["    <citation_list>"]
    for i, c in enumerate(json.loads(f.read_text(encoding="utf-8")), 1):
        doi = f"<doi>{E(c['doi'])}</doi>" if c.get("doi") else ""
        out.append(f'      <citation key="ref{i}">{doi}<unstructured_citation>{E(c["text"])}</unstructured_citation></citation>')
    return "\n".join(out + ["    </citation_list>"]) + "\n", True


def ror_fill(csv_path):
    """add every institution of authors_struct/translators_struct not yet in ror.tsv, with ROR's chosen match"""
    f = load_ror(csv_path)
    known = set()
    if f.exists():
        known = {ln.split("\t")[0].strip() for ln in f.read_text(encoding="utf-8").splitlines()[1:]}
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    todo = sorted({i for r in rows for col in ("authors_struct", "translators_struct") for a in parse_authors(r.get(col))
                   for i in institutions(a["aff"]) if not i.startswith("[") and i not in known})
    new = []
    for inst in todo:
        u = "https://api.ror.org/v2/organizations?" + urllib.parse.urlencode({"affiliation": inst})
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "SROM (mailto:" + DEPOSITOR_EMAIL + ")"}), timeout=40) as resp:
            items = json.load(resp).get("items", [])
        ch = next((i for i in items if i.get("chosen")), None)
        name = next((n["value"] for n in ch["organization"]["names"] if "ror_display" in n["types"]), "") if ch else ""
        new.append(f"{inst}\t{ch['organization']['id'] if ch else ''}\t{name}\t"
                   f"{'ROR affiliation match (chosen) ' if ch else 'no confident ROR match '}{datetime.date.today():%d.%m.%Y}")
        print(new[-1])
    with open(f, "a", encoding="utf-8") as fh:
        if not known:
            fh.write("institution\tror\tror_name\tsource\n")
        fh.write("".join(x + "\n" for x in new))
    print(f"ROR: {len(new)} added to {f} ({sum(1 for x in new if 'ror.org' in x)} with an ID) — check them before a deposit")


def contributor_xml(authors, translators=()):
    """Authors first (the first one sequence="first"), then translators (always "additional")."""
    parts = []
    people = [(a, "first" if i == 0 else "additional", "author") for i, a in enumerate(authors)]
    people += [(t, "additional", "translator") for t in translators]
    for a, role, contrib in people:
        parts.append(f'      <person_name sequence="{role}" contributor_role="{contrib}">')
        parts.append(f'        <given_name>{E(a["given"])}</given_name>')
        parts.append(f'        <surname>{E(a["surname"])}</surname>')
        if a["aff"] and not a["aff"].startswith("["):
            inst = "".join(f'<institution><institution_name>{E(i)}</institution_name>'
                           + (f'<institution_id type="ror">{E(ROR[i])}</institution_id>' if i in ROR else "") + '</institution>'
                           for i in institutions(a["aff"]))
            parts.append(f'        <affiliations>{inst}</affiliations>')
        if a["orcid"].startswith("https://orcid.org/"):
            parts.append(f'        <ORCID authenticated="false">{E(a["orcid"])}</ORCID>')
        parts.append('      </person_name>')
    return "\n".join(parts)

def article_xml(r, pub_y, pub_m, pub_d, cites=""):
    lang = r.get("language") or LANG_DEFAULT
    authors = parse_authors(r["authors_struct"])
    translators = parse_authors(r.get("translators_struct"))  # optional column; empty/absent -> none
    abstracts = []
    if r.get("abstract_pl"):
        abstracts.append(f'    <jats:abstract xml:lang="pl"><jats:p>{E(r["abstract_pl"])}</jats:p></jats:abstract>')
    if r.get("abstract_en"):
        abstracts.append(f'    <jats:abstract xml:lang="en"><jats:p>{E(r["abstract_en"])}</jats:p></jats:abstract>')

    # translated articles: original_language_title + isTranslationOf relation (if original DOI known)
    orig_title_xml = ""
    if r.get("is_translation") == "TAK" and r.get("original_title"):
        orig_title_xml = f'\n      <original_language_title language="en">{E(r["original_title"])}</original_language_title>'
    rel_xml = ""
    if r.get("original_doi"):
        rel_xml = (
            '    <program xmlns="http://www.crossref.org/relations.xsd">\n'
            '      <related_item>\n'
            f'        <intra_work_relation relationship-type="isTranslationOf" identifier-type="doi">{E(r["original_doi"])}</intra_work_relation>\n'
            '      </related_item>\n'
            '    </program>\n')
    lic_xml = ""
    if (r.get("license_url") or "").startswith("http"):
        lic_xml = (
            '    <program xmlns="http://www.crossref.org/AccessIndicators.xsd" name="AccessIndicators">\n'
            '      <free_to_read/>\n'
            f'      <license_ref applies_to="vor" start_date="{pub_y}-{pub_m}-{pub_d}">{E(r["license_url"])}</license_ref>\n'
            '    </program>\n')

    return f"""  <journal_article publication_type="full_text" language="{lang}">
    <titles>
      <title>{E(r["title_pl"])}</title>{orig_title_xml}
    </titles>
    <contributors>
{contributor_xml(authors, translators)}
    </contributors>
{chr(10).join(abstracts)}
    <publication_date media_type="online">
      <month>{pub_m}</month><day>{pub_d}</day><year>{pub_y}</year>
    </publication_date>
    <pages>
      <first_page>{E(r["pages_from"])}</first_page>
      <last_page>{E(r["pages_to"])}</last_page>
    </pages>
{lic_xml}{rel_xml}    <doi_data>
      <doi>{E(r["doi"])}</doi>
      <resource content_version="vor">{E(r["landing_url"])}</resource>
      <collection property="crawler-based">
        <item crawler="iParadigms"><resource>{E(r["pdf_url"])}</resource></item>
      </collection>
    </doi_data>
{cites}  </journal_article>"""

def main():
    if sys.argv[1:2] == ["--ror"]:
        return ror_fill(sys.argv[2])
    src = sys.argv[1] if len(sys.argv) > 1 else "srom_master_v3.csv"
    load_ror(src)
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    if not rows:
        sys.exit("Empty CSV.")
    r0 = rows[0]
    if "XXXXX" in r0["doi"]:
        sys.exit("ABORT: DOI prefix still 10.XXXXX — fill in the real prefix in the CSV first.")
    import re
    for r in rows:
        if not re.fullmatch(r"[a-z0-9]{8}", r["doi_suffix"]):
            sys.exit(f"ABORT: doi_suffix '{r['doi_suffix']}' ({r['article_id']}) is not a final 8-char lowercase suffix.")
    try:
        pub_y, pub_m, pub_d = r0["pub_date_online"].split("-")
        int(pub_d)
    except ValueError:
        sys.exit("ABORT: pub_date_online must be YYYY-MM-DD (currently: %r)" % r0["pub_date_online"])

    now = datetime.datetime.now()
    batch_id = f"srom-{r0['volume']}-{now:%Y%m%d%H%M%S}"
    parts, norefs = [], []
    for r in rows:
        cites, has = citations_xml(src, r["article_id"])
        if not has:
            norefs.append(r["article_id"])
        parts.append(article_xml(r, pub_y, pub_m, pub_d, cites))
    articles = "\n".join(parts)

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<doi_batch xmlns="http://www.crossref.org/schema/5.4.0"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
           version="5.4.0"
           xsi:schemaLocation="http://www.crossref.org/schema/5.4.0 https://www.crossref.org/schemas/crossref5.4.0.xsd">
<head>
  <doi_batch_id>{batch_id}</doi_batch_id>
  <timestamp>{now:%Y%m%d%H%M%S}</timestamp>
  <depositor>
    <depositor_name>{E(DEPOSITOR_NAME)}</depositor_name>
    <email_address>{E(DEPOSITOR_EMAIL)}</email_address>
  </depositor>
  <registrant>{E(REGISTRANT)}</registrant>
</head>
<body>
<journal>
  <journal_metadata language="{LANG_DEFAULT}">
    <full_title>{E(JOURNAL_TITLE)}</full_title>
    <issn media_type="print">{ISSN_PRINT}</issn>
  </journal_metadata>
  <journal_issue>
    <publication_date media_type="online">
      <month>{pub_m}</month><day>{pub_d}</day><year>{pub_y}</year>
    </publication_date>
    <journal_volume><volume>{E(r0["volume"])}</volume></journal_volume>
  </journal_issue>
{articles}
</journal>
</body>
</doi_batch>"""
    out = sys.argv[2] if len(sys.argv) > 2 else f"crossref_deposit_srom_{r0['volume']}_{r0['year']}.xml"
    pathlib.Path(out).write_text(xml, encoding="utf-8")
    if norefs:
        print(f"note: no references file (citations/<article_id>.json) for {len(norefs)}: {', '.join(norefs)}")
    print(f"OK: {out} ({len(rows)} articles). Validate at https://www.crossref.org/02publishers/parser.html or deposit to test.crossref.org first.")

if __name__ == "__main__":
    main()
