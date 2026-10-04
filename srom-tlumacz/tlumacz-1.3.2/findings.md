# 1.3.2 Vol. 19 vocabulary: findings (29.09.2026 14:10) [general]

Shortlist (MB 29.09.2026): Ndiaye, Ostendorf, Pahulich, Tittel (drafted), West Ohueri (source frozen, not started).
Measured with `vol19_terms.py` (25 probes; table `vol19-concordance.tsv`); every flag read in context; vol. 18
precedent checked in `sources/vol18-md/`. Drafts were read, not edited.

## 1. Result

- 25 probes: consistent 16, single 5, flagged 4 (3 divergent, 1 missing). After reading the flagged ones in context:
  **2 real divergences** (P08 against vol. 18 precedent; P15 against HOUSE C-0018), 2 not faults (P19 a style choice,
  P25 a counting artefact). Two more divergences found by the precedent check, outside the probe verdicts: *Soviet*
  (P09; single in vol. 19, but the vol. 18 translation used „radziecki”) and *nomadism* (P24; single, Tittel
  „nomadyzm” vs vol. 18 „koczownictwo”).
- The vol. 19 drafts agree with each other and with the HOUSE rows on the rest: urasowienie, antycyganizm, matryca
  rasowa, kapitalizm rasowy, biała supremacja, zniewoleni (except P15), czarni/biali lower case, „Murzyn” only in
  period voice, „Egipcjanie” in quotation marks for early-modern *Egyptians*, włóczęgostwo, rdzenni, dzicy,
  „Cyganie” in quotation marks for the author's scare-quoted "gypsy" (Tittel, Ostendorf; MB decides in D25).

## 2. Flagged probes, reviewed

| id | verdict | reading in context | action |
|---|---|---|---|
| P08 | divergent | *nomadic lifestyle*: Ndiaye „koczowniczy tryb życia”; Pahulich „wędrowny tryb życia” (3×) but „koczowania”, „koczowników”, „koczownicy” elsewhere in the same draft. Vol. 18 precedent: *nomadic* → „koczowniczy” (Marushiakova/Popov 6×, Fotta 1×); *itinerant/peripatetic* → „wędrowny” (Fotta 3×). | Rows C-0046, C-0047 (PROVISIONAL, precedent quoted); D26 (a). Pahulich's draft deviates from precedent. |
| P15 | missing | Tittel: "lifelong enslavement" (the 1547 English statute's punishment) → „dożywotnie niewolnictwo”. HOUSE C-0018: *enslavement* → „zniewolenie”; *slavery* (the institution) → „niewolnictwo”. As a punishment, „dożywotnia niewola” or „dożywotnie zniewolenie” fits better. | D26 (b), pointer to D25. |
| P19 | divergent | *entanglement(s)*: Pahulich „splątanie” (title, 6×); Ostendorf 1× „splot”, inside her weaving metaphor (veil, weft, fabric). | Not a fault: style within one text. No row. |
| P25 | divergent | Artefact: Ndiaye's one *itinerant* is a pilgrimage, rendered with the verb („pielgrzymować”, no alternative needed); the script counts alternatives over the whole file, so Ndiaye's „koczowniczy” (P08) shows here too. | None. Limitation noted in § 4 (L4). |

Also read (not flagged by the script): P07 Tittel *sedentariness* (a state) → „osiadłość” — a different concept from
*sedentarization*, probe narrowed; P20 Tittel "belonging to" (verb) — probe narrowed to the noun.

## 3. Termbase (PROVISIONAL, awaiting MB: D26)

C-0041 antyczarność · C-0042 uinnienie (othering; closes C-0024's OPEN member) · C-0043 białość · C-0044 przynależność
(West Ohueri decides *racial belonging*) · C-0045 antyromski (kept apart from antycyganizm) · C-0046 koczowniczy ·
C-0047 wędrowny · C-0048 sowiecki (or radziecki: MB) · C-0049 osiedlanie (trap: the 1964 action).
Not admitted (obvious, or single-text choices already in D22/D23/D25): włóczęgostwo, rdzenni, dzicy, kolonialność,
splątanie, mobilna biedota, wolni kolorowi, skrypty rasowe.

**West Ohueri, before its intake** (source read for terms only): *whiteness* 64× (C-0043; *peripheral whiteness* →
„peryferyjna białość”?), *racial belonging* 16× and *non-belonging* (C-0044, open), *blackness* 11× lower case
(C-0013), *Ottomanness*, *Albanianness*, *Europeanness* (-ość forms), *Balkanism*. **Trap:** *Egyptians* (22×) there
are the present-day Balkan group (kartoteka „Egipcjanie (bałkańscy)”), **not** the early-modern designation that the
other drafts put in quotation marks (D13). Albanian *jevg*, *jevgjit* are exonyms (§ 3.4, T24).

## 4. Lessons for the module

- **L1 Duplicated checks.** Each parallel session wrote its own draft checker (`ndiaye/leftover_en.py`,
  `ost_check.py`, `pah_check.py`, `tit_check.py`: leftover English, `DO SPRAWDZENIA: S<n>` vs notes sheet, quotes vs
  quotes sheet), with copy drift (`tit_check.py` names gates 1.5.4b; it is 1.5.5b). → One shared checker (leaf 1.4.2a).
- **L2 Parallel sessions.** ID collisions (D21 → D22; srom-typeset's second T20 → T21) and a "not started" status
  line overtaken by a parallel session (T18). The rules already say: re-read before appending, commit at once. To add
  (MB): a session claims a text in HANDOVER § 7 before starting, and takes the next free D-number from the file at the
  moment of writing.
- **L3 Precedent quotes of non-HOUSE rows were not checked.** Fixed in `tlumacz-check_tb.py --precedent` (second output
  line); rows promoted by MB now arrive with verified quotes.
- **L4 Harvest gaps.** Leaf 1.3.1 missed *nomadic*/*itinerant* and *Soviet* (its harvest list was fixed in advance).
  The concordance catches such gaps only for probed concepts, and counts alternatives per file, not per occurrence
  (P25). When West Ohueri is drafted: re-run, add probes for its terms, and add vol. 18 as a column.
- **L5 Intake vs draft.** Intake tables are not updated after drafting (Pahulich: intake „ubodzy w drodze”, draft
  „mobilna biedota”). The notes sheet (`<id>_uwagi.md`) is the record of the draft's choices; intake is the plan.
  Template line to add at 1.4.3.
- **L6 One Kanon gap raised twice**: the annotation for a quotation translated from someone else's published English
  translation („tłum. z przekładu angielskiego”, without „autorki”): Ostendorf (E17, D22), Pahulich (S9, D23). One
  decision covers both; pointer in D26 (c).
- **L7 Cross-text visibility.** Per-text sheets hold each draft's choices; nothing showed the volume until this
  concordance. With the PROVISIONAL rows, the next draft's termbase lookup sees them.
