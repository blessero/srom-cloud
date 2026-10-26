#!/usr/bin/env python3
"""Find the page of a digitised period publication that mentions a word, and fetch its image (learnt 25.10.2026).

    ia_find.py <out-dir> <term-regex> <ia-id> [<ia-id> ...]

For each Internet Archive id: downloads <id>_djvu.txt (grep: line numbers and context), then <id>_djvu.xml to give the
LEAF INDEX of every page whose text matches, and saves that page and its neighbours as <out-dir>/<id>_n<k>.jpg
(`/download/<id>/page/n<k>_w1000.jpg`; n<k> = the leaf index printed here, checked exact on jacksonsfamousph01jack,
so look at the image and its printed folio before citing). Pages only appear in the xml of books with OCR; a book with
no OCR gives nothing (SKILL.md known-item search, step 3). Example that found the Pike Gypsies:
    ia_find.py /tmp/x 'gyps|gipsy|romany' jacksonsfamousph01jack onpikethefirstco00unse
Polite: 2 s between requests; never put the journal's domain in anything (sources.md § Wikimedia)."""
import sys, re, os, time, urllib.request

UA = "SROM-ikonograf/0.2 (Studia Romologica, non-commercial journal research; https://github.com/blessero)"
def get(url, tries=3):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120).read()
        except Exception:
            time.sleep(5 * (k + 1))
    return None

out, pat, ids = sys.argv[1], re.compile(sys.argv[2], re.I), sys.argv[3:]
os.makedirs(out, exist_ok=True)
for i in ids:
    txt = get(f"https://archive.org/download/{i}/{i}_djvu.txt"); time.sleep(2)
    if not txt: print(f"== {i}: no OCR text"); continue
    lines = txt.decode("utf-8", "ignore").splitlines()
    hits = [n for n, l in enumerate(lines) if pat.search(l)]
    print(f"== {i}: {len(lines)} lines, {len(hits)} hits")
    for n in hits[:12]:
        flat = re.sub(r"\s+", " ", lines[n])[:200]
        print("   line %d: %s" % (n + 1, flat))
    if not hits: continue
    xml = get(f"https://archive.org/download/{i}/{i}_djvu.xml"); time.sleep(2)
    if not xml: print("   (no djvu.xml: find the page by hand)"); continue
    pages = xml.decode("utf-8", "ignore").split("<OBJECT")[1:]
    leaves = [k for k, p in enumerate(pages) if pat.search(re.sub(r"<[^>]+>", " ", p))]
    print("   leaf indices:", leaves[:30])
    for k in leaves[:6]:
        for j in (k, k + 1):
            b = get(f"https://archive.org/download/{i}/page/n{j}_w1000.jpg"); time.sleep(2)
            if b: open(os.path.join(out, f"{i}_n{j}.jpg"), "wb").write(b)
        print(f"   saved {i}_n{k}.jpg (+ n{k+1})")
