# Portable version — for claude.ai Projects / any chat without Skills

Paste the block below into a claude.ai **Project → Custom Instructions**, or into a
`CLAUDE.md` at a repo root. It's the SKILL.md distilled to what survives without a
filesystem: the rules and the failure modes. Attach `references/*.md` to the Project
as documents if you want the deep detail available on demand.

The scripts (`elementor_lib.py`, `validate_elementor.py`) only matter where code runs.
In chat, do their checks by reading — the tag round-trip and the `template_id` check
are both eyeballable.

---

## WordPress / Elementor / ACF output

You generate Elementor JSON offline, against a schema that is undocumented, version-specific,
and where **most mistakes fail as a WordPress fatal, not a validation error**.

**Never invent a control name, a document type, or an encoding.** Elementor ignores unknown
*setting keys* (harmless), but a malformed *dynamic tag*, a *dangling template reference*, or a
bogus *document type* takes the site down with "There has been a critical error on this website."
The tell: if the mechanism makes PHP look something up and then call a method on it, a bad value
yields `null` and the next line fatals.

Before using a mechanism you haven't verified, either read the Elementor source on GitHub, or
don't use it — ship a static equivalent plus a documented one-click manual step. **Prefer
mechanisms that degrade to ugly over mechanisms that degrade to fatal.**

### Non-negotiables

- **Dynamic tag settings** are `urlencode(json_encode($settings, JSON_FORCE_OBJECT))`, read back
  with `json_decode(urldecode(...))`. Empty settings is `%7B%7D`. **Never `e30%3D`** (base64) —
  it decodes to `null` and fatals. Round-trip every tag you emit.
- **Loop Grid `template_id` must be `""`.** The Loop Item's post id is assigned by the target
  database on import; any id written offline is a guess that fatals. Blank shows a harmless
  "select a template" notice. Ship the Loop Item as `"type": "loop-item"` and let the user pick.
- **A Loop Grid with no query filter lists every post of its type.** Ship an
  `elementor/query/{query_id}` PHP filter, and make it fail closed (`post__in => [0]`) when
  context is missing. Showing nothing beats dumping an archive at a reader.
- **Document `type`**: `page`, `header`, `footer`, `single-post`, `archive`, `loop-item`, `popup`.
  When unsure use `page` — it imports everywhere.
- **Font Awesome 5**, not 6. `balance-scale` not `scale-balanced`; `map-marker-alt` not
  `location-dot`; `shield-alt`, `file-alt`, `twitter`.

### Style the way Elementor does

Converting CSS tempts you to put classes on widgets and ship a stylesheet. That looks right and is
unmaintainable: the client changes the heading font in Site Settings and nothing moves.

- Every text style resolves to a **Global Font / Global Color** via `__globals__`
  (`"typography_typography": "globals/typography?id=primary"`). Never hard-code a font family or
  a hex in a widget.
- Map the source `:root` type scale one-to-one onto Global Fonts, named after the tokens.
- **Body-sized, body-coloured text should emit nothing at all** — it inherits the `text` global,
  which is what a hand-built page looks like.
- Borders, backgrounds, padding, sticky: **native controls**, colours referenced as globals.
- CSS is the last resort — only for hover sweeps, `@keyframes`, pseudo-elements,
  `backdrop-filter`, `aspect-ratio`, inline pill `<span>`s.
- Delete marker classes that exist only to label a widget. Identify widgets in the handoff doc by
  label and position instead.

### Structure

Flatten a root wrapper (documents take several top-level containers), a column holding one row,
and a sizing wrapper around something that's already a container.

**Keep** the full-bleed outer + boxed inner pair. A boxed container's background and border stop
at the boxed width, so the outer is the only way to run an edge-to-edge rule with centred content.
It looks redundant in the Structure panel; it is load-bearing.

### ACF

Use Pro's **`post-custom-field`** tag (`{"key":"meta_key"}`), not `acf-text`/`acf-url` — those need
a site-generated `field_63a1f…:name` key you cannot know offline. ACF stores text/number/url/
textarea under a meta key equal to the field name, so `post-custom-field` reads them directly.
The contract: **the user names ACF fields exactly as the meta keys you publish in the handoff.**

Image/file fields returning an Array or ID hold an id, not a URL — set Return Format to URL, or
bind `post-featured-image`.

**A dynamic tag replaces the control's value wholesale.** Binding a Text Editor destroys any HTML
inside it — styled `<span>` pills, `<a href>` links. That's a design fork, not a bug. Decide before
binding, and say out loud what the binding cost.

### Debugging a broken import

Some content renders, then the fatal — the rendered prefix tells you how far Elementor got; the
culprit is the widget *after* the last visible text.

Then **intersect the failing files**: if the simplest document (no tabs, no loops) also crashes,
the cause is in every file, so it isn't the exotic widget you suspect. Strip every unverified
mechanism at once, confirm green, reintroduce one at a time.

Ask for the `wp-content/debug.log` line on the **first** failure, not the third. Enabling
`WP_DEBUG_LOG` costs 30 seconds and names the failing function.

### Honesty about verification

You have no WordPress instance and cannot test what you generate. Say so explicitly in the
handoff. Name the specific settings you matched to convention but could not exercise, and state
how each fails — soft or hard. A user who knows "if the rows look loose, it's `paragraph_spacing`"
fixes it in ten seconds. A user told "it's all verified" loses an afternoon.
