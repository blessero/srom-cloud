"""Fetch the PRNG collection PolskaNazwaGeograficznaSwiata (Polish names of world places; source: the 2019 KSNG
world list) from the official GUGiK OGC API, all pages, and store the name fields without geometry.
Output: prng_swiat.jsonl (one record per line, properties only) + fetch_log.txt. Re-runnable; overwrites."""
import json, os, time, urllib.request
BASE = "https://ogcapi.geoportal.gov.pl/res/ims/maps/PRNG/apiFeatures/collections/PolskaNazwaGeograficznaSwiata/items?f=json&limit=150&offset={}"
HERE = os.path.dirname(os.path.abspath(__file__))
out, off, total, stamp = [], 0, None, None
while total is None or off < total:
    for attempt in range(5):
        try:
            d = json.load(urllib.request.urlopen(BASE.format(off), timeout=60)); break
        except Exception as e:
            if attempt == 4: raise
            time.sleep(3 * (attempt + 1))
    total = d["numberMatched"]; stamp = stamp or d.get("timeStamp")
    out += [f["properties"] for f in d["features"]]
    if not d["features"]: break
    off += 150
ids = {r["idPRNG"] for r in out}
with open(os.path.join(HERE, "prng_swiat.jsonl"), "w", encoding="utf-8") as f:
    for r in out: f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(os.path.join(HERE, "fetch_log.txt"), "w", encoding="utf-8") as f:
    f.write(f"fetched {time.strftime('%Y-%m-%d %H:%M')} (API timeStamp of first page {stamp})\n"
            f"numberMatched {total}; records {len(out)}; unique idPRNG {len(ids)}\n")
print(f"records {len(out)} / matched {total}; unique {len(ids)}")
