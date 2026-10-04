# Deep review — the staged pass, for finalists and doubtful cases only

MB's critical-review kit ("Ziziek critical_review_prompt_kit.md", kept in the workspace's `srom-zizek/_sources/` as the
original), adapted to run inside Zizek. Use it when a card is not enough: a finalist whose weakness could
sink the block, a manuscript that needs a real referee-grade read, or a card whose verdict MB doubts.
Expect one paper per session.

**Principle:** three axes — internal coherence, methodology, standing in the field — assessed separately
and recombined only in synthesis. "Internally inconsistent", "methodologically weak" and "wrong per the
field" are different verdicts on different evidence; never let one pass for another.

**Files:** each pass is saved as `volumes/<vol>/deep/<slug>-<pass>.md` as soon as it is done, so the
session can be compacted or resumed without losing work. Every pass file starts with the line
`deep · <pass> · <date> · text: text/<slug>.txt` so that `check.py` can find the text. Pass 5 updates
the paper's card (verdict, scores, a link to the deep review).

**Who runs what — the blind read.** By the time a paper gets a deep review, this session has usually read
its card, whose 3C section is full of field searches: an internal read done here would be contaminated by
exactly what the kit keeps out of it. So passes 0–2 are run by a **blind reader**: one fresh subagent
(general-purpose, run in the foreground) given only this file's passes 0–2 section, the path to
`text/<slug>.txt`, and the three output paths. Its brief says: do not open `cards/`, `concept.md`,
`context/` or anything else in the volume; use no search or web tools; read the whole text. Zizek then
checks the blind reader's work (Pass 0 check below) and runs 2b, 3, 4, the rebuttal and 5 itself.
If MB wants it, the blind reader can run on another model (Agent `model` parameter) — say so in the pass files.

**Search:** passes 0, 1, 2, 4 and 5 use no search tools at all (not even to "check one thing"). Only 2b
(targeted) and 3 (broad) search. The rebuttal opens only the sources the findings already cite.

**Anchors:** short verbatim quote (5–10 words) + nearest heading, page only if it survived extraction.
Run `python3 "$Z/check.py" volumes/<vol>/deep/<slug>-*.md` after each pass; fix every MISSING or CLOSE
anchor against the text before the next pass builds on it.

**Text:** the deterministic extraction in `text/<slug>.txt`. Before pass 0, check it: notes present and
numbered, no missing pages, hyphenation OK, running heads not mistaken for text. Author interviews or
correspondence, if any, are a labelled secondary source: they may inform methodology and synthesis, never
the coherence read.

---

## Pass 0 — Extraction ledger (no judgement) · blind reader
Record faithfully; where something is ambiguous, record the ambiguity. Anchor every entry.
- **A. Thesis** — central claim(s) in the author's words.
- **B. Subsidiary claims** — numbered; for each the claim, anchor, and the evidence offered (author's words).
- **C. Key-term ledger** — for each central term, *every* place it is defined or characterised (verbatim + anchor)
  and 2–3 places it is used in argument; differing wordings side by side, not judged.
- **D. Evidence inventory** — main empirical/textual findings and which claims (B-numbers) each supports.
- **E. Structural map** — one line per section: the move it makes.
- **F. Load-bearing citations** — the 3–6 references the thesis or a B-claim visibly rests on (a quoted
  authority, a borrowed finding, a statistic), each with what the paper says the source says (anchor).
Be exhaustive, especially in C. If the text is long, do it section by section rather than compress.

**Pass 0 check (Zizek, before Pass 1 starts).** The ledger is checked against the text, not against
memory: for each C-term, `grep -n -i "<term>" text/<slug>.txt` (and its variants: plural, adjective,
the author's other spellings) and scan the hits for a defining or characterising use the ledger missed;
record the hit count beside each term. Add what was missed; then run `check.py` on the ledger.

## Pass 1 — Internal coherence · blind reader
Assume every premise and cited source is true; no outside knowledge; do not judge whether the conclusion is
correct. Steelman first, then test:
1. **Definitional consistency** — incompatible definitions or silent shifts between senses of a term.
2. **Validity** — non-sequiturs, gaps, circularity, equivocation.
3. **Claim-to-evidence scaling** — claims stronger than the evidence *as presented*.
4. **Internal contradictions.**
Each finding: severity (LOAD-BEARING / MODERATE / MINOR), anchors, and one line on why it is internal rather
than a disagreement. Say where the argument is sound.

## Pass 2 — Methodology · blind reader
Work from the text. Where disciplinary-norm knowledge is needed, flag, don't resolve.
1. **Method-to-claim fit.** 2. **Overreach** (quantify the gap). 3. **Competence boundaries** — claims in a
method or subfield outside the author's evident competence (linguistic, statistical, archival, genetic…):
[FLAG-EXTERNAL] + the precise question. 4. **Smuggled assumptions** and researcher degrees of freedom.
Severity and anchors; note what is sound.

## Pass 2b — Resolve the flags (optional; targeted search)
Only the [FLAG-EXTERNAL] items: find the current disciplinary position for each specific question —
defensible / outdated / contested / wrong — grounded in a retrieved, citable source. No general survey.

## Pass 3 — Situating against the field (broad search)
Every claim about "the field" grounded in a retrieved source; contested areas flagged as contested; sparse
fields called sparse.
1. **State of knowledge** on the core questions, from citable sources.
2. **Coverage** — (a) ignored-and-consequential work (with evidence it is recognised) vs (b) defensible omissions.
3. **Misrepresentation** — where the text characterises prior work: quote it and the source it distorts.
4. **Citation audit** — the Pass 0 F list only. For each: does the reference exist as cited (Crossref
   `verify_reference`), and — where the source can be opened — does it say what the paper says it says?
   Verdict per item: *supports* / *weaker than cited* / *does not say this* / *could not open* (say why).
   A translation reprints the author's citations under SROM's name; this is where that risk is caught.
   (Bibliographic details — places, pages, editions — are srom-tlumacz's job later; here only whether
   the source carries the claim.)
5. **Positioning** — novel, redundant, or contradicted?
6. **Afterlife** (published papers): what has happened to it since publication. Citation trajectory and
   `retracted` flag (OpenAlex `get_paper`); corrections or errata; published responses or rebuttals
   (who cites it and how — OpenAlex `https://api.openalex.org/works?filter=cites:<W-id>`, then read the
   citing passages of the few that engage it); and **the author's own later work** — has a later book
   chapter or article revised, extended or superseded the argument? If so, which version should SROM
   translate? Sparse afterlife is a fact, not a flaw: say so.
7. **The Polish field** — what Polish-language work it should know, and what it means for Polish readers
   (`context/polish-field.md`; grep `context/srom-abstracts.tsv`).

## Pass 4 — Synthesis, draft (no search)
Keep the three axes labelled and separate.
1. Findings under Internal coherence / Methodology / Field standing.
2. The **load-bearing** failures, separated from peripheral ones.
3. For each: **fixable** by revision (or by an editor's note / translator's note) or **fatal** to the core claim.
4. Overall judgement with reasoning, and a fair statement of the contributions.
If the session has grown long, work from the saved pass files rather than memory.

## Rebuttal — the author answers (fresh subagent)
The kit's "surviving critiques are the ones that survive rebuttal", made real. One fresh subagent plays the
**author's advocate**: it gets the text, the Pass 4 draft's LOAD-BEARING and MODERATE findings (with
anchors and the sources each field finding cites) and nothing else, and for each finding writes the
strongest answer the author could give *from the text or from the cited source* — with anchors — or
concedes. Output: `deep/<slug>-rebuttal.md` (same header line as the pass files). Zizek then rules on each answer: **stands** / **downgraded**
(severity lowered, say why) / **withdrawn** (the text answers it). A rebuttal that only disagrees, without
anchors, changes nothing.

## Pass 5 — Synthesis, final (no search)
The Pass 4 draft revised by the rulings, each finding marked stands / downgraded / withdrawn, and:
- **For the block:** keep / keep with framing in the intro / drop — and what the intro must supply.
- **For a TRANSLATION:** the list the translation will need — editor's notes (findings "fixable by note"),
  figures or statistics to source, citations that failed the audit, the version to translate (Pass 3.6),
  terms needing a decision. This list goes into the card's section 8 and, once the paper is chosen, to
  srom-tlumacz.
- **For a SUBMISSION:** a separate section *Do autora* in Polish — the points to send, phrased as a
  referee would (what to fix, why, where), without SROM-internal matters (scores, block strategy, other
  candidates). MB edits it before anything is sent.
Then update the card (scores, verdict, link to `deep/<slug>-5.md`, a line on what changed and why).

## Tips carried over from the kit
- Steelman first; the rebuttal step then tests whether the critique survives.
- Keep passes 1 and 2 separate even though both are internal: merging them reintroduces the blending.
- A long book: the blind reader works chapter by chapter, saving each chapter's ledger before the next.
