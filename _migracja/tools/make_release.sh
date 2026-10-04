# Release: workspace rebuilt from the live folders, README/MANIFEST/plugin.json from src/, srom.plugin (the plugin
# folder as one uploadable zip, .claude-plugin/ at its root), then srom-cowork-<date>.zip of the whole bundle here.
set -e
M=$(cd "$(dirname "$0")/.." && pwd); B="$M/build/srom-cowork"
sh "$M/tools/make_workspace.sh"
mkdir -p "$B/plugin/srom/.claude-plugin"
cp "$M/src/plugin.json" "$B/plugin/srom/.claude-plugin/plugin.json"
cp "$M/src/README.md" "$M/src/MANIFEST.md" "$B/"
find "$B" -name .DS_Store -delete
rm -f "$B/srom.plugin"; (cd "$B/plugin/srom" && zip -qr -X "$B/srom.plugin" . -x '*.DS_Store')
Z="$M/srom-cowork-$(date +%Y%m%d-%H%M).zip"; rm -f "$M"/srom-cowork-*.zip
(cd "$M/build" && zip -qr -X "$Z" srom-cowork -x '*.DS_Store')
echo "RELEASE $(basename "$Z") $(du -h "$Z" | cut -f1), srom.plugin $(du -h "$B/srom.plugin" | cut -f1), $(unzip -l "$Z" | tail -1 | awk '{print $2}') files"
