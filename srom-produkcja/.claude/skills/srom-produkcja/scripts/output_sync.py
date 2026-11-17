#!/usr/bin/env python3
"""MB's `2. Output/` folder (MB, 17.11.2026): one place for the files he works with, rebuilt from the record.

    python3 output_sync.py              # rebuild the aliases (Mac job pl.srom.output-sync, every 5 minutes)
    python3 output_sync.py --dry-run    # print the plan, write nothing
    python3 output_sync.py --root DIR   # another Redakcja tree (tests)

Layout (Finder aliases, so Word always opens and saves the real file in `workspace/`; nothing is moved):
  Word/            one file per live text: the one MB opens next. `<id>_robocza.docx` (the master), or
                   `<id>_robocza_v2.docx` while a v2 (tracked corrections for MB) is newer than the master.
  Word/_src/       `<id>_src_robocza.docx` of the live texts (the frozen source, for reading).
  Word/_old/       everything else of the `_robocza` family, named `<id> · <date time> · <what>.docx`:
                   `_archive/` copies, `_oldN`/`_tracked` variants, `pl/` sealed deliveries, dropped texts.
  Social/          `workspace/social/<yyyy-mm>.md` from this month on; earlier months in `Social/_old/`.
  Letters/         drafts of letters to authors (`*listy*do*autor*`, `*letter*`, a review with a „Do autora” part);
                   `_archive/` ones in `Letters/_old/`.
  PDF online (ready, with cover)   one alias to `3. PDF online/ready/`.
  Kontaktowki/     real copies, written by srom-ikonograf's `pobierz.py` (not by this script).
Live or dropped comes from `workspace/STATUS.md` (a text section with a `**Dropped dd.mm.yyyy` line), as desk_sync.py.
This script writes and removes only the aliases it made (listed in `2. Output/.output_sync.json`); it never touches
a file in `workspace/` and never overwrites a file it did not make. Prints one line: `OUTPUT SYNC OK …`.
"""
import json, os, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_NAME = "2. Output"
MANIFEST = ".output_sync.json"
JXA = r"""ObjC.import('Foundation');
function run(argv){ var bad=[];
 for (var i=0;i<argv.length;i+=2){ var err=Ref();
  var d=$.NSURL.fileURLWithPath(argv[i]).bookmarkDataWithOptionsIncludingResourceValuesForKeysRelativeToURLError(1024,$(),$(),err);
  if(!d || d.isNil()){bad.push(argv[i]);continue;}
  if(!$.NSURL.writeBookmarkDataToURLOptionsError(d,$.NSURL.fileURLWithPath(argv[i+1]),0,err)) bad.push(argv[i+1]); }
 return bad.length ? "FAIL "+bad.join(" | ") : "OK"; }"""


def stamp(p):
    return time.strftime("%Y-%m-%d %H.%M", time.localtime(p.stat().st_mtime))


def dropped_ids(status):
    """Text keys (`[Tittel PTA]` -> `tittelpta`) of STATUS.md sections that carry a **Dropped line."""
    out = set()
    if not status.exists():
        return out
    for sec in re.split(r"^(?=### )", status.read_text(encoding="utf-8"), flags=re.M)[1:]:
        sec = sec.split("\n## ")[0]
        m = re.match(r"### .*?\[([^\]]+)\]", sec)
        if m and re.search(r"\*\*Dropped \d\d\.\d\d\.\d{4}", sec):
            out.add(re.sub(r"\W", "", m.group(1).lower()))
    return out


def plan_word(W, dropped):
    """{alias path relative to 2. Output: target} for the `_robocza` family."""
    plan, live = {}, {}

    def old(tid, p, what):
        key, n = f"Word/_old/{tid} · {stamp(p)} · {what}.docx", 2
        while key in plan:                                      # never two files under one name
            key, n = f"Word/_old/{tid} · {stamp(p)} · {what} ({n}).docx", n + 1
        plan[key] = p
    for mod in ("srom-tlumacz", "srom-produkcja"):           # tlumacz first: its master wins over a produkcja one
        base = W / mod / "work"
        if not base.is_dir():
            continue
        for d in sorted(x for x in base.iterdir() if x.is_dir()):
            tid = d.name
            gone = tid in dropped
            for p in sorted(d.glob("*_robocza*.docx")) + sorted(d.glob("pl/*_robocza*.docx")):
                if p.name.startswith("~$"):
                    continue                                    # Word's lock file
                stem = p.stem[len(tid) + 1:] if p.stem.startswith(tid + "_") else p.stem
                if p.parent.name == "pl":
                    old(tid, p, "pl delivery (sealed)")
                elif stem == "src_robocza":
                    if gone:
                        old(tid, p, "src_robocza (text dropped)")
                    else:
                        plan[f"Word/_src/{p.name}"] = p
                elif gone:
                    old(tid, p, f"{stem} (text dropped)")
                elif stem in ("robocza", "robocza_v2") and tid not in live.get(stem, {}):
                    live.setdefault(stem, {})[tid] = p
                else:
                    old(tid, p, stem if stem != "robocza" else f"robocza ({mod}, not the master)")
    masters, v2s = live.get("robocza", {}), live.get("robocza_v2", {})
    for tid in sorted(set(masters) | set(v2s)):
        m, v = masters.get(tid), v2s.get(tid)
        if v and (not m or v.stat().st_mtime > m.stat().st_mtime):
            plan[f"Word/{v.name}"] = v                         # the corrections MB opens next
            if m:
                old(tid, m, "robocza (master; open the v2 in Word first)")
        else:
            plan[f"Word/{m.name}"] = m
            if v:
                old(tid, v, "robocza_v2 (older than the master)")
    arch = W / "_archive"
    if arch.is_dir():
        for p in sorted(arch.rglob("*_robocza*.docx")):
            if p.name.startswith("~$"):
                continue
            tid = re.split(r"_(?:src_)?robocza", p.name)[0]
            where = p.relative_to(arch).parts
            what = where[1] if len(where) > 2 else where[0]  # `20261117/ndiaye_polonizacja_before/…` -> the folder
            old(tid, p, f"archive {what} · {p.stem[len(tid) + 1:]}")  # … · robocza / robocza_v2 / src_robocza
    return plan


def plan_rest(R, W, today):
    plan = {}
    soc = W / "social"
    if soc.is_dir():
        for p in sorted(soc.glob("*.md")):
            if re.fullmatch(r"\d{4}-\d{2}", p.stem):
                plan[("Social/" if p.stem >= today[:7] else "Social/_old/") + p.name] = p
    pat = re.compile(r"(listy?[-_ ]?do[-_ ]?autor|letter)", re.I)
    for p in sorted(W.rglob("*")):
        rel = p.relative_to(W).parts
        if not p.is_file() or rel[0] in ("desk", "social") or p.suffix not in (".md", ".docx"):
            continue
        is_review = len(rel) > 2 and rel[-2] == "reviews" and p.suffix == ".md" and "Do autora" in p.read_text(
            encoding="utf-8", errors="ignore")
        if not (pat.search(p.name) or is_review):
            continue
        sub = "Letters/_old/" if rel[0] == "_archive" else "Letters/"
        tag = "review + letter" if is_review else p.parent.name if p.parent.name != "ikonografia" else p.parents[1].name
        plan[f"{sub}{tag} · {p.name}"] = p
    ready = R / "3. PDF online" / "ready"
    if ready.is_dir():
        plan["PDF online (ready, with cover)"] = ready
    return plan


def plan_all(R, today=None):
    W = R / "workspace"
    plan = plan_word(W, dropped_ids(W / "STATUS.md"))
    plan.update(plan_rest(R, W, today or time.strftime("%Y-%m-%d")))
    return plan


def sync(R, dry=False):
    out = R / OUT_NAME
    plan = plan_all(R)
    man_path = out / MANIFEST
    try:
        man = json.loads(man_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        man = {}
    sig = lambda p: [str(p), p.stat().st_ino, int(p.stat().st_mtime)]
    removed, make, skipped = [], [], []
    for rel in sorted(set(man) - set(plan)):
        q = out / rel
        if q.is_file() and not q.is_symlink() and q.stat().st_size < 65536:
            removed.append(rel)
            if not dry:
                q.unlink()
    for rel, tgt in sorted(plan.items()):
        q = out / rel
        if rel in man and man[rel] == sig(tgt) and q.exists():
            continue
        if q.exists() and rel not in man:
            skipped.append(rel)                                 # a file MB or someone else put there: never overwritten
            continue
        make.append((rel, tgt))
    counts = {k: sum(1 for r in plan if r.startswith(k)) for k in ("Word/_src/", "Word/_old/", "Social/", "Letters/")}
    counts["Word/"] = sum(1 for r in plan if r.startswith("Word/") and r.count("/") == 1)
    if dry:
        for rel, tgt in sorted(plan.items()):
            print(f"{'MAKE' if (rel, tgt) in make else 'keep'}  {rel}  ->  {tgt}")
        for rel in removed:
            print(f"DROP  {rel}")
    elif make:
        if sys.platform != "darwin":
            print("OUTPUT SYNC SKIP (Finder aliases need the Mac)")
            return 0
        argv = []
        for rel, tgt in make:
            q = out / rel
            q.parent.mkdir(parents=True, exist_ok=True)
            if q.exists():
                q.unlink()                                      # our own alias, its target changed
            argv += [str(tgt), str(q)]
        r = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA, *argv], capture_output=True, text=True)
        if not r.stdout.startswith("OK"):
            print(f"OUTPUT SYNC FAIL {r.stdout.strip()} {r.stderr.strip()}")
            return 1
    if not dry:
        out.mkdir(exist_ok=True)
        man_path.write_text(json.dumps({rel: sig(t) for rel, t in plan.items() if rel not in skipped},
                                       ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    print(f"OUTPUT SYNC OK word={counts['Word/']} src={counts['Word/_src/']} old={counts['Word/_old/']} "
          f"social={counts['Social/']} letters={counts['Letters/']} made={len(make)} removed={len(removed)}"
          + (f" not-ours={len(skipped)}: " + "; ".join(skipped) if skipped else "") + (" (dry run)" if dry else ""))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    root = Path(a[a.index("--root") + 1]) if "--root" in a else HERE.parents[5]
    sys.exit(sync(root, dry="--dry-run" in a))
