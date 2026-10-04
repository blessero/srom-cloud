# HTML/CSS/JS component → native Elementor widget

The conversion table, plus the honest gaps.

## Direct substitutions

| Source | Widget | Notes |
|---|---|---|
| `<h1>`–`<h6>` | `heading` | `header_size` sets the tag; `span`/`p`/`div` also valid |
| `<p>`, rich text | `text-editor` | HTML *inside* is fine — it's not the "HTML widget" |
| `<a class="btn">` | `button` | `link`, `selected_icon`, `icon_align` |
| icon + text list | `icon-list` | repeater: `{text, selected_icon, link}` |
| icon + title + blurb card | `icon-box` | |
| `<img>` | `image` | external URLs work: `{"url": "...", "id": "", "source": "url"}` |
| social links | `social-icons` | `social_icon_list` repeater |
| `<iframe>` Google Maps | `google_maps` | `address`, `zoom`, `height` |
| `<hr>` / rules | `divider` | or a container `border_width` bottom |
| nav `<ul>` | `nav-menu` (Pro) | `menu` = the WP menu slug; gives its own mobile hamburger |
| `<form>` | `form` (Pro) | `form_fields` repeater; never reach for a form plugin |
| tabs | `nested-tabs` | children are containers → can hold any widget |
| accordion | `nested-accordion` | same |
| inline SVG brand mark | `icon` widget | Font Awesome often has a near-match (`dharmachakra` for a chakra wheel) — or upload the SVG |

## Things with no native equivalent

Be upfront about these rather than pretending.

| Source | Best native answer | What's lost |
|---|---|---|
| Bespoke JS carousel (expanding cards etc.) | `slides` (Pro) — bg image + heading + description + button per slide | The bespoke interaction. Slides has no eyebrow field; fold it into the description. |
| Horizontal scroll-snap slider of rich cards | `loop-grid` (Pro) + Loop Item, or a wrapping flex grid | The horizontal scroll, unless you add CSS `overflow-x` |
| Comma-separated string → styled pills | Text Editor with `<span>`s + CSS, **static only** | Bindable dynamically only via an ACF repeater + Loop |
| Sprite `<use href="#icon">` | Inline SVG (HTML widget) or uploaded SVG icon | Native purity — flag it as the exception |
| Scrollspy, smooth scroll | `_element_id` anchors + Elementor's built-ins | The active-link highlight |
| `@keyframes`, `:hover` on a descendant, `backdrop-filter` | Site Settings → Custom CSS | Nothing — this is CSS's proper job |

## Grid and layout

Everything is a flex Container. For a 2/3 + 1/3 split:

```
row  (flex_direction: row, flex_wrap: wrap, flex_gap 44px)
  ├ col (width 63%)
  └ col (width 33%)
```

Widths must leave room for the gap — `63 + 33 = 96` plus ~2% gap fits. Setting `50 + 50` with a gap overflows and wraps.

Sticky rail: the native **Sticky: Top** motion effect (`sticky`, `sticky_on`, `sticky_offset`), not `position: sticky` in CSS.

## Deciding when to break "native only"

Clients ask for "native widgets only" meaning *"don't hand me a page of raw HTML I can't edit."* They rarely mean "never use an HTML widget for a 40-line inline SVG brand mark."

So: keep every piece of **content and layout** native and editable. Where a decorative asset genuinely has no native home, use one HTML widget, isolate it in its own container, and name it in the handoff as the single sanctioned exception. Then it's a decision, not a leak.

## Fonts

Global Fonts referencing a Google family auto-enqueue it. A family used *only* in Custom CSS won't load — add `@import url('https://fonts.googleapis.com/css2?family=...')` at the top of the kit's `custom_css`.
