# PRNG — Polish names of world places (leaf 1.3.3 input)

- `prng_swiat.jsonl`: all 14,268 records of the PRNG collection *PolskaNazwaGeograficznaSwiata* (GUGiK OGC API,
  `ogcapi.geoportal.gov.pl`), fetched 27.09.2026 with MB's OK (`fetch_log.txt`). Properties only, geometry dropped.
  The records' source field is the *Urzędowy wykaz polskich nazw geograficznych świata*, 2nd ed., 2019 (KSNG).
- Useful fields: `nazwaGlowna` (standard Polish name), `nazwaDluga` (official long form, states), `nazwaOboczna`,
  `nazwaHistoryczna`, genitive / locative / adjective of each, `endonim` (local names), `polozenieTerytorialne`,
  `rodzajObiektu`, `statusNazwy`.
- Rule (MB 27.09.2026): historical and political names are **never** mapped mechanically. The register offers
  candidates; the choice follows the period, place and politics of the passage and goes in the review sheet.
- Refresh: `python3 fetch_prng.py` (overwrites), then `shasum -a 256 -c manifest.sha256` will show the change.
