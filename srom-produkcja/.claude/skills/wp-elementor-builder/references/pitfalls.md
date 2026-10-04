# Pitfalls — the crash catalogue

Every entry here was learned by taking down a live site. Read this first when an import fails.

## Fatal vs. soft failure

Elementor's tolerance is asymmetric, and knowing which side you're on decides how bold you can be.

**Soft (safe to guess):** unknown *setting keys*. Elementor ignores a setting it doesn't recognise. If you're unsure whether the control is `paragraph_spacing` or `text_spacing`, guessing costs you a cosmetic miss, not a crash.

**Fatal (never guess):**
- Dynamic tag shortcodes with malformed `settings`
- `template_id` referencing a post that doesn't exist
- Document `type` values that aren't registered
- Anything where Elementor fetches an object and then calls a method on the result

The pattern: if the mechanism causes PHP to *look something up and then use it*, a bad value yields `null` and the next line is `->method()` on null. That's the fatal.

---

## 1. Dynamic tag settings encoded as base64

**Symptom:** partial page render, then "There has been a critical error on this website."

**Cause:** I emitted `settings="e30%3D"` (urlencoded base64 of `{}`). Elementor writes and reads:

```php
// elementor/core/dynamic-tags/manager.php
// write: urlencode( wp_json_encode( $settings, JSON_FORCE_OBJECT ) )
// read:  json_decode( urldecode( $settings ), true )
```

`json_decode(urldecode("e30="))` → `null` → fatal.

**Fix:** empty settings is `%7B%7D`. With settings: `urlencode('{"key":"pages"}')` → `%7B%22key%22%3A%22pages%22%7D`.

**Verify:** round-trip every tag you emit — `json.loads(unquote(encoded))` must yield a `dict`.

> There is a *second* encoding (`urlencode(base64_encode(json))`) used only in `ajax_render_tags()`. Do not let it confuse you; the shortcode path is plain urlencoded JSON.

## 2. Loop Grid with a hard-coded `template_id`

**Symptom:** fatal on any page containing the grid.

**Cause:** the Loop Item's post ID is assigned by the *target* database on import. Any ID you write offline is a guess. The widget fetches it, gets `null`, uses it.

**Fix:** ship `template_id: ""`. Blank renders a "select a template" notice. The user picks it once. Document the step.

## 3. Invented document `type`

`"type"` must be a registered Elementor document type. Verified-real values:

| type | What |
|---|---|
| `page` | generic saved template / page. **Use this when unsure.** |
| `header`, `footer` | Theme Builder parts |
| `single-post`, `single-page` | Theme Builder singles |
| `archive` | Theme Builder archive |
| `loop-item` | Loop Grid item (Pro) |
| `popup`, `section`, `container` | as named |

`page` is the safest fallback: it imports everywhere, and the user can copy/paste its content into a Theme Builder document via the editor's ⋮ menu, which sidesteps doc-type mismatch entirely.

## 4. Per-element Custom CSS

The `custom_css` setting on an element is a Pro control whose `selector` placeholder only resolves inside that control. Two hazards:

- Putting site-wide CSS there means it only loads on pages containing that element.
- Writing `selector .foo{}` anywhere else (e.g. a stylesheet) ships a literal `selector` token that matches nothing.

Prefer Site Settings → Custom CSS (kit-level `custom_css`). Use per-element CSS only for genuinely element-scoped tweaks, and only once you've confirmed it doesn't destabilise import.

## 5. Font Awesome 5 vs 6 names

Elementor bundles **Font Awesome 5**. FA6 names render as blank squares — soft failure, but embarrassing.

| Don't (FA6) | Do (FA5) |
|---|---|
| `scale-balanced` | `balance-scale` |
| `shield-halved` | `shield-alt` |
| `location-dot` | `map-marker-alt` |
| `file-lines` | `file-alt` |
| `x-twitter` (brand) | `twitter` |

`dharmachakra`, `lock-open`, `cubes`, `file-pdf`, `book`, `globe`, `pen`, `clock`, `envelope`, `search`, `link`, `arrow-right`, `facebook-f`, `linkedin-in` exist in FA5.

## 6. Binding a Text Editor destroys its HTML

A dynamic tag replaces the control's whole value. Any markup you authored inside the editor dies:
- styled `<span>` pills → become a comma string
- `<a href>` inside a meta value → becomes plain text

This is not a bug to route around; it's a design fork. Either keep the widget static, or restructure (Button widget with a bound URL; ACF repeater + Loop for pills). **Tell the user what the binding cost.**

## 7. Boxed containers don't span full width

A container with `content_width: boxed` has its background and border constrained to the boxed width. To get an edge-to-edge band or hairline rule with centred content, you need:

```
container(content_width: full)   ← background, border-bottom
  └ container(content_width: boxed)  ← the content
```

This pair looks redundant in the Structure panel. It is load-bearing. Every *other* single-child wrapper is fair game to flatten.

## 8. ACF-specific dynamic tags need an unknowable key

`acf-text`, `acf-url`, `acf-image` take `{"key": "field_63a1f8c2b91:my_field"}` — an ACF-generated key. You cannot know it offline.

Use Pro's `post-custom-field` with `{"key": "my_field"}` instead. ACF stores text/number/url/textarea values under a meta key equal to the field name, so this reads them fine. The tradeoff: the user must name ACF fields to match the meta keys, which you list in the handoff. That's a much better bargain than a broken tag.

Exception: ACF `image`/`file`/`gallery` fields with "Return: Array" store an ID, not a URL. Either set Return Format to URL, or bind the image to `post-featured-image` instead.

## 9. Loop Grid with no query filter lists everything

A Loop Grid does not know what page it's on. Give it a Query ID and hook it:

```php
add_action( 'elementor/query/my_query_id', function ( $query ) {
    $parent = (int) get_post_meta( get_the_ID(), 'parent_field', true );
    if ( ! $parent ) {           // fail CLOSED
        $query->set( 'post__in', array( 0 ) );
        return;
    }
    $query->set( 'meta_query', array( array( 'key' => 'parent_field', 'value' => $parent ) ) );
} );
```

Fail closed. Showing nothing is a visible bug the user reports; silently dumping an entire archive into a sidebar is a bug they ship.

## 10. Kit `wp-content` / menu plumbing is the flakiest part

The Elementor Import Kit's `manifest.json` + `wp-content/nav_menu_item/` structure is undocumented and version-specific. `site-settings.json`, `content/`, and `templates/` import reliably; menus and page assignment do not.

Ship the menu best-effort, and document the 60-second manual fallback (Appearance → Menus). Homepage assignment (Settings → Reading) is always manual — no kit carries it dependably.

---

## Debugging method

1. **Read the rendered prefix.** "Część I – Romski Atlantyk" then a fatal means Elementor rendered the eyebrow and died on the next widget.
2. **Intersect the failing files.** If the simplest document (no tabs, no loops) also crashes, the cause is in *every* file — so it's not the exotic widget. It's the thing you added everywhere.
3. **Strip all unverified mechanisms at once.** Confirm green. Then reintroduce one per test.
4. **Ask for `wp-content/debug.log`.** `define('WP_DEBUG', true); define('WP_DEBUG_LOG', true);` names the failing function and file. Ask for this on the *first* failure, not the third.
