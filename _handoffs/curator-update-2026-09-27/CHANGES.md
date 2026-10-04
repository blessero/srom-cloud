# srom-scholarly-curator — translator credit (C1), 27.09.2026

Done by srom-tlumacz at MB's request (there is no separate curator chat). Request: `../tlumacz-to-curator.md` C1.

## What changed (4 files, 45 lines; full diff in `changes.patch`)

| File | Change |
|---|---|
| `scripts/validate_master.py` | New **optional** column `translators_struct` (not required, so older CSVs stay valid). Warns if `is_translation`=`TAK` has no translator, or a translator is given without `TAK`. **Blocks** if a translator segment is not 4 pipe-fields. |
| `scripts/generate_crossref_xml.py` | After the authors, one `<person_name sequence="additional" contributor_role="translator">` per translator (ORCID and affiliation as for authors). No column → no change. |
| `references/master_schema.md` | Row 39 `translators_struct`. |
| `SKILL.md` | Three short notes (schema, generator, validator). |

**Not changed:** the mu-plugin `assets/srom-scholarly.php` (byte-identical), the Importer, and Elementor. WordPress does not show the translator yet (see "Not done" below).

## Tests (run from the packaged `.skill`): 11/11

- A legacy CSV (38 columns) gives XML **identical** to before. Its validator exit code is unchanged, with one new warning on a translated row that has no translator.
- A CSV with the new column differs from before only by the translator `<person_name>` elements (2 of 2 in the fixture).
- Warning, warning and blocking cases each triggered as intended.
- Both XMLs validate against the official Crossref **5.4.0 XSD** (gitlab.com/crossref/schema, run offline with xmllint). The negative control (role `interpreter`) is rejected, and the schema's own error message lists `translator` among the allowed roles.
- The mu-plugin is byte-identical to the installed one.
- `contributor_role="translator"` is confirmed by three sources: Crossref's markup guide *Contributors*, `common5.4.0.xsd` line 1392, and the validator run above.

## Which version this is built on — please check

The file you attached (`Downloads/srom-scholarly-curator.skill`) is **older** than the copy installed for Claude Code (`~/.claude/skills/srom-scholarly-curator`):

- mu-plugin **v2.0** vs **v2.3**;
- `section_label` without vs with locked decision #4 (generic `Część I–IV`);
- no "Component manifest" / "Live-surface inventory" sections in SKILL.md.

The two scripts were identical in both. **The update is built on the newer, installed copy.** If your desktop Claude still has the older version, installing the new `.skill` there also brings the v2.3 mu-plugin text and decision #4 into desktop. That is only the skill's copy of the file, not what runs on the site. Confirm that v2.3 is the current one.

## Files here

- `srom-scholarly-curator.skill` — the updated skill; upload it to desktop Claude (Settings → Capabilities → Skills), replacing the old one.
- `backup-installed-before-2026-09-27.skill` — the installed copy exactly as it was before this change; reinstall it to roll back.
- `changes.patch` — the diff between the two.

Claude Code: already installed (`~/.claude/skills/srom-scholarly-curator` now matches the package).

## Not done (needs a decision; would touch the site)

To show the translator on the landing page, three things would be needed: an ACF field `translators_display` (Importer model), the Importer mapping, and a mu-plugin shortcode or meta line. That touches live WordPress and the Importer (wp-acf-plugin-builder). It is left for a separate, deliberate step.
