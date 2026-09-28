# Decisions for MB — all SROM modules

Only what is still pending and only MB can decide. Any module appends. Whichever session receives MB's
decision on an item, or is asked to resolve it itself, **removes the item** once it is actually resolved; the
decision is recorded where it takes effect (Kanon, handover, handoff item, commit). No history here.

Rules:
- New item under **Open**: `## D<n> — <subject> (dd.mm.yyyy, <module>)`, then the question, the options, the
  module's recommendation, what it blocks, and where the detail is (file + item ID). Next free number: **D17**.
- A partial answer (item still open) is a new line under the item: `- dd.mm.yyyy DECIDED: … (MB)`.
- `MB-decisions-archive.md` keeps the text of items closed before 27.09.2026; it is not appended to.

**Needs MB now: nothing.**

## Open (scheduled, or waiting for a later moment)

## D3 — House style v2 / reducing the InDesign style set (27.09.2026, srom-typeset)
Stage 3 (typesetting). Deferred by MB until stages 1–2 are finished and tested; then a style discussion with MB and
the cleaned template as IDML. Detail: `srom-typeset/docs/HANDOVER-typeset.md` § 4.

## D5 — Translator credit: what is still open (27.09.2026, srom-tlumacz)
Curator skill updated (C1 items 1–3, 5). Waiting, by MB's decision, until the rest is finalised: showing the
translator on the WordPress page (C1 item 4) and the desktop upload of the new curator .skill.
Question before that upload: **is mu-plugin v2.3 the current one?** The .skill MB attached on 27.09 carried v2.0; the
update was built on the copy installed for Claude Code (v2.3, checked again 28.09.2026: `srom-scholarly.php` Version 2.3),
so uploading it brings v2.3 and locked decision #4 to desktop Claude. This is the skill's copy, not what runs on the site.
Detail: `curator-update-2026-09-27/CHANGES.md` ("Which version this is built on").
- 28.09.2026 DECIDED: the live site is old (untouched since about June 2026). No upload now: when the work here is
  finished, MB updates the curator skill in desktop Claude and the plugin on the site together. (MB)

## D6 (c) — Vol. 19 translation shortlist (27.09.2026, srom-tlumacz)
Deferred by MB (26.09.2026). (a) and (b) are closed.

## D15 — Licence: withdraw the CC BY-NC-ND option? (28.09.2026, srom-typeset)
Kanon § 13.2 marks it "DO ROZSTRZYGNIĘCIA – kolegium redakcyjne". Today the author chooses CC BY / BY-NC / BY-NC-ND
(default BY-NC). Options: (a) keep the choice; (b) withdraw ND, keep BY / BY-NC; (c) one licence for the whole journal.
srom-typeset's recommendation: (b) at least — ND rules out the DOAJ Seal (§ 13.2); (c) is the dominant practice.
Blocks nothing in stages 1–2; matters for the licence field of the master CSV and the Crossref deposit.
Kolegium's decision, via MB. Detail: `srom-typeset/.claude/skills/srom-kanon/references/kanon-redakcyjny.md` § 13.2.

## D16 — PILNE before any open-access announcement: vol. 18 copyright-transfer clause (28.09.2026, srom-typeset)
Kanon § 13.2: the printed *Informacje dla autorów* in vol. 18/2025 say authors transfer copyright to the Redakcja;
the licence agreement says the opposite. The text in print and on the website must be **replaced**, not supplemented.
Needed from MB: the replacement wording (or who writes it) and where it goes (website page; vol. 19 front matter).
srom-typeset can draft the Polish text on request. Blocks: the OA announcement. Detail: Kanon § 13.2.
