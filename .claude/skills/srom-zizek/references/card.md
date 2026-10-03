# Card — one paper, one page, comparable with every other card

The card is the unit of Zizek. It trades depth for comparability: every paper gets the same fixed
sections and the same score rubric, so twelve cards can be laid side by side. Anything that needs more
depth goes to `deep-review.md` — only for finalists or doubtful cases.

**Length:** 600–1,000 words, not counting the header table and Sources; up to about 1,300 when the paper needs it
(MB, 03.10.2026: completeness beats brevity here). Past that, the extra belongs in a deep review, not in the card.
**Output:** `volumes/<vol>/cards/<slug>.md` (slug = the text file's name). Update the row in `pool.md`.

## Before writing
1. Read the whole text (`volumes/<vol>/text/<slug>.txt`), not a sample. Book-length: card one chapter
   (extract it with `--pages`), say so in the header.
2. Read `volumes/<vol>/concept.md` (what the block is for) and skim `context/srom-archive.md` and
   `context/polish-field.md`.
3. Do sections 1–3A–3B from the text alone, with no searching (search would contaminate the internal read).
   Then search for 3C and 5.

## After writing
Run `python3 "$Z/check.py" volumes/<vol>/cards/<slug>.md` (add `--online` to look up the DOIs at Crossref).
Fix every MISSING or CLOSE anchor against the text — a CLOSE is usually a misquote, not extraction noise
(the pilot card had one). The card is not done while the check fails.

## Template

```markdown
# <Author> — <short title>
card · <date> · <scope: whole text | ch. N, pp. x–y> · text: text/<slug>.txt

| Type | TRANSLATION candidate (published: venue, year, DOI, licence if known) / SUBMISSION (manuscript) |
|---|---|
| Language · size | EN · 10,700 words · 22 pp. incl. notes |
| Discipline · method | e.g. history (archival: parish records 1780–1840) / theory essay / ethnography (n=…) |

## 1. Claim
The thesis in 2–3 sentences in the author's terms.
Anchor: "5–10 verbatim words" (§ heading)

## 2. How it argues
3–5 lines: the moves, the evidence base (what corpus, how much, from where), the key interlocutors.

## 3. Three axes — kept apart
Steelman: the strongest reading of the paper, in 1–2 sentences, before any criticism.

**A. Internal coherence** — sound / strained / broken
Does it hold on its own terms (premises and sources assumed true)? 1–3 findings, each:
[L|M|m] what — "anchor" (§) — why it is internal, not a disagreement.

**B. Method & evidence** — fit / stretched / unfit
Does the method carry the size of the claim? Overreach (quantify: "3 court cases → claim about the
Commonwealth"). Unstated assumptions. [FLAG-EXTERNAL] + the precise question, where a specialist is needed.

**C. Field standing** — advances / consolidates / derivative / contested / outdated
Grounded in retrieved sources only: reception (citations and their trajectory, reviews, rebuttals),
what it adds to the literature, consequential omissions (with evidence the omitted work is recognised).
Sparse field → say sparse.

## 4. Fit with the concept
Which strand of `concept.md` it serves; what only this paper brings; which other candidates it talks to,
duplicates or contradicts (by slug).

## 5. For the Polish reader
- New in Polish? (author/argument already available in Polish, incl. SROM — grep `context/srom-abstracts.tsv` for the
  author, key terms and Polish/EN equivalents; cite vol. + title, or a search hit)
- Hooks and frictions from `polish-field.md` §4 that apply (only those that apply)
- Terms that will need a decision in translation

## 6. Scores (rubric below — one line of justification each)
| Quality | Fit | Value for Polish readers |
|---|---|---|
| n | n | n |

## 7. Verdict
CORE / STRONG / CONDITIONAL (on what) / OUT — and why, in 2–3 lines.

## 8. Facts for the non-scholarly discussion (record, do not weigh)
Length and translation effort; rights holder and licence (CC BY? publisher permission?); author reachable /
known to SROM; a later or revised version by the author (book chapter, second edition) that might be the
better text to translate; anything else MB will want at the table.

## Sources
[1] Author, title, venue, year — URL/DOI — how verified (Crossref / publisher page / opened)
```

## Score rubric (anchored, so cards written on different days by different sessions agree)

**Quality** (sections 3A–C together; the worst load-bearing flaw caps it)
5 exceptional — would stand out in Critical Romani Studies / Romani Studies; no load-bearing flaw
4 solid — sound, minor or moderate flaws only
3 publishable with fixable problems (at least one moderate, fixable)
2 a load-bearing problem that revision may not fix
1 unsound

**Fit** (against `concept.md` as it stands on the card's date — re-check if the concept moves)
5 answers the concept's core question  ·  4 carries one strand fully  ·  3 relevant to one strand
2 tangential, would need framing to belong  ·  1 does not belong

**Value for Polish readers**
5 opens a debate absent from Polish scholarship  ·  4 new argument in a debate Poles know
3 partly available (other works, other languages Polish readers use)  ·  2 largely known in Polish
1 already in Polish / already in SROM

*Dialogue with other papers is not scored on the card — it depends on the others. It is judged in `block.md`.*

## Calibration anchors (MB's judgement is the reference)
When MB agrees with a card's scores, or corrects them, record it in the card's section 7 as
`MB <date>: agrees` / `MB <date>: Quality 3→4 — <reason>`, and list the card here. Card-writing subagents
read the cards listed here before scoring, so the rubric is anchored in MB's judgements, not only in words.
If MB's corrections keep pointing the same way, change the rubric above, not just the scores.
- (none confirmed yet — the pilot `19-2026/cards/black-bodies-white-bodies-gypsy-images-i` awaits MB's view)

## Rules that bite most often
- Anchors are verbatim, in the original language, 5–10 words + nearest heading. Never paraphrase inside quotes.
- `check.py` reads any quotation of 4+ words as an anchor. Put titles of other works in *italics*, not in
  quotes, or they are reported as missing (short quoted terms are ignored).
- The internal read (3A) takes the author's premises as true. "I disagree" is not an internal finding.
- A claim about "the literature" or "the field" needs a retrieved source in Sources. Model knowledge may point
  where to look; it is never the evidence. Mark any unverified recollection [MK].
- Manuscripts (SUBMISSION) are confidential: search with short conceptual queries, never with passages.
- Say where the paper is sound. A card that only lists faults is a bad card.
