"""The website mu-plugin (srom-quant assets/srom-scholarly.php) under PHP: php -l, then fixtures/muplugin_harness.php
(WordPress stubbed) runs the metadata, body-class, licence, flipbook and query-filter paths (review 20.10.2026: v2.5).
Needs php on PATH (the Mac: Homebrew); without it the last line is MUPLUGIN SKIP. Last line: MUPLUGIN ALL PASS n/n."""
import os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, "..", "..", "srom-quant", "assets", "srom-scholarly.php"))
php = shutil.which("php")
if not php:
    print("MUPLUGIN SKIP (no php on PATH)")
    raise SystemExit(0)
res = []
def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))
lint = subprocess.run([php, "-l", PLUGIN], capture_output=True, text=True, stdin=subprocess.DEVNULL)
t("php -l", "No syntax errors" in lint.stdout, lint.stdout + lint.stderr)
src = open(PLUGIN, encoding="utf-8").read()
t("no fatal catcher, no ?srom_off kill switch (removed v2.5)",
  not re.search(r"register_shutdown_function|SROM_FILTERS_OFF|\$_GET\['srom_off'\]", src))
t("PHP 7.4-safe: no str_starts_with / str_contains / match()", not re.search(r"\bstr_(starts_with|contains|ends_with)\(|\bmatch\s*\(", src))
v = re.search(r"\* Version: (\S+)", src).group(1)
t("header version = [srom_diag] version", f"'mu-plugin version'      => '{v}'" in src, v)
# The Importer (review 21.10.2026): a volume's pub_date is the print date the plugin prints as citation_publication_date
IMP = os.path.normpath(os.path.join(HERE, "..", "..", "wp-acf-plugin-builder", "assets", "srom-importer"))
imp = {f: open(os.path.join(IMP, "includes", f), encoding="utf-8").read() for f in ("class-srom-imp-fields.php", "class-srom-imp-runner.php")}
t("Importer: volume pub_date from pub_date_print (preset and auto-created Tom), never pub_date_online",
  "'pub_date'       => array( 'pub_date_print'" in imp["class-srom-imp-fields.php"]
  and "'pub_date'  => array( 'pub_date_print', 'pub_date' )" in imp["class-srom-imp-runner.php"]
  and not any(re.search(r"'pub_date'\s*=>\s*array\(\s*'pub_date_online'", s) for s in imp.values()))
t("Importer: php -l", all("No syntax errors" in subprocess.run([php, "-l", os.path.join(IMP, *p)], capture_output=True, text=True,
  stdin=subprocess.DEVNULL).stdout for p in (("srom-importer.php",), ("includes", "class-srom-imp-fields.php"), ("includes", "class-srom-imp-runner.php"))))
h = subprocess.run([php, os.path.join(HERE, "fixtures", "muplugin_harness.php"), PLUGIN],
                   capture_output=True, text=True, stdin=subprocess.DEVNULL)
cases = [l for l in h.stdout.splitlines() if l.startswith(("ok ", "FAIL "))]
for l in cases:
    t("harness: " + l.split(None, 1)[1], l.startswith("ok "), l)
t("harness ran to the end", "HARNESS ALL PASS" in h.stdout and len(cases) >= 20, (h.stdout + h.stderr)[-800:])
n, ok = len(res), sum(res)
print(f"MUPLUGIN ALL PASS {n}/{n}" if ok == n else f"MUPLUGIN FAILED {n - ok}/{n}")
