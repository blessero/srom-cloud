# volumes — data of the journal as a whole (not of one article)

- `autorzy.tsv` — register of SROM authors, one row per person: sort key, name as printed (with degree), ORCID,
  affiliation, note (Polish), contact, source, doubts (`uwagi`). Built 30.09.2026 from
  `0. ASSETS/# Studia Romologica – Authors INFO.md` (vols. 1–18, 78 persons) plus two gaps from the vol. 18 cover data
  (Fotta's note, Wesołkin); 33 ORCIDs from the newer copy in `WEBSITE/Claude Code/SROM DataChief/`, each checked
  against its ORCID record (name matches), 46 in all. The Markdown file is superseded by this one; texts kept as written, doubts flagged, not fixed.
  Edit it in Numbers/Excel (tab-separated, UTF-8). Feeds "Noty o autorach" and the `bio_note` of the master CSV.
- `<vol>/citations/<article_id>.json` — each article's printed bibliography (srom-produkcja build `_citations.json`, copied at
  INJECT) for the Crossref deposit's reference list (srom-quant `generate_crossref_xml.py`).
- `ror.tsv` — institution as written in `authors_struct` → ROR ID (https://ror.org), for the Crossref affiliations. Filled by
  `generate_crossref_xml.py --ror <csv>` from ROR's confident matches or by name; the `source` column says which. Check new rows
  before a deposit; an institution without an ID is deposited by name only.
