"""tools/install_scripts.sh: links general + per-text scripts into a (fake) Scripts Panel; idempotent."""
import os, subprocess, tempfile, glob
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sh = os.path.join(repo, "tools", "install_scripts.sh")
apps = glob.glob("/Applications/Adobe InDesign */")
if not apps:
    print("INSTALL ALL PASS 0/0 (no InDesign here: SKIP)"); raise SystemExit
name = os.path.basename(apps[0].rstrip("/"))
ver = subprocess.run(["defaults", "read", f"{apps[0]}{name}.app/Contents/Info", "CFBundleShortVersionString"],
                     capture_output=True, text=True).stdout.split(".")[0].strip()
with tempfile.TemporaryDirectory() as h, tempfile.TemporaryDirectory() as b:
    os.makedirs(f"{h}/Library/Preferences/Adobe InDesign/Version {ver}.0/en_GB/Scripts")
    for k in ("postimport", "ibidem"):
        open(f"{b}/zz_pl_{k}.jsx", "w").write("//x")
    for _ in range(2):
        r = subprocess.run(["sh", sh, b], capture_output=True, text=True, env={**os.environ, "HOME": h})
        assert r.returncode == 0, r.stdout + r.stderr
    P = f"{h}/Library/Preferences/Adobe InDesign/Version {ver}.0/en_GB/Scripts/Scripts Panel"
    need = ["srom_style_setup.jsx", "srom_final_pass.jsx", "srom_zakladki.jsx", "srom_zz_pl/zz_pl_postimport.jsx", "srom_zz_pl/zz_pl_ibidem.jsx"]
    miss = [n for n in need if not os.path.exists(f"{P}/{n}")]
    assert not miss, miss
print("INSTALL ALL PASS 1/1")
