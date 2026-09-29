#!/usr/bin/env python3
"""
generate_crossref_xml.py — Studia Romologica
CSV (srom_master_v3.csv) -> Crossref deposit XML (schema 5.4.0), one file per volume.

Usage:
    python3 generate_crossref_xml.py srom_master_v3.csv [output.xml]

Before first use, fill in the CONFIG block (prefix, depositor, e-mail).
Upload the result at https://doi.crossref.org (admin tool) or test first at
https://test.crossref.org with the same credentials.
"""
import csv, sys, html, datetime, pathlib

# ---------------- CONFIG ----------------
DEPOSITOR_NAME  = "Studia Romologica / Komitet Opieki nad Zabytkami Kultury Zydowskiej w Tarnowie"
DEPOSITOR_EMAIL = "studiaromologica@muzeum.tarnow.pl"   # deposit reports go here
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
            parts.append('        <affiliations><institution><institution_name>'
                         f'{E(a["aff"])}</institution_name></institution></affiliations>')
        if a["orcid"].startswith("https://orcid.org/"):
            parts.append(f'        <ORCID authenticated="false">{E(a["orcid"])}</ORCID>')
        parts.append('      </person_name>')
    return "\n".join(parts)

def article_xml(r, pub_y, pub_m, pub_d):
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
  </journal_article>"""

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "srom_master_v3.csv"
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
    articles = "\n".join(article_xml(r, pub_y, pub_m, pub_d) for r in rows)

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
    print(f"OK: {out} ({len(rows)} articles). Validate at https://www.crossref.org/02publishers/parser.html or deposit to test.crossref.org first.")

if __name__ == "__main__":
    main()
