# Block — from cards to the 4–5 papers that make the strongest whole

A block is not the five best cards. It is the set that together makes an argument no single paper makes,
without one dead weight and without two papers saying the same thing. Work from the **cards**, not the
full texts (that is what makes a dozen candidates manageable); open a text only to settle a specific doubt.
Output: `volumes/<vol>/block.md`.

## Steps

1. **Calibrate the cards.** First run `python3 "$Z/check.py" volumes/<vol>/cards/*.md` and fix what it
   reports (cards by subagents misquote too). Then a table of every carded candidate: 3 scores + verdict +
   one-line claim + MB's view where recorded. Cards written in separate sessions drift; read them side by
   side and correct scores that are out of line with the rubric and the calibration anchors in `card.md`
   (note each change and why in the card itself). Drop OUT verdicts from what follows, but list them.

2. **Relations.** For the plausible candidates (normally STRONG/CORE, plus CONDITIONAL worth a look), one
   line per meaningful pair: *complements* (what together they show) · *duplicates* (keep which?) ·
   *productive tension* (they disagree in a way worth staging) · *talks past*. Only pairs that matter —
   not a full matrix.

3. **Two or three alternative blocks** of 4–5, each with a different logic (e.g. the most coherent /
   the most provocative / the one most anchored in Polish material). For each:
   - **Through-line**: one paragraph — the argument the block makes. (This is the seed of the editorial intro.)
   - **Order**, with one line on why this order (the order is part of the argument).
   - **What it gains, what it loses**, which strands of the concept stay empty.
   - **Weakest link** and what happens if it falls out.

4. **Stress tests** — run each on every option, report only what they find:
   - *Remove-one*: is every paper load-bearing for the through-line?
   - *Archive*: does it repeat a past SROM block or article (`context/srom-archive.md`; grep `context/srom-abstracts.tsv` for the argument itself, not just the title)? Does it continue a
     thread usefully (e.g. vol. 18 → 19 → this)?
   - *Polish reader*: after reading the block, what does a Polish reader know that they did not?
   - *Voices*: composition facts — Romani / non-Romani authors, Polish / foreign, translation / original,
     gender, discipline, career stage. State them; do not weigh them (see step 6).
   - *Skeptic*: the strongest criticism a hostile reviewer would make of the block as a whole.

5. **Recommendation.** Which option and why, in a short paragraph — and what would change it
   (e.g. "if the rights for X fail, option B").

6. **To discuss with MB — the non-scholarly considerations.** MB asked (30.09.2026) to be reminded that
   selection is not only scholarly and that this has to be discussed. Never make the final call without it.
   Collect here the facts from each card's section 8 and ask MB to go through, at least: rights and fees ·
   length and translation effort, translator capacity · author relations, commitments already made ·
   balance and representation (step 4 facts) · institutional and political sensitivities · funding or
   evaluation requirements · links to the Tabor conference or other SROM events · MB's own conflicts of interest.
   Record MB's decisions here with the date.

7. **Brief for the intro and the translation** — only after MB has chosen. One short section per chosen
   paper, collected from its card (§ 5, § 8) and deep review (Pass 5), not written anew: what the editorial
   intro must supply (Polish material, framing of a known weakness); editor's or translator's notes the
   paper needs; the version to translate; terms that need a decision; anything the author must be asked.
   Then the through-line of the chosen option, revised to the final set and order — the skeleton MB's
   *Wstęp* can grow from. Zizek then opens each chosen paper's section in `MB-decisions.md` (workspace root; a text code per
   paper, e.g. `PAH`: propose one) and its section in `STATUS.md`; the text goes on to RIP (srom-produkcja) and TRANS
   (srom-tlumacz), which take these items from there.

## Rules
- Relations and block logic are Zizek's judgement: argue them, don't just list them.
- If no option reaches four strong papers, say so plainly and say what to look for (feeds back into
  `concept.md` step 6), rather than padding the block.
