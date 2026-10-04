#!/usr/bin/env python3
"""Validate generated Elementor JSON before you hand it over.

Catches, in order of how badly they hurt:
  FATAL  malformed dynamic-tag settings (base64 / non-object → null → WP fatal)
  FATAL  loop-grid with a non-empty template_id (ID can't exist in target DB)
  FATAL  unregistered document `type`
  WARN   globals referencing ids absent from site-settings.json
  WARN   hard-coded typography / colours (design system bypassed)
  WARN   redundant container nesting
  INFO   widget inventory, depth, tag inventory

Usage:
    python3 validate_elementor.py out/*.json
    python3 validate_elementor.py out/*.json --site-settings kit/site-settings.json
    python3 validate_elementor.py kit/ --recursive
Exit code is non-zero if any FATAL is found, so it drops into CI.
"""
from __future__ import annotations
import argparse, glob, json, os, re, sys
from urllib.parse import unquote

TAG_RE = re.compile(r'\[elementor-tag id="([^"]*)" name="([^"]*)" settings="([^"]*)"\]')
GLOBAL_RE = re.compile(r'globals/(colors|typography)\?id=([A-Za-z0-9_-]+)')

KNOWN_TYPES = {
    "page", "post", "wp-page", "wp-post", "header", "footer",
    "single", "single-post", "single-page", "archive", "loop-item",
    "popup", "section", "container", "kit",
}

# Colour controls that should be globals, not hexes.
COLOR_CONTROLS = {
    "title_color", "text_color", "primary_color", "secondary_color",
    "description_color", "icon_color", "button_text_color",
}
HEX = re.compile(r"^#[0-9a-fA-F]{3,8}$")
# Pure white/black are routinely literal (button text on a coloured fill) and
# rarely earn a design-token slot. Don't nag about them.
LITERAL_OK = {"#fff", "#ffffff", "#000", "#000000"}


class Report:
    def __init__(self):
        self.fatal: list[str] = []
        self.warn: list[str] = []
        self.info: list[str] = []

    def __bool__(self):
        return not self.fatal


def load_global_ids(path):
    if not path or not os.path.exists(path):
        return None, None
    s = json.load(open(path, encoding="utf-8")).get("settings", {})
    fonts = {e["_id"] for e in s.get("system_typography", []) + s.get("custom_typography", [])}
    colors = {e["_id"] for e in s.get("system_colors", []) + s.get("custom_colors", [])}
    return fonts, colors


def check_tag(raw, where, rep: Report):
    m = TAG_RE.fullmatch(raw.strip())
    if not m:
        rep.fatal.append(f"{where}: malformed dynamic tag → {raw[:70]!r}")
        return
    _id, name, enc = m.groups()
    if enc.lower().startswith("e30"):
        rep.fatal.append(
            f"{where}: tag '{name}' uses base64 settings ({enc!r}). "
            f"Elementor does json_decode(urldecode(...)) → null → fatal. Use %7B%7D."
        )
        return
    try:
        decoded = json.loads(unquote(enc)) if enc else None
    except Exception as e:
        rep.fatal.append(f"{where}: tag '{name}' settings don't urldecode+json_decode ({e})")
        return
    if not isinstance(decoded, dict):
        rep.fatal.append(f"{where}: tag '{name}' settings decode to {type(decoded).__name__}, not object")
        return
    rep.info.append(f"tag {name}({decoded.get('key','')})")


def walk(el, rep: Report, fonts, colors, path="content", depth=0, stats=None):
    stats["depth"] = max(stats["depth"], depth)
    et = el.get("elType")
    wt = el.get("widgetType")
    label = wt or et or "?"
    here = f"{path}/{label}"
    s = el.get("settings", {}) or {}

    if et == "container":
        stats["containers"] += 1
    if wt:
        stats["widgets"][wt] = stats["widgets"].get(wt, 0) + 1

    # --- FATAL: loop grid template_id
    if wt == "loop-grid":
        tid = s.get("template_id", "")
        if tid not in ("", None):
            rep.fatal.append(
                f"{here}: loop-grid template_id={tid!r}. That post id cannot be "
                f"guaranteed to exist in the target DB → fatal. Ship '' and let the user pick."
            )
        if not (s.get("query_id") or s.get("query_query_id")):
            rep.warn.append(f"{here}: loop-grid has no query_id — it will list every post of its type.")

    # --- FATAL: dynamic tags
    for control, raw in (s.get("__dynamic__") or {}).items():
        check_tag(raw, f"{here}[{control}]", rep)

    # --- WARN: globals resolve
    for kind, gid in GLOBAL_RE.findall(json.dumps(s, ensure_ascii=False)):
        if kind == "typography" and fonts is not None and gid not in fonts:
            rep.warn.append(f"{here}: unresolved global font '{gid}'")
        if kind == "colors" and colors is not None and gid not in colors:
            rep.warn.append(f"{here}: unresolved global colour '{gid}'")

    # --- WARN: hard-coded styling
    if s.get("typography_typography") == "custom" and "typography_typography" not in (s.get("__globals__") or {}):
        rep.warn.append(f"{here}: hard-coded typography — use a Global Font (__globals__).")
    g = s.get("__globals__") or {}
    for ctrl in COLOR_CONTROLS:
        v = s.get(ctrl)
        if (isinstance(v, str) and HEX.match(v) and ctrl not in g
                and v.lower() not in LITERAL_OK):
            rep.warn.append(f"{here}: hard-coded {ctrl}={v} — use a Global Color.")

    kids = el.get("elements", []) or []

    # --- WARN: redundant nesting
    if et == "container" and len(kids) == 1 and kids[0].get("elType") == "container":
        inner = kids[0]
        outer_bleed = s.get("content_width") == "full"
        # full-bleed outer + boxed inner is legitimate (edge-to-edge bg/rule)
        legit = outer_bleed and inner.get("settings", {}).get("content_width") == "boxed"
        if not legit:
            rep.warn.append(f"{here}: container wraps a single container — flatten it.")

    for i, c in enumerate(kids):
        walk(c, rep, fonts, colors, f"{here}[{i}]", depth + 1, stats)


def validate(path, fonts, colors) -> Report:
    rep = Report()
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        rep.fatal.append(f"invalid JSON: {e}")
        return rep

    if isinstance(doc, list):           # e.g. custom-code.json
        rep.info.append("array document (not an Elementor doc) — skipping element checks")
        return rep

    dtype = doc.get("type")
    if dtype and dtype not in KNOWN_TYPES:
        rep.fatal.append(f"unregistered document type {dtype!r}. Safe default: 'page'.")

    if "e30%3D" in json.dumps(doc):
        rep.fatal.append("legacy base64 tag settings 'e30%3D' present somewhere.")

    stats = {"depth": 0, "containers": 0, "widgets": {}}
    for i, el in enumerate(doc.get("content", []) or []):
        walk(el, rep, fonts, colors, f"content[{i}]", 0, stats)

    if stats["depth"] > 6:
        rep.warn.append(f"container depth {stats['depth']} — consider flattening (target ≤5).")
    rep.info.append(
        f"type={dtype} depth={stats['depth']} containers={stats['containers']} "
        f"widgets={sorted(stats['widgets'])}"
    )
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--site-settings", help="kit site-settings.json, to resolve global ids")
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="only show FATAL/WARN")
    args = ap.parse_args()

    fonts, colors = load_global_ids(args.site_settings)
    if fonts is None:
        print("· no --site-settings given: global ids will not be resolved\n")

    files = []
    for p in args.paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, "**", "*.json"), recursive=True)
        else:
            files += glob.glob(p)

    n_fatal = 0
    for f in sorted(files):
        rep = validate(f, fonts, colors)
        n_fatal += len(rep.fatal)
        status = "FAIL" if rep.fatal else ("warn" if rep.warn else "ok")
        print(f"[{status:4}] {f}")
        for m in rep.fatal:
            print(f"   FATAL {m}")
        for m in rep.warn:
            print(f"   warn  {m}")
        if not args.quiet:
            tags = [m for m in rep.info if m.startswith("tag ")]
            for m in rep.info:
                if not m.startswith("tag "):
                    print(f"   info  {m}")
            if tags:
                print(f"   info  {len(tags)} dynamic tags: {', '.join(sorted(set(tags))[:8])}"
                      + (" …" if len(set(tags)) > 8 else ""))
        print()

    print(f"{len(files)} file(s), {n_fatal} fatal issue(s).")
    sys.exit(1 if n_fatal else 0)


if __name__ == "__main__":
    main()
