#!/usr/bin/env python3
"""
validate_master.py — pre-deposit invariant checker for the SROM master CSV.

Run before minting DOIs / generating the Crossref deposit:
    python3 validate_master.py srom_master_v3.csv

Exit code 0 = clean (deposit-ready). Exit code 1 = blocking errors present.
Warnings never block but should be reviewed. This mirrors the hard-aborts in
generate_crossref_xml.py plus schema/consistency checks the generator doesn't do.
"""
import csv, sys, re

SCHEMA = [
    'article_id','doi_suffix','doi','landing_url','pdf_url',
    'journal_title','issn','volume','year','issue_signature','issue_theme','publisher','pub_date_online','pub_date_print','editorial_period',
    'section_nr','section_label','seq',
    'title_pl','title_en','authors_display','authors_struct','affiliation_display','orcid_display',
    'abstract_pl','abstract_en','keywords_pl','keywords_en','bio_note',
    'pages','pages_from','pages_to','pdf_file',
    'language','license','license_url','is_translation','original_title','original_source','original_doi',
]
# Optional columns: accepted when present, never required (older CSVs stay valid).
OPTIONAL = [
    'translators_struct',   # Given|Surname|Affiliation|ORCID ;; … — translator(s), Kanon § 12.2.3
]
SUFFIX_RE = re.compile(r'^[a-z0-9]{8}$')
DATE_RE   = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ORCID_RE  = re.compile(r'^https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}[\dX]$')
DOI_RE    = re.compile(r'^10\.\d{4,9}/[a-z0-9]{8}$')

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'srom_master_v3.csv'
    try:
        rows = list(csv.DictReader(open(path, encoding='utf-8-sig')))
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}"); sys.exit(1)

    errors, warnings = [], []
    E = errors.append; W = warnings.append

    if not rows:
        print("ERROR: empty CSV."); sys.exit(1)

    # --- schema ---
    have = list(rows[0].keys())
    missing = [c for c in SCHEMA if c not in have]
    extra   = [c for c in have if c not in SCHEMA and c not in OPTIONAL]
    if missing: E(f"schema: missing columns: {missing}")
    if extra:   W(f"schema: unexpected extra columns (ignored downstream): {extra}")

    seen_suffix, seen_id = {}, {}
    for i, r in enumerate(rows, 1):
        rid = r.get('article_id', f'row{i}')

        # DOI prefix / suffix
        doi = r.get('doi', '')
        if 'XXXXX' in doi:            E(f"{rid}: DOI prefix still placeholder 10.XXXXX")
        suf = r.get('doi_suffix', '')
        if not SUFFIX_RE.match(suf):  E(f"{rid}: doi_suffix '{suf}' is not final opaque [a-z0-9]{{8}}")
        elif suf in seen_suffix:      E(f"{rid}: duplicate doi_suffix '{suf}' (also {seen_suffix[suf]})")
        else:                         seen_suffix[suf] = rid
        if doi and 'XXXXX' not in doi and not DOI_RE.match(doi):
            W(f"{rid}: doi '{doi}' doesn't match 10.<prefix>/<8-char suffix>")

        # article_id uniqueness
        if rid in seen_id: E(f"duplicate article_id '{rid}'")
        else: seen_id[rid] = i

        # date
        d = r.get('pub_date_online', '')
        if not DATE_RE.match(d):       E(f"{rid}: pub_date_online '{d}' not YYYY-MM-DD")
        d = r.get('pub_date_print', '')
        if not DATE_RE.match(d):       E(f"{rid}: pub_date_print '{d}' not YYYY-MM-DD")
        if not (r.get('editorial_period') or '').strip(): E(f"{rid}: editorial_period empty")

        # license
        for col in ('license', 'license_url'):
            v = r.get(col, '')
            if not v or v.upper() == 'TODO': E(f"{rid}: {col} unfilled ('{v}')")
        lu = r.get('license_url', '')
        if lu and lu.upper() != 'TODO' and not lu.startswith('http'):
            W(f"{rid}: license_url not a URL: '{lu}'")

        # pages
        try:
            pf, pt = int(r['pages_from']), int(r['pages_to'])
            if pf > pt: E(f"{rid}: pages_from {pf} > pages_to {pt}")
        except (ValueError, KeyError):
            E(f"{rid}: pages_from/pages_to not both integers ('{r.get('pages_from')}'/'{r.get('pages_to')}')")

        # slug lowercase
        if suf and suf != suf.lower(): E(f"{rid}: doi_suffix must be lowercase")

        # authors_struct + ORCIDs
        struct = r.get('authors_struct', '')
        if not struct.strip():
            E(f"{rid}: authors_struct empty")
        else:
            for a in struct.split(';;'):
                a = a.strip()
                if not a: continue
                parts = [p.strip() for p in a.split('|')]
                if len(parts) != 4:
                    E(f"{rid}: author segment not 4 pipe-fields: '{a}'")
                    continue
                orc = parts[3]
                if orc and not ORCID_RE.match(orc):
                    W(f"{rid}: ORCID malformed for {parts[1]}: '{orc}'")

        # translation consistency
        if r.get('is_translation', '').upper() == 'TAK' and not r.get('original_title', '').strip():
            W(f"{rid}: is_translation=TAK but original_title empty (Crossref original_language_title will be omitted)")
        if r.get('original_doi', '').strip() and not r['original_doi'].startswith('10.'):
            W(f"{rid}: original_doi doesn't look like a DOI: '{r['original_doi']}'")

        # translators (optional column translators_struct -> Crossref contributor_role="translator")
        tstruct = r.get('translators_struct') or ''
        is_tr = r.get('is_translation', '').upper() == 'TAK'
        if is_tr and not tstruct.strip():
            W(f"{rid}: is_translation=TAK but translators_struct empty or absent (no translator in the deposit)")
        if tstruct.strip() and not is_tr and r.get('is_translation', '').upper() != 'ADAPTACJA':   # adapted and translated (C7)
            W(f"{rid}: translators_struct filled but is_translation is not TAK")
        for t in tstruct.split(';;'):
            t = t.strip()
            if not t: continue
            parts = [p.strip() for p in t.split('|')]
            if len(parts) != 4:
                E(f"{rid}: translator segment not 4 pipe-fields: '{t}'")
                continue
            if parts[3] and not ORCID_RE.match(parts[3]):
                W(f"{rid}: ORCID malformed for translator {parts[1]}: '{parts[3]}'")

    # --- report ---
    print(f"Checked {len(rows)} rows against {len(SCHEMA)}-column schema.\n")
    if errors:
        print(f"BLOCKING ERRORS ({len(errors)}):")
        for e in errors: print("  ✗", e)
        print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings: print("  !", w)
        print()
    if not errors and not warnings:
        print("✓ clean — deposit-ready.")
    elif not errors:
        print("✓ no blocking errors — deposit-ready (review warnings).")
    else:
        print("✗ NOT deposit-ready — resolve blocking errors first.")
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
