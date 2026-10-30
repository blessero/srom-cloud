# Card — one paper, one page, comparable with every other card

The card is the unit of Zizek. It trades depth for comparability: every paper gets the same fixed
sections and the same score rubric, so twelve cards can be laid side by side. Anything that needs more
depth goes to `deep-review.md` — only for finalists or doubtful cases.

**Length:** as long as the paper needs, up to about 2,000 words, not counting the header table and Sources (MB
29.10.2026: enough to understand and discuss the paper, short enough to read a dozen side by side). § 2 takes the
room first (up to ~400). Over 2,000, trim repetition before anything else; what still does not fit belongs in a deep
review.
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
An argument map, about 200–400 words, from which MB can recall the paper without rereading it and see how its
concepts relate (MB 27.10.2026: the pilot's one-line chain of detours served neither):
**Concepts:** each key term glossed in a phrase, as the author uses it.
**Steps:** numbered, in the paper's order; for each, what it is meant to establish (which part of the thesis), the
evidence (what corpus, how much, from where) and the interlocutor it leans on.
**What reaches the conclusion:** which parts of the thesis the steps carry, and which are only announced or dropped.
Never a bare chain of names.

## 3. Three axes — kept apart
Steelman: the strongest reading of the paper, in 1–2 sentences, before any criticism.

**A. Internal coherence** — sound / strained / broken
Does it hold on its own terms (premises and sources assumed true)? 1–4 findings, each:
[L|M|m] what — "anchor" (§) — why it is internal, not a disagreement.
Before calling two passages inconsistent, check that they use the term in the same sense (pilot, MB 27.10.2026:
modernity hiding the *order of oppression* and Roma becoming *more visible as a group* are two visibilities, not a
contradiction). This guards against misreading; it excuses nothing: when the author's own slide between two senses
does the work, the slide is the finding (MB 29.10.2026: the point is to read the text inside out, critically). An argument that thins as it goes (limbs of the thesis announced and dropped, detours that never
return to it, a conclusion that restates rather than draws) is an internal finding: say which parts reach the end.

**B. Method & evidence** — fit / stretched / unfit
Does the method carry the size of the claim? Overreach (quantify: "3 court cases → claim about the
Commonwealth"). Unstated assumptions. [FLAG-EXTERNAL] + the precise question, where a specialist is needed.
**Freewheeling** is MB's first concern in humanities papers (MB 27.10.2026): an interpretive leap presented as a
finding — an identification or attribution (who a figure is, a group membership read from iconography or a
memoir), an intention read into an author or a character, an absence claimed from the author's own search, a few
artists' or writers' view taken for society's. Name each, say what rests on it and rate it by that: [L] if the
thesis or a main section's conclusion needs it, [M] if one step does. Never leave one unrated.
**Four tests for claims of othering, gaze or racialisation** (MB 30.10.2026, on Máté & Raatzsch's Mueller essay, dropped):
- *Baseline:* is the group treated differently from the author's or artist's unmarked subjects? A trait found across the
  whole oeuvre or corpus (stylisation, nudity, sexualisation of all women) is no evidence of othering this group.
- *Falsifiability:* what would count against the thesis? If marking the group is othering and not marking it is erasure,
  no evidence can, and the claim is a stance, not a finding.
- *Period vocabulary:* a term judged by today's norms needs the alternatives the period offered; with none, its use
  shows the period's language, not the author's intent.
- *Stance vs evidence:* an advocacy or reparative stance is legitimate and not a flaw; its empirical claims still need
  sources. Weigh the evidence density (a few footnotes behind sweeping accusations is freewheeling, rated as above).

**C. Field standing** — advances / consolidates / derivative / contested / outdated
Grounded in retrieved sources only: reception (citations and their trajectory, reviews, rebuttals),
what it adds to the literature, consequential omissions (with evidence the omitted work is recognised).
Sparse field → say sparse.
Reception counts, second to merit (MB 29.10.2026): citations, their trajectory, reviews and rebuttals are a real
part of the Quality judgement, never above the read itself; a solid, little-cited text (a niche venue, another field,
a recent one) is still a find (MB 27.10.2026). Say how much the count weighs here, given the paper's age and venue. Who wrote the
paper (Romani or not), and whether newer work is Romani-authored or agency-centred, is no criterion: never a minus,
never a reason to prefer another text. An omission is consequential only if it changes the argument.

## 4. Fit with the concept
Which strand of `concept.md` it serves; what only this paper brings; which other candidates it talks to,
duplicates or contradicts (by slug).

## 5. For the Polish reader
- New in Polish? (author/argument already available in Polish, incl. SROM — grep `context/srom-abstracts.tsv` for the
  author, key terms and Polish/EN equivalents; cite vol. + title, or a search hit)
- Hooks and frictions from `polish-field.md` §4 that apply (only those that apply), each named in words with one
  line on what it means for this text, never by its number alone (MB 27.10.2026: "1; 3" could not be followed)
- Terms that will need a decision in translation

## 6. Scores (rubric below — one line of justification each)
| Quality | Fit | Value for Polish readers |
|---|---|---|
| n | n | n |

## 7. Verdict
CORE / STRONG / CONDITIONAL (on what) / OUT — and why, in 2–3 lines. An alternative named here is weighed on
merit, never on its author's background or on being newer.

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
- `19-2026/cards/black-bodies-white-bodies-gypsy-images-i` (Kovács, the pilot), MB 27.10.2026: no correction to the
  scores; agrees with the reading and the CONDITIONAL verdict, and finds the text weaker the further it goes (messy,
  meandering) — weaker coherence than the card gave. Zizek re-checked the scores the same day: Fit 4→3 (the 13.10
  fit lens), Value 3→4 (the Polish overlap is thematic only). MB's corrections are the rules above: § 2 as an argument
  map; 3A same-sense check and the thinning argument; 3B freewheeling rated by what rests on it; 3C reception
  secondary to merit, authorship and agency-centred readings no criterion; frictions in words.
- `19-2026/cards/noemie-ndiaye-black-roma`, MB 27.10.2026 (in his comments on the pilot): the Scapin-as-Rom reading
  is load-bearing, far more than Kovács's identifications: [M]→[L], Quality 4→3.

## Rules that bite most often
- Anchors are verbatim, in the original language, 5–10 words + nearest heading. Never paraphrase inside quotes.
- `check.py` reads any quotation of 4+ words as an anchor. Put titles of other works in *italics*, not in
  quotes, or they are reported as missing (short quoted terms are ignored).
- The internal read (3A) takes the author's premises as true. "I disagree" is not an internal finding.
- A claim about "the literature" or "the field" needs a retrieved source in Sources. Model knowledge may point
  where to look; it is never the evidence. Mark any unverified recollection [MK].
- Manuscripts (SUBMISSION) are confidential: search with short conceptual queries, never with passages.
- Say where the paper is sound. A card that only lists faults is a bad card.
- When `concept.md` says the volume has no editorial introduction, a weakness "the intro can frame" is not fixed: name
  the editor's or translator's note that would fix it, or let it count.
