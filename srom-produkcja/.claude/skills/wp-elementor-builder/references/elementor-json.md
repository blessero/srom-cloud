# Elementor JSON schema

Verified against Elementor's developer docs (`developers.elementor.com/docs/data-structure/`) and real exports.

## Document (a template / page file)

```json
{
  "version": "0.4",
  "title": "My Template",
  "type": "page",
  "content": [ /* array of top-level elements */ ],
  "page_settings": { "template": "elementor_header_footer", "hide_title": "yes" },
  "metadata": {}
}
```

- `version` — data-structure version, `"0.4"` currently.
- `type` — see the doc-type table in `pitfalls.md` §3. `page` is the safe default.
- `content` — **can hold several top-level containers.** Don't wrap them in a root container.
- `page_settings.template` — `elementor_header_footer` (full width, Theme Builder header/footer render), `elementor_canvas` (bare), or omit for theme default.

## Element

```json
{
  "id": "a1b2c3d",
  "elType": "container",
  "isInner": false,
  "settings": {},
  "elements": []
}
```

Widgets add `"widgetType": "heading"` and `elType: "widget"`. Ids are 7-char hex; any unique string works, but keep them deterministic so re-runs diff cleanly.

## Containers (flexbox)

| Control | Values |
|---|---|
| `content_width` | `"boxed"` \| `"full"` |
| `flex_direction` | `"row"` \| `"column"` |
| `flex_justify_content` | `flex-start`, `center`, `space-between`… |
| `flex_align_items` | `flex-start`, `center`, `stretch`… |
| `flex_wrap` | `"wrap"` \| `"nowrap"` |
| `flex_gap` | `{"unit":"px","size":"20","column":"20","row":"20","isLinked":true}` |
| `width` | `{"unit":"%","size":63,"sizes":[]}` — the child's width in a flex parent |
| `padding` / `margin` | `{"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":false}` |
| `min_height` | `{"unit":"px","size":68,"sizes":[]}` |
| `background_background` | `"classic"` (required before `background_color` applies) |
| `border_border` | `"solid"` / `"dashed"` (required before `border_width`/`border_color` apply) |
| `link` | `{"url":"#","is_external":"","nofollow":""}` (Pro) |

Widgets use `_padding` / `_margin` / `_border_*` (underscore-prefixed, Advanced tab). Containers use the bare names. Mixing these up is a soft failure — the style just doesn't apply.

**Boxed does not mean full-width-with-centred-content.** See `pitfalls.md` §7.

## Advanced controls

- `_element_id` — the HTML `id`, needed for anchor navigation.
- `_css_classes` — space-separated class string — **widgets only**. Containers
  register the bare name **`css_classes`**; the underscored variant on a
  container is silently dropped on import (verified live: widget classes
  survived, container classes vanished — killing every CSS/JS hook on them).
- `custom_css` — Pro, per-element. Read `pitfalls.md` §4 before using.

## Globals — the whole point of a design system

Reference a Global Color or Global Font instead of hard-coding:

```json
"settings": {
  "title": "Heading",
  "header_size": "h1",
  "__globals__": {
    "typography_typography": "globals/typography?id=primary",
    "title_color": "globals/colors?id=srom_ink"
  }
}
```

The `__globals__` key maps **control name → global reference**. The control's normal key may be omitted entirely.

System IDs that always exist: colors `primary`, `secondary`, `text`, `accent`; typography `primary`, `secondary`, `text`, `accent`. Custom globals get whatever `_id` you define in the kit.

Which control name to target:
| Widget | Typography control | Colour control |
|---|---|---|
| heading | `typography_typography` | `title_color` |
| text-editor | `typography_typography` | `text_color` |
| button | `typography_typography` | `background_color`, `button_text_color`, `border_color` |
| icon-list | `typography_typography` | `icon_color`, `text_color` |
| icon-box | `title_typography_typography`, `description_typography_typography` | `primary_color`, `title_color`, `description_color` |
| divider | — | `color` |
| container | — | `background_color`, `border_color` |

**Emit nothing for default body text.** A body-sized, body-coloured paragraph with no `__globals__` and no typography inherits the `text` global — which is exactly what a hand-built Elementor page looks like. Adding an explicit reference to `text` is noise.

## Site Settings (kit) typography & colour entries

```json
"system_colors":  [ {"_id":"primary","title":"Primary","color":"#211E1B"} ],
"custom_colors":  [ {"_id":"brand_rose","title":"Rose","color":"#F7ECEA"} ],
"system_typography": [
  {"_id":"primary","title":"Primary — H1","typography_typography":"custom",
   "typography_font_family":"Epilogue","typography_font_weight":"700",
   "typography_font_size":{"unit":"px","size":46,"sizes":[]},
   "typography_line_height":{"unit":"em","size":1.03,"sizes":[]},
   "typography_letter_spacing":{"unit":"em","size":-0.02,"sizes":[]}}
],
"custom_typography": [ /* same shape */ ]
```

Map the source `:root` type scale one-to-one and name the globals after the tokens. `--fs-h1` → `primary`, `--fs-body` → `text`, `--fs-eyebrow` → a custom `mono` global, and so on. Then the client changes a font in Site Settings and the whole site follows — which is the entire reason to do this.

Also useful in kit settings: `container_width` (`{"unit":"px","size":1200}`), `body_background_background`/`body_background_color`, `custom_css`, `viewport_md`, `viewport_lg`, `default_generic_fonts`.

Google Fonts named in Global Fonts are auto-enqueued. A family used *only* inside Custom CSS is not — add an `@import` for those.

## Nested widgets (tabs, accordion)

`nested-tabs` and `nested-accordion` hold **containers** as children, matched to the `tabs` repeater by order:

```json
{
  "elType": "widget", "widgetType": "nested-tabs",
  "settings": { "tabs": [ {"_id":"a","tab_title":"One"}, {"_id":"b","tab_title":"Two"} ] },
  "elements": [ /* container for tab 1 */, /* container for tab 2 */ ]
}
```

Keep the settings minimal — the `tabs` repeater plus a css class. Cosmetic sub-controls (`title_typography_*`, `tabs_justify_horizontal`) are guessy; style via globals on the inner widgets and CSS on `.e-n-tab-title`. First tab is the one open on load, so order the array to match intent.
