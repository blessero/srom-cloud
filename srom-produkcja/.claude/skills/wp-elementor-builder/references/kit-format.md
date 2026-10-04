# Elementor Import Kit (.zip)

The format behind **Elementor → Tools → Import / Export Kit** ("Import Website Template").

## Layout

```
manifest.json          index of everything below
site-settings.json     global colours + fonts + container width + custom CSS
custom-code.json       Pro Custom Code snippets (often just [])
content/
  page/
    1001.json          an Elementor document per page
templates/
  2001.json            Theme Builder parts (header/footer/single/archive)
wp-content/
  page/1001.json       the WordPress post row for each page
  post/
  nav_menu_item/4001.json
taxonomies/
  nav_menu.json
```

Note the split: `content/` holds the **Elementor document** (elements), `wp-content/` holds the **WordPress post row**. Both are keyed by the same id.

## manifest.json

```json
{
  "name": "my-kit",
  "title": "My Kit",
  "description": null,
  "author": "Name",
  "version": "1.0.0",
  "elementor_version": "3.25.0",
  "created": "2026-07-10 12:00:00",
  "thumbnail": false,
  "site": "https://example.com",
  "plugins": [
    {"name":"Elementor","plugin":"elementor/elementor","version":"3.25.0"},
    {"name":"Elementor Pro","plugin":"elementor-pro/elementor-pro","version":"3.25.0"}
  ],
  "site-settings": {"globalColors": true, "globalFonts": true,
                    "themeStyleSettings": true, "generalSettings": true},
  "content": {
    "page": { "1001": {"title":"Home","doc_type":"wp-page","thumbnail":"","url":"…"} }
  },
  "templates": {
    "2001": {"title":"Header","doc_type":"header","thumbnail":"",
             "conditions":[{"type":"include","name":"general","sub_name":"","sub_id":0}]}
  },
  "wp-content": {"page": {}, "post": {}, "nav_menu_item": {}},
  "taxonomies": {}
}
```

Every id in the manifest must have a matching file, and every file must be valid JSON — the importer iterates the manifest and chokes on a missing or malformed target.

## site-settings.json

```json
{ "settings": {
    "system_colors": [...], "custom_colors": [...],
    "system_typography": [...], "custom_typography": [...],
    "container_width": {"unit":"px","size":1200,"sizes":[]},
    "body_background_background": "classic",
    "body_background_color": "#F4F1EA",
    "custom_css": "…",
    "default_generic_fonts": "sans-serif",
    "viewport_md": 768, "viewport_lg": 1025
} }
```

This is the reliable part of a kit. Even when the rest of an import misbehaves, Site Settings lands — which is why globals should carry your design system rather than a stylesheet.

## Reliability, honestly

| Piece | Imports reliably? |
|---|---|
| `site-settings.json` | Yes |
| `templates/` (header, footer, archive) | Yes |
| `content/` pages | Yes |
| `wp-content/nav_menu_item/` + `taxonomies/nav_menu` | **Flaky** — undocumented, version-specific |
| Homepage assignment | **No** — always manual |

So: build the menu best-effort, and document the fallback (Appearance → Menus, 60 seconds). Homepage is Settings → Reading, always. Say this up front rather than letting the user discover it.

## The per-item fallback

Every file under `content/` and `templates/` is *already* a valid standalone template JSON (`version` / `title` / `type` / `content`). If a whole-kit import complains about one item, the user can import the rest individually via **Templates → Saved Templates → Import**. Mention this — it turns a failed import from a dead end into a detour.

## Theme Builder conditions

Conditions live in the manifest, not in the document:

```json
"conditions": [{"type":"include","name":"general","sub_name":"","sub_id":0}]
```

`general` = entire site. Re-confirm them after import; a blank condition means the header simply doesn't show, which reads as "the kit didn't work."

## Building the zip

Zip the *contents*, not the parent folder — `manifest.json` must sit at the archive root.

```python
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(kit_dir):
        for fn in files:
            fp = os.path.join(root, fn)
            z.write(fp, os.path.relpath(fp, kit_dir))
```
