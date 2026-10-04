# One repository, on the Mac and in the cloud: guide for MB (05.10.2026 00:42)

Since 05.10.2026 `SROM edit and trans` is **one git repository**, remote `blessero/srom-cloud` (GitHub, private).
Your Mac folder is a clone of it, and so is every cloud session. Both work on `main`: each session pulls before it
starts and pushes after every commit, so there is nothing to carry back and forth. `cloud.py` and its round-trip test
are retired (they lived until the export of 05.10.2026 00:31; `git log -- _cloud/cloud.py` shows them).
Rules for sessions: root `CLAUDE.md` § Cloud sessions.

## 1. The switch on the Mac (once)
Quit every Code session first; Cowork waits too (it writes into this folder).
1. Last carry with the old tool, from the old folder: `python3 _cloud/cloud.py sync`. It must end without a refusal;
   then GitHub holds everything, Cowork's newest items included.
2. In Terminal, in `CODE/SROM/`:
   `mv "SROM edit and trans" "SROM edit and trans.old"`
   `git clone https://github.com/blessero/srom-cloud.git "SROM edit and trans"`
   Same path as before, so `~/.claude/skills` links, hooks, project memory and Cowork's mount keep working.
3. Check, in the new folder: `git status` (clean), then both tests:
   `~/.venvs/srom/bin/python srom-produkcja/.claude/skills/srom-produkcja/tests/run_all.py` → SUITE ALL PASS,
   `~/.venvs/srom/bin/python srom-tlumacz/.claude/skills/srom-tlumacz/scripts/tlumacz-test_handoff.py` → HANDOFF
   CONTRACT n/n (all held),
   and `~/.venvs/srom/bin/python _handoffs/tools/mb_view.py --all` (rebuilds `_widok/`, which git does not keep).
4. When that passes: delete `../srom-cloud` (the old mirror). Keep `SROM edit and trans.old` a week, then delete it
   (the backup `CODE/_backup/srom-20261004-2120.tar.gz` stays).

## 2. Every day
- Any session, Mac or cloud, starts with `git pull --rebase origin main` and pushes after each commit (it does this
  itself; the rule is in root CLAUDE.md). Don't run two sessions of the same module on the same text at once.
- Cowork writes on the Mac and does not commit: the next Mac session commits and pushes its files. If you work only
  in the cloud for a while, open a Mac session now and then ("root: commit and push Cowork's changes"), or Cowork's
  items won't reach the cloud.
- A file a cloud session asks you to open: `git pull` in Terminal (or start a Mac session), then open it.
- Not in git: `_widok/`, `srom-produkcja/dist/`, `_migracja/build/` (all rebuilt when needed).

## 3. Cloud sessions
- Start each one with the module: "produkcja: …", "tlumacz: …", "root: …".
- The environment (claude.ai/code → environment `srom`), unchanged: Network **Custom** + "include defaults", add
  `api.crossref.org doi.org data.crossref.org api.ror.org www.wikidata.org query.wikidata.org api.openalex.org
  katalogi.bn.org.pl data.bn.org.pl lccn.loc.gov id.loc.gov lx2.loc.gov services.dnb.de portal.dnb.de studiaromologica.pl`;
  environment variable `TZ=Europe/Madrid`; setup script: all of `_cloud/setup-cloud.sh` (`check_pins.py` keeps its
  pins equal to the Mac venv and Cowork).
- The Claude GitHub app must stay installed on `srom-cloud`.
- Credit (claim by 07.10.2026, 23:59 US Pacific: `claude`, then `/claim-credit`): $100 for cloud sessions, spent at API
  prices (Opus $4 / $20, Sonnet $2 / $10 per million tokens in/out); a long Opus session ≈ $5–15. One clear, test-checked
  job per session; Sonnet for mechanical work, Opus for design; don't leave a session idle more than 5 minutes mid-work.
