# Checkup 20.10.2026 — milestone review (root session) [general]

Written 20.10.2026 01:39. Reviewer = root session; at MB's request ("resolve as much as you can") it also fixed what needed no
decision (commits 97b6c0b, 26cfc4c, 54f464b, 3579e7d, c6065c0). Scope: tools, contract, Kanon, channel, hygiene, plus the
live site's plugin surface (read-only) and the 20.10.2026 audit of the mu-plugin's fatal catcher.

## Conclusions
- Tools green on both sides: SUITE ALL PASS 28/28 (new: MUPLUGIN), HANDOFF CONTRACT 35/35. Nothing blocks a module.
- Cowork's back-catalogue build (C19/C20) was sound but had real defects, all fixed here: bogus DOI metadata on no-DOI
  articles, body classes leaking onto archive grids, a wrong volume licence for mixed volumes, a recursion fatal in
  `[srom_flipbook]`, and ORCIDs matched on partial names. All are fixed in mu-plugin **v2.5** and rip_volume.py, with tests.
- The audit's conclusion stands: the v2.3 fatal catcher and `?srom_off=1` are removed (v2.5). Corrections to the audit: the
  LiteSpeed Cache plugin is not active (no cache risk); `debug.log` is already refused by the host (403), so WP_DEBUG_LOG is safe;
  `srom-loops.php.bak` is publicly downloadable (200) — delete it.
- Live site still runs v2.3; GEN-122 now uploads v2.5 (K25).
- One sequencing problem for MB: vol. 17's import would put unregistered DOIs on the site (K25 item 2).
- Backup refreshed (was 12 days old).

## Verdict lines as printed
- `SUITE ALL PASS 28/28` (HEAD 3579e7d); within it `BACKCAT ALL PASS 28/28`, `QUANT ALL PASS 54/54`, `MUPLUGIN ALL PASS 25/25`,
  `CHECK ALL PASS 82/82`, `KANON ALL PASS 20/20`
- srom-tlumacz (contract test run against 42a9643, before this review's commits; none touched its files): `HANDOFF CONTRACT 35/35`;
  `selftest: 9/9 negative controls caught`; check_tb: `training quotes verified: 25/25`, `candidate rows: 12, each with a verified training
  quote`; draft_check --all: tittel, tittelpta, westohueri `leftover 0`, marks equal, quotes all matched
- `php -l`: `No syntax errors detected` (PHP 8.5.8 local; site PHP 8.3.35)
- harness on v2.4 (baseline): 2 FAIL, then `Maximum call stack size … reached` (flipbook self-reference)
- vol. 17 scratch deposit: `DEPOSIT CHECK OK 10/10`; validate_master: `✓ no blocking errors`
- `BACKUP OK srom-20261020-0134.tar.gz: 1397 paths, sha256 verified, 161M`

## Findings
| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | No-DOI article printed `dc.identifier "doi:"` and `"identifier":"https://doi.org/"` | srom-scholarly.php v2.4 l. 270, 289–290; harness | will bite (Scholar ingest of every back volume) | fixed 26cfc4c |
| 2 | srom-no-* body classes taken from the first post of an archive (srom_ctx_id fallback) → rows hidden on every grid item | v2.4 § 8 body_class; harness "archive" cases | will bite | fixed 26cfc4c |
| 3 | `[srom_volume_license]` ignored rights-reserved articles: vol. 17 shown as CC BY-NC 4.0 | v2.4 srom_volume_licences; vol. 17 003 NONE | will bite (false licence claim) | fixed 26cfc4c |
| 4 | `[srom_flipbook]` recursed when flipbook_shortcode contains it | harness: stack-overflow fatal on v2.4 | cosmetic (needs an editor's typo) | fixed 26cfc4c |
| 5 | Fatal catcher (public log URL) + `?srom_off=1` (anyone unscopes grids) still in v2.4 | v2.4 l. 68–97, 483 | will bite | removed, v2.5 |
| 6 | rip_volume ORCID lookup by substring | 89 partial-name hits on autorzy.tsv | will bite (vols ≤ 16 rely on the register) | fixed 26cfc4c |
| 7 | rip_volume re-run silently overwrote hand edits in the master CSV | code; test "names the CSV cells it changes" | will bite | fixed 26cfc4c |
| 8 | `srom-loops.php.bak` publicly downloadable | HTTP 200, 5555 B; no secrets inside | cosmetic | MB (K25 1) |
| 9 | Vol. 17 import (GEN-123) before its deposit publishes 10 dead DOI links, against BACK-CATALOGUE.md's own rule | CSV doi filled; V18-107 not done | will bite | MB (K25 2) |
| 10 | C17's check.py change committed without its test | no ebd case in tests | cosmetic | fixed 54f464b |
| 11 | Stale text: schema "38 columns + 1" (40 + 2); KB "until the next Kanon version" (v1.17 done); SKILL.md lacked the three new scripts | files | cosmetic | fixed 26cfc4c |
| 12 | C16–C20 had no status line in code-to-cowork.md | channel files | cosmetic | fixed c6065c0 (K24) |
| 13 | backup.sh missed the memory of sessions started in SROM/Redakcja (the recommended start) | glob | cosmetic | fixed 3579e7d |
| 14 | 2.3 GB of June–July backups from an inactive plugin in wp-content (protected, 403) | list-directory | cosmetic | Cowork GEN-116 (K24) |

## Last review's findings
Review 07.10.2026: every item has its status line in both module files (Status of review 07.10.2026, 08.10.2026); For MB 1–5 done
(vol. 18 released, K11 decided (a), cleanup done 08.10.2026). Cowork's review 14.10.2026: its Code items (C15) answered in K22/K23.

## For srom-produkcja
Nothing. (Open, not urgent: C17 requests 1–2; the C17 Kanon wording waits for the next Kanon version that carries a rule change.)

## For srom-tlumacz
Nothing.

## For MB
1. K25 item 1 (GEN-122): upload v2.5, delete `srom-loops.php.bak`, switch on WP_DEBUG_LOG for a week (wp-config, display off).
   Then say "done" in a session that checks the pages and `debug.log`.
   Run with: Sonnet · medium effort — post-upload checks follow a written procedure.
2. K25 item 2: vol. 17 — (a) recommended: V18-107 first, then import vol. 17 and deposit it the same day.
   Run with: Sonnet · high effort — CSV/DOI/Crossref work.
