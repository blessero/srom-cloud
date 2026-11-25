# The notes sheet `<id>_uwagi.md`: one per text (MB, 25.11.2026)

MB reads one sheet per text, laid out by what he does with it, not by the stage that wrote it. Model: Davis
(`workspace/srom-produkcja/work/davis/davis_uwagi.md`).

- **Where.** `workspace/srom-produkcja/work/<id>/<id>_uwagi.md`, for every text (translation or Polish original). RIP
  starts it; TRANS, the language pass, take-back, letters and every later session write into the same file. No second
  sheet in `srom-tlumacz/work/<id>/`: a text that still has two is merged the next time a session touches it (old
  sheets to `workspace/_archive/<date>/`). Biurko shows it as „Uwagi”.
- **Open items only.** When an item closes (MB decided, the author answered, it was applied or dropped), the session
  moves it, with date and reason, to `<id>_uwagi_log.md` beside the sheet, in the same session. The log is not on
  Biurko; it answers "where did X go". "Odśwież uwagi <text>" = re-read the ledger, `STATUS.md` and
  `korespondencja.tsv` and move everything closed to the log.
- **Language.** Part 1 in the author's language (English for a translated text, Polish for a Polish author),
  paste-ready: Biurko's reader copies a section with its formatting ("Copy"). Parts 2–3 in Polish, plain words.
- **Top line:** `Stan dd.mm.rrrr HH:MM.` only. No file lists, gates, tool output or stage history: those go to
  `STATUS.md` and the log.
- **S-items** (translator's `DO SPRAWDZENIA: S<n>` marks): their `- S<n> …` lines live in the log;
  `tlumacz-draft_check.py --marks` reads sheet and log together. The sheet names them only in brackets.
- **Letters.** `listy-do-autorow.md` holds only the composed letters, short; they carry part 1 pasted from the sheet.
  No separate `<id>_queries_for_author.*` from now on.
- **Links.** An item number (DAV-102) is written bare: Biurko's reader opens the item when it is open and greys it when
  closed. A cross-reference inside the sheet links its heading: `[1.5](#1-5-corrected-from-the-records-fyi)` (the
  heading id: lower case, spaces and dots to hyphens, at most 40 characters).

## Skeleton

```
# [<Author>] „<title>” — uwagi
Stan dd.mm.rrrr HH:MM.

## 1. Dla autorów (<language>, do wklejenia)
One line: what has gone to them and what has not (which letter, which item).
### 1.1 <the substantial matter of this text, if any>
  e.g. Pahulich: Grellmann's German against her quotations; Davis: sources we found. Omit when there is none.
### 1.2 Questions
  Numbered, one per item, bold lead with the note numbers; each answerable in a line.
### 1.3 Author note (draft for approval)          (R8; articles only)
### 1.4 Changed in the text, unless you object
### 1.5 Corrected from the records (FYI)
  | Note | As in the article | As corrected | Record |   (R1)

## 2. Dla Ciebie — otwarte
| | co | rekomendacja / stan |   one row per open ledger item of the text; the item itself is the full text
**Przy Twojej edycji Worda:** R6 choices and translator's notes MB enters himself.
**Czekamy na autorów:** … **Po odpowiedzi autorów (sesja, nie Ty):** …

## 3. Rejestr (FYI): co zrobione bez pytania i dlaczego
### 3.1 Poprawione bez pytania      R1 (→ 1.5), obvious slips (Kanon § 12.2.8), RIP deviations from print; each says what and where
### 3.2 Zostawione jak w druku      and why
### 3.3 Nie pytamy autorów          every query dropped: what it was and why, readable on its own
### 3.4 Terminy                     | angielski | polski | ile | podstawa |; sources in full (author, title, journal, year, link)
                                    under the table; terms settled earlier (HOUSE, MB's decisions) in one paragraph
### 3.5 Ustalone z Tobą i stałe dane   licence, volume, translator, the authors' grammatical forms if decided
```

Part 1 order is by weight: the substantial matter, then questions, then what MB only reports (records last). Sections
with nothing in them are left out.
