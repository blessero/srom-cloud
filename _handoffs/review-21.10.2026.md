# Checkup 21.10.2026 — milestone review (root session) [general]

Written 21.10.2026 03:44. Reviewer = root session, at MB's request ("system checkup … a lot of new stuff, some very delicate, to do
with slugs on site, things that can affect DOI registration"). Scope: the 15 commits since review 20.10.2026 (3579e7d..9caea09),
above all the URL work of the night (volume base `/tom/` → `/volumes/`, PDF names `SROM_` → `Studia_Romologica_`, the DOI
rewrite rule, mu-plugin v2.6–v2.8); tools, contract, channel, hygiene; MB's two notes (the host is seohost.pl, not Hostinger;
the folder name "SROM edit and trans"). Live site: two requests, 61 s apart (MB's IP had been blocked earlier that night).

## Conclusions
- **DOI registration is safe.** No DOI is deposited yet (K29), so nothing registered can break; the night's changes touch
  volume URLs (no DOI) and PDF names (the deposit is regenerated after them, GEN-129), never an article's landing address.
- Measured, not assumed: all 25 `landing_url`s in the vol. 17–18 CSVs are exactly `https://studiaromologica.pl/articles/{doi}/`,
  every suffix `[a-z0-9]{8}`; on the live site all 15 published articles have slug = DOI suffix and a permalink equal to the CSV's
  address, and a DOI page answers 200 itself (no redirect) with that canonical. The v2.6–v2.8 URL code reads sound (DOI rule ahead
  of the CPT's attachment rule, self-check rebuilds once, retired bases 301 with query kept); the harness covers it.
- Two guards were missing on the one irreversible step, the deposit: nothing checked that `landing_url` has that exact form, and
  `check_deposit.py --site` silently followed redirects (and paced 1.5 s on a site that blocks bursts). Both fixed in Apply.
- Cowork's C23 date bug is real (live: `citation_online_date` "2025" = the print year) and has a twin: the Importer fills a volume's
  `pub_date`, which everything else reads as the **print** date, from `pub_date_online`. Vol. 17 is safe (its Tom existed), but an
  auto-created Tom 19 would date its articles by the day they went online. Fixed: mu-plugin v2.9, Importer 2.3.1.
- The host: no Code knowledge file named it; Cowork's privacy-policy draft (GEN-113, unpublished) says the logs are kept by
  "Hostinger"; an old (July) session memory calls the site "the hostinger site". Now recorded: seohost.pl live, Hostinger staging only.
- The folder name: 38 mentions in 13 repository files, but also 7 skill links, the old CODE link, 29 Cowork files (two of them
  code), the srom-naczelny copy on claude.ai and the path-keyed session history. A partial rename makes the skills vanish silently
  and sessions fall back to stale claude.ai copies. Recommendation: leave it.
- Tests green on both sides; backup refreshed.

## Verdict lines as printed
- `SUITE ALL PASS 28/28` (HEAD 9caea09, before Apply); within it `MUPLUGIN ALL PASS 39/39`, `QUANT ALL PASS 62/62`, `KB ALL PASS 4/4`,
  `KANON ALL PASS 20/20`
- srom-tlumacz (run against 9caea09; no contract change since 3579e7d): `HANDOFF CONTRACT 35/35`; `selftest: 9/9 negative controls caught`;
  check_tb: `training quotes verified: 25/25`, `candidate rows: 12, each with a verified training quote`; draft_check --all: seven
  drafts `leftover 0`, marks equal, quotes all matched (ostendorf 43/43, steiner 18/18, tittel 34/34, tittelpta 10/10, westohueri 15/15)
- Live, 03:37:14: `GET /wp-json/wp/v2/srom_article?per_page=100&_fields=id,slug,link,status` → 200, `x-wp-total: 15`, 15/15 slug = suffix,
  0 mismatches; 03:38:15: `GET /articles/10.68100/n61tj1yi/` (redirects not followed) → 200, `server: LiteSpeed`,
  `<link rel="canonical" href="https://studiaromologica.pl/articles/10.68100/n61tj1yi/" />`, `citation_publication_date` 2025,
  `citation_online_date` 2025, `citation_pdf_url` still `SROM_18_2025_…` (expected until GEN-129)
- v2.8 under the new harness case: `FAIL dates: publication date = Tom print date, no citation_online_date` (the bug), v2.9 `ok`
- `BACKUP OK srom-20261021-0342.tar.gz: 1745 paths, sha256 verified, 161M`

## Findings
| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | `validate_master.py` does not check `landing_url`, the address deposited as each DOI's `<resource>`; the URL bases moved twice (`/artykul/`, `/tom/`) | `scripts/validate_master.py` (no landing check); `master_schema.md` #4 calls it "reference only" | will bite (first deposit pending) | srom-produkcja |
| 2 | `check_deposit.py --site` follows redirects (urllib default), so a deposited address that 301s passes as 200; paced 1.5 s on a site that blocks bursts | `check_deposit.py` `get()`, `time.sleep(1.5)`; K29 step 4 wants "200, no 301" | will bite | srom-produkcja |
| 3 | `citation_online_date` repeats the print date; no field on the site holds an article's online date (C23 assumed one) | `srom-scholarly.php` v2.8 l. 294–296; live n61tj1yi: both "2025"; Importer field groups | will bite (false metadata) | srom-produkcja |
| 4 | Importer fills volume `pub_date` (the print date for the mu-plugin, the cover's „Data publikacji”, Crossref's issued date) from `pub_date_online`, a mapping older than `pub_date_print` (07.10.2026) | `class-srom-imp-fields.php` l. 250, `class-srom-imp-runner.php` find_or_create_volume; Tom 17 = post 699 existed (GEN-123 trail), so only a new Tom is hit | will bite (vol. 19) | srom-produkcja |
| 5 | 4b0e7fa changed the Importer's slug defaults without a version or changelog line (still 2.3.0) | `srom-importer.php` header | cosmetic | srom-produkcja |
| 6 | The live host is recorded nowhere; Cowork's GEN-113 privacy draft names Hostinger as the host keeping the logs; an old session memory says "hostinger site" | KB l. 21; `workspace/gen/GEN-113_polityka_prywatnosci.html` („Dzienniki przechowuje dostawca hostingu, Hostinger”); memory `SROM-Elementor-2/srom-elementor-kit.md` | will bite (legal text; sessions asking for the wrong host) | srom-produkcja (KB, skill), Cowork (GEN-113), root (memory) |
| 7 | Stale text: KB "mu-plugin v2.5 in assets … the live site runs v2.3"; srom-quant "38-column schema"; srom-produkcja CLAUDE.md "python3 … miniconda with the packages" (no pikepdf there: cover tests fail outside run_all's venv); KB's hard-coded list lacks the site address | KB l. 68–71, 133–137; SKILL.md l. 155; `python3 -c "import pikepdf"` → ModuleNotFoundError | cosmetic | srom-produkcja |
| 8 | C21, C22, C23 have no status line in `code-to-cowork.md` (C22 committed in 6f9d915 without a K-item) | `grep -c` → 0 each | cosmetic | root (K31) |
| 9 | The old link `SROM/CODE/SROM/SROM edit and trans` is still there (deletion planned 15.10.2026) | `ls -la SROM/CODE/SROM/` | cosmetic | MB |

Not findings (checked): `SROM_DOI_PREFIX` is defined but unused (harmless; removing it could fatal any custom snippet that names it,
so it stays); DOI rule is lowercase-only by design (suffixes are lowercase; doi.org always sends the registered address).

## Last review's findings
Review 20.10.2026: #1–7, 10–13 fixed there; #8 (`.bak`) done (K26: 404); #9 (vol. 17 before its deposit) decided (a), GEN-123 waits for
the vol. 18 deposit; #14 (2.3 GB old backups) still with Cowork/MB (GEN-116). For MB 1 done (K26), For MB 2 decided (K26).

## For srom-produkcja
1. `srom-quant/scripts/validate_master.py`: error when a row with a final DOI has `landing_url` ≠ `https://studiaromologica.pl/articles/{doi}/`;
   test in `test_quant.py` (old base, no slash, www fail; exact form passes). Vols 17 and 18 must still validate clean.
2. `srom-quant/scripts/check_deposit.py --site`: never follow a redirect; report `301 → <Location>` as a fault; pace 5 s (`SROM_PACE`
   for tests); docstring and srom-quant SKILL.md step 8a; test with a local server (301 fails, 200 passes).
3. mu-plugin v2.9: drop `citation_online_date`; header, `[srom_diag]` version; harness case (publication date = the Tom's print date, no
   online date) that fails on v2.8.
4. Importer 2.3.1: volume `pub_date` from `pub_date_print` (preset and auto-created Tom); version, changelog (with 4b0e7fa's defaults),
   HANDOVER table; guard + `php -l` in `test_muplugin.py`.
5. Knowledge: KB § Identity "Website" gains the host (seohost.pl live; Hostinger staging only) and the request pacing; KB § DOIs mu-plugin
   versions; KB hard-coded list gains the site address; srom-quant § Live-surface inventory the same host and pacing facts;
   srom-quant "38-column" → 40 + 2 optional and the landing check; srom-produkcja CLAUDE.md python3 line.
Verify: `run_all.py` → SUITE ALL PASS 28/28.

## For srom-tlumacz
Nothing.

## For MB
1. **Upload with GEN-129 step 3** (no extra trip): `srom-quant/assets/srom-scholarly.php` v2.9 instead of v2.8 (one wrong meta tag
   gone). **Before vol. 19's first import:** SROM Importer 2.3.1 (three files). Cowork enters both in the ledger (K32).
2. **GEN-113 (privacy policy):** the draft names Hostinger; Cowork changes it to seohost.pl before you approve. Give the hosting
   company's name as it should appear (the legal name on the seohost.pl invoice).
3. **Optional, your call:** a real online date on article pages (Scholar's `citation_online_date`; DOAJ recommends dates on each
   article): one ACF field on the Tom added by hand (a minute), one Importer mapping, one mu-plugin line, tests. Cheapest: nothing
   (v2.9 just leaves the tag out).
4. **Folder name:** leave "SROM edit and trans" (measured above). If ever wanted: one sitting with every session closed (move, re-link
   the skills, Cowork's paths, re-upload srom-naczelny), about an hour.
5. Cosmetic: delete the old link `SROM/CODE/SROM/SROM edit and trans` when convenient (planned 15.10.2026).
