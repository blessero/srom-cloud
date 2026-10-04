# Cloud phase: guide for MB (04.10.2026)

This folder stays the home. `cloud.py` copies it (with the three repos' history and the data git keeps out) into a
GitHub mirror `srom-cloud`; cloud sessions work there; `import` brings their commits back as normal commits.
Backup taken first: `CODE/_backup/srom-20261004-2120.tar.gz` (`sh _cloud/verify_backup.sh` → BACKUP OK).

## 1. The credit (claim by 07.10.2026, 23:59 US Pacific; unused balance expires about 04.11.2026)
In a terminal: `claude`, then `/claim-credit`. $100 (Pro), for cloud sessions only, spent at API list prices
(Opus 5.5 $4 / $20 per million tokens in/out, Sonnet 5.5 $2 / $10). Rough value: a long Opus session like today's ≈ $5–15,
so 7–20 such sessions; about twice as many on Sonnet. Per dollar, the Pro plan buys more work than credit or paid extra
usage (both are priced at API rates). Whether cloud sessions spend the credit first or your plan first is not stated in
the docs: check claude.ai → Settings → Usage after the first session.
Spend it well: one clear, test-checked job per session; Sonnet for mechanical work, Opus for design; don't leave a
session idle more than 5 minutes mid-work (the cache expires and the whole context is billed again).
Best first jobs: SYS-10 (a) (make the skill files the same), then the three Cowork patches (review 04.10.2026).

## 2. One-time GitHub setup
1. github.com (account blessero) → New repository → name `srom-cloud`, **Private**, empty (no README).
2. claude.ai/code → connect GitHub → install the Claude app on `srom-cloud` only.
3. In Terminal, from this folder (the mirror is already built here, nothing pushed yet):
   `git -C ../srom-cloud remote add origin https://github.com/blessero/srom-cloud.git`
   `git -C ../srom-cloud push -u origin main`
4. claude.ai/code → environment → New: name `srom`; Network **Custom** + "include defaults", add:
   `api.crossref.org doi.org data.crossref.org api.ror.org www.wikidata.org query.wikidata.org api.openalex.org
   katalogi.bn.org.pl data.bn.org.pl lccn.loc.gov id.loc.gov lx2.loc.gov services.dnb.de portal.dnb.de studiaromologica.pl`;
   Environment variables: `TZ=Europe/Madrid`; Setup script: paste all of `_cloud/setup-cloud.sh`.

## 3. Working in the cloud
- First session, say: "root: run both modules' tests and report; read CLAUDE.md § Cloud sessions first."
  Expect SUITE ALL PASS 24/24 and HANDOFF CONTRACT 33/33 (pandoc there is 3.9, not 3.8.3: report any difference).
- Start each session with the module: "produkcja: …", "tlumacz: …", "root: …".
- While in the cloud, don't work in this folder (Cowork goes on as usual).
- Any time, in Terminal here: `python3 _cloud/cloud.py sync` (brings cloud work back, sends Cowork's new items out).

## 4. Coming back
`python3 _cloud/cloud.py import` → each module gets a "cloud import" commit; then work locally as before.
If it refuses ("this folder changed"), nothing was touched: ask a session to merge. Status: `cloud.py status`.

## 5. Cowork, once
1. In Cowork: connect the folder `/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans`.
2. Paste: "Read `_handoffs/code-to-cowork.md` in the Code folder you can now see, do K1 steps 1–6, answer as C1 in
   `_handoffs/cowork-to-code.md`, and tell me the line to add to srom-naczelny."
3. Upload the srom-naczelny change it gives you.
From then on "checkup" in Cowork follows `_handoffs/checkup/COWORK.md`.
