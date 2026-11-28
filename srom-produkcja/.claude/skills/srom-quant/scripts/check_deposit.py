#!/usr/bin/env python3
"""check_deposit.py — the check before a Crossref upload: the deposit XML against the master CSV, contributor by contributor.

    python3 check_deposit.py <master CSV> <deposit XML> [--site] [--ready <folder of the covered PDFs>] [--only 1-5]

Written 14.10.2026 (Cowork) after the vol. 18 deposit of 13.10.2026 went out with 31 damaged references and a session report
that named two authors as having no ORCID when one had it: that check only counted, and the report named people from memory.
This prints every contributor BY NAME with the ORCID the CSV gives and the one the XML carries, so a report quotes it.
Per article: DOI, landing and PDF address, pages, print and online dates, licence, contributors (authors, then translators)
with ORCID, references (count = citations/<article_id>.json) and their text (no U+FFFD, no doubled accent, no control
character). --site: each landing page answers 200 with the right citation_doi, each PDF answers 200 (and, with --ready, is
byte-identical to the covered PDF there); a redirect is a fault, since the deposited address must be the page itself, not a
301 to it (review 21.10.2026). Paced (PACE seconds per request), because the site blocks bursts (429, and Wordfence). Read-only.
--only a-b (or n): only articles at those positions in the XML (1-based), so a long --site run fits in parts
(C31, 30.10.2026); the CSV-only-rows check is skipped then.
Crossmark (28.11.2026): an article generate_crossref_xml.py gives Crossmark (CROSSMARK_POLICY_DOI set, its volume not in
CROSSMARK_EXCLUDE) must carry <crossmark> with that policy DOI and studiaromologica.pl among its domains; any other article
must not (an XML made under another setting). --site also asks doi.org once whether the policy DOI is registered and
points at CROSSMARK_POLICY_URL (no request to the journal's site). --ready also opens each covered PDF there (local, no request): for an
article with Crossmark, its cover must link the Crossmark dialog for its own DOI and pub_date_online; for one without, not. Last line: DEPOSIT CHECK OK n/n, or DEPOSIT CHECK FAILED k/n. Owner: srom-quant (taken over from Cowork, C15 addendum).
"""
import csv, hashlib, json, os, re, sys, time, unicodedata, urllib.request, urllib.error
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_crossref_xml import CROSSMARK_DOMAIN, CROSSMARK_POLICY_DOI, CROSSMARK_POLICY_URL, crossmark_for, crossmark_pdf_url  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
SITE = "--site" in sys.argv
READY = sys.argv[sys.argv.index("--ready") + 1] if "--ready" in sys.argv else None
if READY in args: args.remove(READY)
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
if ONLY in args: args.remove(ONLY)
if ONLY:
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", ONLY)
    if not m: sys.exit("--only takes n or a-b")
    LO, HI = int(m[1]), int(m[2] or m[1])
if len(args) != 2: sys.exit(__doc__)
csvp, xmlp = args
rows = {r["doi"].strip().lower(): r for r in csv.DictReader(open(csvp, encoding="utf-8-sig"))}
cdir = os.path.join(os.path.dirname(os.path.abspath(csvp)), "citations")
root = ET.parse(xmlp).getroot()
NS = {"c": root.tag.split("}")[0][1:]}
T = lambda e: "".join(e.itertext()).strip() if e is not None else ""
ORC = re.compile(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]")

def people(s):
    out = []
    for a in (s or "").split(";;"):
        f = [x.strip() for x in a.split("|")]
        if len(f) >= 2 and (f[0] or f[1]):
            m = ORC.search(a)
            out.append((f"{f[0]} {f[1]}".strip(), m[0] if m else ""))
    return out

def textflaws(s):
    bad = []
    if "�" in s: bad.append("U+FFFD")
    for i, ch in enumerate(s):
        if unicodedata.combining(ch) and i and ch in unicodedata.normalize("NFD", s[i - 1]): bad.append("doubled accent"); break
    if any(unicodedata.category(c) == "Cc" for c in s): bad.append("control character")
    if unicodedata.normalize("NFC", s) != s: bad.append("not NFC")
    return bad

PACE = float(os.environ.get("SROM_PACE", 5))   # seconds between site requests (was 1.5; 21.10.2026 MB's IP was blocked for a while, host or Wordfence)
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None   # 3xx surfaces as HTTPError: reported, never followed
OPEN = urllib.request.build_opener(NoRedirect).open

def get(url):
    for attempt in range(3):
        req = urllib.request.Request(url, headers={"User-Agent": "SROM check_deposit"})
        try:
            with OPEN(req, timeout=40) as r: return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(20 * (attempt + 1)); continue
            if 300 <= e.code < 400: return f"{e.code} → {e.headers.get('Location', '?')}", b""
            return e.code, b""
        except Exception as e:
            return f"error {e.__class__.__name__}", b""
    return 429, b""

arts = root.findall(".//c:journal_article", NS)
failed, seen = 0, set()
POLICY_BAD = ""
if SITE and any(a.find("c:crossmark", NS) is not None for a in arts):     # one request to doi.org, never followed
    st, _ = get(os.environ.get("SROM_DOI_RESOLVER", "https://doi.org/") + CROSSMARK_POLICY_DOI)
    if not (isinstance(st, str) and st.split(" → ")[-1].rstrip("/") == CROSSMARK_POLICY_URL.rstrip("/")):
        POLICY_BAD = f"policy DOI {CROSSMARK_POLICY_DOI} not registered or not pointing at {CROSSMARK_POLICY_URL} (doi.org: {st})"
        print("!! " + POLICY_BAD)
for pos, a in enumerate(arts, 1):
    if ONLY and not LO <= pos <= HI: continue
    doi = T(a.find("c:doi_data/c:doi", NS)).lower(); seen.add(doi)
    r = rows.get(doi); probs = []
    if r is None:
        print(f"?? {doi}: not in the CSV"); failed += 1; continue
    aid = r["article_id"][-3:]
    if T(a.find("c:doi_data/c:resource", NS)) != r["landing_url"]: probs.append("landing address differs from the CSV")
    if r["pdf_url"] not in [T(x) for x in a.findall(".//c:collection//c:resource", NS)]: probs.append("PDF address missing")
    pages = (T(a.find("c:pages/c:first_page", NS)), T(a.find("c:pages/c:last_page", NS)))
    if pages != (r["pages_from"], r["pages_to"]): probs.append(f"pages {pages[0]}–{pages[1]} vs CSV {r['pages_from']}–{r['pages_to']}")
    dates = {}
    for pd in a.findall("c:publication_date", NS):
        y, m, d = (T(pd.find(f"c:{k}", NS)) for k in ("year", "month", "day"))
        dates[pd.get("media_type")] = f"{y}-{int(m):02d}-{int(d):02d}" if m and d else y
    if dates.get("online") != r.get("pub_date_online"): probs.append(f"online date {dates.get('online')} vs CSV {r.get('pub_date_online')}")
    if (r.get("pub_date_print") or "") and dates.get("print") != r["pub_date_print"]: probs.append(f"print date {dates.get('print')} vs CSV {r['pub_date_print']}")
    lic = [T(x) for x in a.iter() if x.tag.endswith("license_ref")]
    if r.get("license_url") and r["license_url"] not in lic: probs.append("licence missing")
    want = people(r["authors_struct"]) + people(r.get("translators_struct"))
    got = []
    for p in a.findall(".//c:person_name", NS):
        got.append((f"{T(p.find('c:given_name', NS))} {T(p.find('c:surname', NS))}".strip(), (ORC.search(T(p.find('c:ORCID', NS))) or [""])[0]))
    if want != got: probs.append(f"contributors differ: CSV {want} / XML {got}")
    names = "; ".join(f"{n} ({o or 'no ORCID'})" for n, o in got)
    cits = [T(c) for c in a.findall(".//c:unstructured_citation", NS)]
    jf = os.path.join(cdir, r["article_id"] + ".json")
    nj = len(json.load(open(jf, encoding="utf-8"))) if os.path.exists(jf) else 0
    if len(cits) != nj: probs.append(f"references {len(cits)} vs citations file {nj}")
    flaws = [(i + 1, textflaws(c)) for i, c in enumerate(cits)]
    flaws = [(i, f) for i, f in flaws if f]
    if flaws: probs.append(f"{len(flaws)} references with damaged text, e.g. ref {flaws[0][0]}: {', '.join(flaws[0][1])}")
    for el in a.iter():
        if el.text and el.tag.split('}')[-1] in ("title", "p") and textflaws(el.text): probs.append(f"damaged text in {el.tag.split('}')[-1]}"); break
    cm, pol = a.find("c:crossmark", NS), crossmark_for(r)
    if pol:
        if cm is None: probs.append(f"no <crossmark> (vol. {r.get('volume')} has Crossmark, policy {pol}): regenerate the XML")
        else:
            if T(cm.find("c:crossmark_policy", NS)) != pol: probs.append(f"crossmark policy {T(cm.find('c:crossmark_policy', NS))} ≠ {pol}")
            if CROSSMARK_DOMAIN not in [T(x) for x in cm.findall(".//c:domain", NS)]: probs.append(f"crossmark domains lack {CROSSMARK_DOMAIN}")
    elif cm is not None: probs.append(f"<crossmark> in the XML, but vol. {r.get('volume')} has no Crossmark in generate_crossref_xml.py (CROSSMARK_POLICY_DOI / CROSSMARK_EXCLUDE)")
    if cm is not None and POLICY_BAD: probs.append("Crossmark policy DOI not live (see above)")
    if READY:
        lp = os.path.join(READY, r["pdf_file"])
        if pol and not os.path.exists(lp): probs.append(f"no covered PDF in ready/: {r['pdf_file']}")
        elif os.path.exists(lp):
            import pymupdf
            uris = {l.get("uri") or "" for l in pymupdf.open(lp)[0].get_links()}
            if pol and crossmark_pdf_url(r["doi"], r.get("pub_date_online", "")) not in uris: probs.append("covered PDF: no Crossmark link for this DOI and date on the cover")
            if not pol and any("crossmark.crossref.org" in u for u in uris): probs.append("covered PDF has a Crossmark button, but its deposit has no Crossmark")
    if SITE:
        st, body = get(r["landing_url"]); time.sleep(PACE)
        if st != 200 or f'name="citation_doi" content="{r["doi"]}"' not in body.decode("utf-8", "replace"):
            probs.append(f"landing page {st}, citation_doi {'ok' if body and r['doi'] in body.decode('utf-8','replace') else 'missing'}")
        st, pdf = get(r["pdf_url"]); time.sleep(PACE)
        if st != 200: probs.append(f"PDF {st}")
        elif READY:
            lp = os.path.join(READY, r["pdf_file"])
            if not os.path.exists(lp) or hashlib.sha256(open(lp, "rb").read()).digest() != hashlib.sha256(pdf).digest():
                probs.append("PDF on the site differs from ready/")
    print(f"{'OK' if not probs else '!!'} {aid} {doi} pp. {pages[0]}–{pages[1]} · {dates} · refs {len(cits)}{' · Crossmark' if cm is not None else ''} · {names}")
    for p in probs: print(f"     - {p}")
    failed += bool(probs)
for d in ([] if ONLY else sorted(set(rows) - seen)): print(f"!! {rows[d]['article_id']} {d}: in the CSV, not in the XML"); failed += 1
n = len(seen) if ONLY else len(set(rows) | seen)
print(f"DEPOSIT CHECK OK {n}/{n}" if not failed else f"DEPOSIT CHECK FAILED {failed}/{n}")
sys.exit(1 if failed else 0)
