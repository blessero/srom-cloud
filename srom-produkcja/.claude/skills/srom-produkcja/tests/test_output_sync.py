"""output_sync.py: MB's `2. Output/` — one Word file per live text (the master, or a newer v2), sources in `_src/`,
everything else of the `_robocza` family in `_old/` under unique dated names, dropped texts (STATUS **Dropped) out of
the root, social months split by date, letter drafts; on the Mac real aliases, idempotent, stale ones removed, a file
it did not make never overwritten."""
import os, subprocess, sys, tempfile, time
from pathlib import Path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
sys.path.insert(0, S)
import output_sync as o
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

R = Path(tempfile.mkdtemp()); W = R / "workspace"
def mk(rel, age=0):
    p = W / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(rel, encoding="utf-8")
    os.utime(p, (time.time() - age, time.time() - age)); return p
(W / "STATUS.md").parent.mkdir(parents=True, exist_ok=True)
(W / "STATUS.md").write_text("## Texts\n### A [Alpha] — code ALP\n- ok\n### B [Beta Two] — code BET\n"
                             "- **Dropped 08.11.2026 04:56 (MB: out).**\n## Other\n", encoding="utf-8")
mk("srom-tlumacz/work/alpha/alpha_robocza.docx", 100)
mk("srom-tlumacz/work/alpha/alpha_robocza_v2.docx", 10)
mk("srom-tlumacz/work/alpha/alpha_robocza_old1.docx", 500)
mk("srom-tlumacz/work/alpha/~$pha_robocza.docx")
mk("srom-produkcja/work/alpha/alpha_src_robocza.docx", 900)
mk("srom-produkcja/work/alpha/pl/alpha_robocza.docx", 800)
mk("srom-tlumacz/work/betatwo/betatwo_robocza.docx", 50)
mk("srom-tlumacz/work/gamma/gamma_robocza.docx", 50)
mk("srom-tlumacz/work/gamma/gamma_robocza_v2.docx", 500)
a1 = mk("_archive/20261117/alpha_x_before/alpha_robocza.docx", 300)
a2 = mk("_archive/20261117/alpha_x_before/alpha_robocza_v2.docx", 300); os.utime(a2, (a1.stat().st_atime, a1.stat().st_mtime))
mk("social/2026-10.md"); mk("social/2026-11.md"); mk("social/bank.tsv")
mk("srom-tlumacz/tom19_listy_do_autorow.md"); mk("srom-zizek/volumes/19-2026/reviews/x.md").write_text("## Do autora\n")
mk("srom-zizek/volumes/19-2026/reviews/y.md"); mk("desk/backup/listy-do-autorow.md")
(R / "3. PDF online" / "ready").mkdir(parents=True)
plan = o.plan_all(R, today="2026-11-17")
word = sorted(k for k in plan if k.startswith("Word/") and k.count("/") == 1)
t("Word root: one file per live text — the v2 where it is newer than the master, else the master; a dropped text none",
  word == ["Word/alpha_robocza_v2.docx", "Word/gamma_robocza.docx"], word)
olds = sorted(k for k in plan if k.startswith("Word/_old/"))
t("Word/_old: master behind a v2, older v2, _oldN, pl delivery, dropped text, both archive copies under distinct names",
  len(olds) == 7 and any("master; open the v2" in k for k in olds) and any("gamma" in k and "older than the master" in k for k in olds)
  and any("robocza_old1" in k for k in olds) and any("pl delivery" in k for k in olds)
  and any(k.startswith("Word/_old/betatwo") and "text dropped" in k for k in olds)
  and sum("archive alpha_x_before" in k for k in olds) == 2, olds)
t("Word/_src: the frozen source; Word's ~$ lock file nowhere",
  [k for k in plan if k.startswith("Word/_src/")] == ["Word/_src/alpha_src_robocza.docx"]
  and not any("~$" in k for k in plan))
t("Social: this month on in the root, earlier in _old, the bank not at all",
  "Social/2026-11.md" in plan and "Social/_old/2026-10.md" in plan and not any("bank" in k for k in plan))
let = sorted(k for k in plan if k.startswith("Letters/"))
t("Letters: letter drafts and a review with a Do autora part; not desk backups, not a review without one",
  let == ["Letters/review + letter · x.md", "Letters/srom-tlumacz · tom19_listy_do_autorow.md"], let)
t("PDF online: one alias to 3. PDF online/ready", plan.get("PDF online (ready, with cover)") == R / "3. PDF online" / "ready")

if sys.platform == "darwin":
    run = lambda: subprocess.run([sys.executable, os.path.join(S, "output_sync.py"), "--root", str(R)],
                                 capture_output=True, text=True)
    out = R / "2. Output"; out.mkdir(); (out / "Word").mkdir(); (out / "Word" / "gamma_robocza.docx").write_text("MB's own")
    r1 = run()
    kind = subprocess.run(["mdls", "-raw", "-name", "kMDItemKind", str(out / "Word" / "alpha_robocza_v2.docx")],
                          capture_output=True, text=True).stdout
    t("Mac: aliases made; a file it did not make is reported, never overwritten",
      r1.stdout.startswith("OUTPUT SYNC OK") and "not-ours=1" in r1.stdout
      and (out / "Word" / "gamma_robocza.docx").read_text() == "MB's own"
      and (out / "Word" / "alpha_robocza_v2.docx").stat().st_size > 200 and kind in ("Alias", "(null)"), (r1.stdout, r1.stderr, kind))
    r2 = run()
    t("Mac: a second run makes nothing", "made=0 removed=0" in r2.stdout, r2.stdout)
    os.remove(W / "srom-tlumacz/work/alpha/alpha_robocza_v2.docx")
    r3 = run()
    t("Mac: v2 gone -> its alias removed, the master's alias back in the root",
      not (out / "Word" / "alpha_robocza_v2.docx").exists() and (out / "Word" / "alpha_robocza.docx").exists()
      and "removed=" in r3.stdout and "removed=0" not in r3.stdout, r3.stdout)
print(f"OUTPUT_SYNC ALL PASS {sum(res)}/{len(res)}" if all(res) else f"OUTPUT_SYNC FAILED {res.count(False)}/{len(res)}")
