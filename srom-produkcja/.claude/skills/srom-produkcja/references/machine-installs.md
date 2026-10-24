# What the SROM suite has installed on MB's Mac (register)

*Compiled 24.10.2026 22:45 by a Code session from the machine itself (launchctl, `~/.claude`, `~/.venvs`, `~/Library`)
and from `tools/setup_mac.sh`, `tools/install_scripts.sh`, `setup.sh`, `requirements.txt`. No earlier list existed.
Update this file in the same change as any new install; one row per item, with how to remove it.*

Scope: everything **outside the git repository** that a SROM session put on the Mac and that keeps running, loads
automatically or has to exist for the toolchain to pass its preflight. The repo's own files are not listed. Cowork's
Linux VM (`setup.sh`: pandoc into `~/.local/bin`, fonts, `npm -g acorn`) is rebuilt every session and is not on the Mac.

## 1. Runs by itself (check these first)

| # | Item | What it does | Where | Installed | Remove |
|---|---|---|---|---|---|
| 1 | **launchd agent `pl.srom.ikonograf-pobierz`** | runs `pobierz.py` every 300 s (and at load): does the downloads Cowork lists in `work/<id>/ikonografia/pobierz.tsv` (curl, `sips` for 800 px thumbnails), logs to `pobierz.log` beside the list. Python is `/usr/bin/python3` (3.9.6, standard library only). Refuses `studiaromologica` and `seohost` hosts itself. | `~/Library/LaunchAgents/pl.srom.ikonograf-pobierz.plist` (a **copy** of `srom-ikonograf/scripts/pl.srom.ikonograf-pobierz.plist`, identical); stderr log `~/Library/Logs/srom-ikonograf-pobierz.log` | 24.10.2026 (srom-ikonograf, K38) | `launchctl unload ~/Library/LaunchAgents/pl.srom.ikonograf-pobierz.plist`, then delete that file (the log may go too). The repo copy and `pobierz.py` stay: they can be run by hand. |
| 2 | **Claude Code hook `srom-throttle`** (live-site pacing + breaker) | before/after every Bash, WebFetch and `mcp__*` call it paces requests to studiaromologica.pl / seohost.pl (5 s gap, 150/h), and trips a breaker on 403/429/503/Wordfence/timeouts. Does **not** see `pobierz.py` (which refuses those hosts itself). | script `~/.claude/hooks/srom-throttle.py`; wired in `~/.claude/settings.json` (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, matcher `Bash\|WebFetch\|mcp__.*`); state in `~/.claude/srom-throttle/` (`state.json`, `lock`, `TRIPPED`; optional `config.json`, absent = defaults) | 22.10.2026 (after the IP blocks of 21.10 and 22.10) | delete the three `srom-throttle` entries from `hooks` in `~/.claude/settings.json`; then the script and the state folder. Status: `python3 ~/.claude/hooks/srom-throttle.py --status`. **The breaker is TRIPPED (22.10.2026 17:01); clear it (`--clear`) only on MB's word.** |
| 3 | Project hooks `guard_module.py` (srom-produkcja, srom-tlumacz) | stop a module's session editing the other module's files (PreToolUse on Edit/Write). Exits silently if `_handoffs/tools/hooks/guard_module.py` is missing. | `srom-produkcja/.claude/settings.json`, `srom-tlumacz/.claude/settings.json` (in git; uses `/usr/bin/python3`) | 2026 (repo) | in git: edit those two files. |

Doubt to carry: `~/.claude/hooks/srom-throttle.py` and `~/.claude/srom-throttle/` are **not in git**. The only copy is on the Mac
(and whatever the `claude-backup` agent syncs, see § 5). If the hook is to survive a new machine, it has to be added to the repo.

## 2. Links into other programs (symlinks, nothing copied)

| Item | From → to | By | Remove |
|---|---|---|---|
| Claude Code skills (7 srom/wp links) | `~/.claude/skills/{srom-ikonograf, srom-kanon, srom-produkcja, srom-quant, srom-zizek, wp-acf-plugin-builder, wp-elementor-builder}` → `…/SROM edit and trans/srom-produkcja/.claude/skills/<name>`; `~/.claude/skills/srom-tlumacz` → `…/srom-tlumacz/.claude/skills/srom-tlumacz` | `tools/setup_mac.sh` (08.10.2026); `srom-ikonograf` linked 24.10.2026 | `rm` the link only (never `rm -r` it: that follows into the repo). |
| InDesign scripts (3 links) | `~/Library/Preferences/Adobe InDesign/Version 21.0/en_GB/Scripts/Scripts Panel/{srom_style_setup, srom_final_pass, srom_zakladki}.jsx` → `srom-produkcja/.claude/skills/srom-produkcja/indesign/` | `tools/install_scripts.sh` | `rm` the links. An article's own scripts go to a panel folder `srom_<stem>/` (none present now). A real file it replaced is moved to `…/Scripts/replaced/`. |

## 3. Packages the toolchain needs (srom-produkcja preflight: `tests/run_all.py` → `SUITE ALL PASS`)

**Run the preflight with the venv's Python** (`~/.venvs/srom/bin/python`). The system `python3` is 3.9.6 with none of these,
and `/opt/miniconda3` has docx/lxml/PyMuPDF **1.28.0** (not the pinned 1.28.2) and no pikepdf: do not use it for SROM.

| Item | Version now | Pinned / required | Where | How installed | Remove |
|---|---|---|---|---|---|
| Python 3.13 (Homebrew `python@3.13`) | 3.13.15 | >= 3.10 | `/opt/homebrew/bin/python3.13` | `brew install python@3.13` (setup_mac.sh) | `brew uninstall python@3.13` (other things may use it) |
| venv `~/.venvs/srom` | Python 3.13.15 | — | `~/.venvs/srom/` | `tools/setup_mac.sh` | `rm -r ~/.venvs/srom` (re-create with `sh srom-produkcja/tools/setup_mac.sh`) |
| python-docx | 1.2.0 | `==1.2.0` | venv | `requirements.txt` | with the venv |
| lxml | 6.1.3 | `==6.1.3` | venv | `requirements.txt` | with the venv |
| PyMuPDF | 1.28.2 | `==1.28.2` (PDF extraction depends on its behaviour) | venv | `requirements.txt` | with the venv |
| pikepdf | 10.16.0 | `==10.16.0` (Py >= 3.11; 10.13.0.post1 for 3.10) | venv | `requirements.txt` | with the venv |
| pillow, packaging, typing_extensions | 12.3.0, 26.3, 4.16.0 | not pinned (pulled in by the above) | venv | pip | with the venv |
| acorn (npm) | present | latest; optional (ES3 test of the InDesign scripts; a weaker parser if absent) | `~/.venvs/srom/node/node_modules/acorn` | `npm install --prefix ~/.venvs/srom/node acorn` | with the venv |
| pandoc | 3.8.3 | >= 3.1 (tested 3.8.3) | `/usr/local/bin/pandoc` (root-owned: a package installer, **not** Homebrew) | not by a SROM script; `setup_mac.sh` only checks for it | `sudo rm /usr/local/bin/pandoc` (MB) |
| node | v22.17.1 | any; only for acorn | `/usr/local/bin/node` (installer, not Homebrew) | not by SROM | — |
| LibreOffice | 26.8.0 (Homebrew cask) | optional: only `tests/test_pdf.py`; reports SKIP without it | `/Applications/LibreOffice.app`, `/opt/homebrew/bin/soffice` | `brew install --cask libreoffice` | `brew uninstall --cask libreoffice` |
| `sips`, `curl`, `/usr/bin/python3` | macOS built-ins | used by `pobierz.py` | system | — | — |
| Adobe InDesign 2026 (v21) | present | needed for the INJECT scripts | `/Applications/Adobe InDesign 2026/` | MB's licence, not a SROM install | — |

Fonts for `cover_page.py` (srom-quant): IBM Plex Sans is found in `~/Library/Fonts/FontBase/` (FontBase, MB's font manager;
not installed by SROM). Other cover fonts ship in `srom-quant/assets/fonts`. `SROM_FONT_DIR` overrides.
Not installed anywhere: `srom-zizek`, `srom-tlumacz`, `srom-kanon` have no packages of their own beyond the above.

## 4. Connectors and services the suite talks to (not installed on the Mac)

- The site connector `mcp__Ae-…` (WordPress/JetEngine tools for studiaromologica.pl): in Claude's connector list, covered by the
  throttle hook (§ 1, row 2) with a 5 s gap.
- `github.com/blessero/srom-cloud`: the repository's master (`origin`); the Mac folder is a clone.
- Crossref, Wikidata, loc.gov etc.: only used by scripts, nothing installed.

## 5. On the Mac but not SROM (so nobody removes it by mistake)

`com.claude-backup` (launchd, 03:00 daily, `~/.claude-backup/cli.sh sync`: the `claude-backup` plugin; it backs up `~/.claude`,
which would include the hook and settings of § 1), and the other agents in `~/Library/LaunchAgents/` (Perplexity, Adobe, Google,
Dropbox, HP, Spotify, Skype, Epic, uTorrent): none belongs to SROM. No crontab entries exist.

## How to re-check this register

```sh
launchctl list | grep -i srom ; ls ~/Library/LaunchAgents | grep -i srom
grep -n srom-throttle ~/.claude/settings.json ; python3 ~/.claude/hooks/srom-throttle.py --status
ls -l ~/.claude/skills | grep -i -E "srom|wp-acf|wp-elementor"
~/.venvs/srom/bin/pip list ; pandoc --version | head -1
```
