---
name: wp-elementor-builder
description: Build WordPress / Elementor Pro / ACF-native output — importable Elementor JSON templates, Import Kits (.zip), Theme Builder headers/footers/singles/archives, Loop Grids + Loop Items, dynamic tags, and Global Fonts/Colors — especially when converting an existing HTML/CSS/JS design or design system into Elementor. Use this skill whenever the user mentions Elementor, an Elementor kit or template, ACF fields, WordPress Theme Builder, Loop Grid, dynamic tags, or asks to "rebuild this page in WordPress", "convert this design to Elementor", "make a WP post template", or hands over a custom.css / index.html to be recreated in a page builder — even if they don't say the word "Elementor". Also use it when debugging an Elementor template that imports badly or throws "There has been a critical error on this website."
---

# WordPress / Elementor / ACF builder

Generating Elementor JSON offline is hostile terrain: the schema is undocumented, version-specific, and **most mistakes fail as a WordPress fatal, not a validation error**. This skill encodes what actually works.

## The one rule that matters

**Never invent a control name, a doc type, or an encoding.** Elementor silently accepts unknown *setting keys* (harmless), but a malformed *dynamic tag*, a *dangling template reference*, or a bogus *document type* takes the whole site down with "There has been a critical error on this website."

Before emitting any mechanism you haven't personally verified, do one of:
1. Read the Elementor source (`elementor/core/...`, `elementor-pro/modules/...`) — via GitHub raw URLs, which are fetchable.
2. Export a real example from a live Elementor install and read its JSON.
3. Don't use the mechanism. Ship a static equivalent and document the one-click manual step.

Option 3 is not a cop-out. A template that imports and needs three clicks beats one that fatals. **Prefer mechanisms that degrade to ugly over mechanisms that degrade to fatal.**

## Workflow

1. **Read the source design fully** — HTML, CSS, JS. Extract the design tokens (`:root` custom properties) and the component inventory before writing anything.
2. **Map tokens → Elementor Globals.** The type scale becomes Global Fonts; the palette becomes Global Colors. This is step one, not an afterthought — every widget will reference these.
3. **Map sections → Containers.** Flexbox containers only. No Inner Sections (deprecated), no Atomic elements unless confirmed enabled.
4. **Map components → native widgets.** See `references/widget-mapping.md` for the substitution table (hero carousel → Slides, archive slider → Loop Grid, etc.) and what genuinely has no native equivalent.
5. **Generate with a script, not by hand.** Thousands of lines of JSON authored by hand drift. A Python generator with helpers stays consistent and is re-runnable. Start from `scripts/elementor_lib.py`.
6. **Validate before delivering.** Run `scripts/validate_elementor.py`. It catches every failure class in `references/pitfalls.md`.
7. **Write the handoff doc.** List what's auto vs. what needs a manual step, and say plainly what you could not verify.

## Styling: think like Elementor, not like a CSS author

The instinct when converting CSS is to slap classes on widgets and ship a stylesheet. That produces something that *looks* right and is *unmaintainable in the editor* — the client opens Site Settings, changes the heading font, and nothing moves.

Instead:

- Every text style resolves to a **Global Font / Global Color** via the native `__globals__` key. Never hard-code `typography_font_family` or a hex in a widget.
- Body-sized body-coloured text should emit **nothing at all** — it inherits the `text` global, exactly as a hand-built page would.
- Borders, backgrounds, padding, sticky, aspect: **native controls**, with colours referenced as globals.
- CSS is the last resort, reserved for what Elementor has no control for: hover sweeps/transitions, `@keyframes`, pseudo-elements, `backdrop-filter`, `aspect-ratio`, inline pill `<span>`s, `:hover` on a descendant.

If a class exists only to mark a widget for later, delete it. Dead marker classes are noise; identify widgets by label and position in the handoff doc.

## Structure: flatten, but know what's load-bearing

Strip wrappers that do nothing:
- A **root container** wrapping the whole document — Elementor accepts multiple top-level containers.
- A **column container holding exactly one row** — make the container the row.
- A **sizing wrapper** around something that's already a container — give the inner one the width.

Keep the one that looks redundant but isn't: **a full-bleed outer + boxed inner pair**. A boxed container's background and border stop at the boxed width, so the outer container is the only way to run an edge-to-edge rule or band while keeping content at the site width.

## Dynamic content (Elementor Pro + ACF)

Read `references/dynamic-and-acf.md` before writing a single tag. The headline facts:

- Tag settings are `urlencode(json_encode($settings, JSON_FORCE_OBJECT))`. **Empty settings is `%7B%7D`**, never `e30%3D` (base64). Base64 decodes to `null` → method call on non-object → fatal.
- Prefer Pro's **`post-custom-field`** tag (`{"key": "meta_key"}`) over `acf-text`/`acf-url`. The ACF tags need a site-generated key like `field_63a1f…:name` that cannot be known when generating offline. ACF stores text/number/url/textarea under a meta key equal to the field name, so `post-custom-field` reads them directly — and the field map becomes "name your ACF fields exactly these keys."
- A dynamic tag **replaces the control's value wholesale**. Binding a Text Editor destroys any HTML inside it — styled `<span>` pills, `<a href>` links. Decide before binding, and tell the user what the binding cost them.

## Loop Grids

`template_id` pointing at a post that doesn't exist in the target DB is a fatal. You cannot know that ID offline — it's assigned on import.

So: ship the Loop Item as its own document (`"type": "loop-item"` is genuine), ship the Loop Grid with **`template_id: ""`**, and have the user pick it once. Blank renders a harmless "select a template" notice.

A Loop Grid also has no idea what it's scoped to. Without a query filter it lists every post of that type. Ship a `elementor/query/{query_id}` PHP filter alongside, and make it fail closed (`post__in => [0]`) when context is missing — showing nothing beats dumping the whole archive at a reader.

Three traps that make a *correct* filter look broken:
- **Query ID key.** Elementor Pro ≥4.2 stores the grid's Query ID under **`post_query_query_id`**; older exports carry only `query_query_id`/`query_id`. A grid with just the legacy key is silently ignored and the filter never fires. Set it through the current UI, or write all three keys.
- **Never self-query inside the filter.** Elementor fires `elementor/query/{id}` from within `pre_get_posts`; calling `get_posts()`/`new WP_Query` there re-enters `pre_get_posts` → the same filter → unbounded recursion → a **non-catchable** "Maximum call stack size reached" fatal (try/catch can't see it). Shape the passed `$query` in place. Guard with a re-entrancy flag if a query is truly unavoidable.
- **`is_singular()` is false inside a loop item / editor preview / ajax render.** The global query isn't the main query there, so a shortcode or filter gated on `is_singular()` silently renders nothing. Latch the queried object at `wp` and fall back to the set-up post instead.

## Diagnosing a broken import

The signature is: **some content renders, then "There has been a critical error"**. The rendered prefix tells you how far Elementor got — the widget *after* the last visible text is the culprit.

Method that works: list the failing documents, then find the mechanism **common to all of them**. When the simplest file (no tabs, no loops) also crashes, the cause is something in every file — not the exotic widget you suspect. Strip every unverified mechanism at once, confirm green, then reintroduce one at a time.

And always ask for the actual `wp-content/debug.log` line. Enabling `WP_DEBUG_LOG` costs the user 30 seconds and names the failing function. Guessing from symptoms costs a round trip. Ask early. Two caveats learned the hard way: the host's "error log" is often the **ModSecurity/access log** with *no* PHP errors in it — make sure you're reading `debug.log`. And `WP_DEBUG_LOG` / try-catch never catch a **stack overflow or memory exhaustion** (they're `E_ERROR`, not exceptions) — a `register_shutdown_function` + `error_get_last()` logger does.

**The export is not the running site.** When a template fatals only on the live install, the cause may be code the JSON can't show — a `wp-content/mu-plugins/*.php` (auto-loaded, un-deactivatable), an Elementor **Custom Code** snippet, or the theme's `functions.php` — especially a second thing hooking the same `elementor/query/{id}`. Enumerate those before blaming the template. (Real case: a legacy `srom-loops.php` mu-plugin recursing on a shared query ID, diagnosed only after setting the grid's Query ID to an unhooked name isolated the fault away from the template.)

## Reference files

Read these as needed — don't load them all up front.

| File | When |
|---|---|
| `references/pitfalls.md` | **Read first when anything fatals.** Catalogue of every known crash cause + fix. |
| `references/elementor-json.md` | Document & element schema, doc types, container controls, globals. |
| `references/dynamic-and-acf.md` | Dynamic tags, encoding, ACF field mapping, Loop Grids, query filters. |
| `references/kit-format.md` | Import Kit `.zip` layout, manifest.json, site-settings.json, menus. |
| `references/widget-mapping.md` | HTML/JS component → native Elementor widget substitution table. |

## Scripts

| Script | Use |
|---|---|
| `scripts/elementor_lib.py` | Import as the base for a generator: ids, primitives, containers, globals-aware widgets, verified dynamic tags. |
| `scripts/validate_elementor.py` | Run on every generated file before delivering. Catches bad tag encoding, unresolved globals, dangling `template_id`, hard-coded typography/colour, excess nesting. |

```bash
python3 scripts/validate_elementor.py out/*.json --site-settings kit/site-settings.json
```

These require a filesystem + Python, so they're for coding sessions. In a chat-only context the references still carry everything; you just do the checks by reading.

## Honesty about verification

You will generate files you cannot test, because you have no WordPress instance. Say so, explicitly, in the handoff. Name the specific settings you matched to convention but could not exercise, and state how each one fails (soft or hard). A user who knows "if the rows look loose, it's `paragraph_spacing`" can fix it in ten seconds. A user told "it's all verified" loses an afternoon.
