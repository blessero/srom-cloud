# Dynamic tags, ACF, and Loop Grids

## The shortcode format (verified in source)

`elementor/core/dynamic-tags/manager.php`:

```php
// write
urlencode( wp_json_encode( $tag->get_settings(), JSON_FORCE_OBJECT ) )
// read
json_decode( urldecode( $tag_settings_match[1] ), true )
```

So:

```
[elementor-tag id="a1b2c3d" name="post-title" settings="%7B%7D"]
[elementor-tag id="e4f5a6b" name="post-custom-field" settings="%7B%22key%22%3A%22pages%22%7D"]
```

- Empty settings → `%7B%7D`. **Not** `e30%3D` — that's base64, decodes to `null`, fatals.
- `id` is any unique 7-char hex.
- Python: `quote(json.dumps(settings, separators=(",",":")), safe="")`, and `"{}"` for empty.

Always round-trip what you emit:
```python
assert isinstance(json.loads(unquote(encoded)), dict)
```

## Attaching a tag to a widget

`__dynamic__` maps **control name → tag string**. The static value stays as the editor fallback.

```json
"settings": {
  "title": "Static fallback",
  "__dynamic__": { "title": "[elementor-tag id=\"a1b2c3d\" name=\"post-title\" settings=\"%7B%7D\"]" }
}
```

Which control to bind:

| Widget | Control | Notes |
|---|---|---|
| heading | `title` | also `link` for a linked heading |
| text-editor | `editor` | **replaces all inner HTML** |
| image | `image` | needs an image-category tag |
| button | `link` | needs a URL-category tag |

## Tag names

Verified in use:
- `post-title` — no settings
- `post-featured-image` — no settings, image category
- `post-custom-field` — `{"key": "<meta_key>"}` (Pro)
- `post-excerpt`, `post-date`, `post-content`

Less certain: `post-url` (permalink). It works in practice but confirm; a wrong tag name generally yields an empty value rather than a fatal, because `create_tag()` returns null and callers check — but don't rely on that.

## ACF: use `post-custom-field`, not the `acf-*` tags

`acf-text` / `acf-url` / `acf-image` take `{"key":"field_63a1f8c2b91:my_field"}` — an ACF-generated key that only exists in the target database. Unknowable offline.

`post-custom-field` reads plain post meta, and ACF stores text / number / url / textarea / wysiwyg values under a meta key **equal to the field name**. So:

> Name the ACF fields exactly as the meta keys, and every binding resolves with zero clicks.

Publish that key list in the handoff doc. It's the contract between your JSON and their field group.

**Field types that don't map cleanly:**
- `image` / `file` / `gallery` with Return Format = Array or ID → meta holds an ID, not a URL. Set Return Format to URL, or use `post-featured-image`.
- `relationship` / `post_object` → meta holds a post ID. Fine for query filters; useless as display text.
- `repeater` → meta is a count, with sub-fields under `field_0_subfield`. Not bindable to one widget; needs a Loop.

## What a binding destroys

The tag replaces the control's **entire value**. Consequences worth deciding on *before* you bind:

- A Text Editor containing `<div class="pills"><span>a</span><span>b</span></div>` styled by `.pills span` → the spans vanish; you get the raw meta string.
- A meta value rendered as `<a href="...">DOI ↗</a>` → plain text, no link.

Fixes: keep the widget static; or restructure (Button widget with bound URL; ACF repeater + Loop Grid for pills). Either way, **say out loud what the binding cost**, because it's invisible until the client looks.

## Loop Grids

```json
{
  "elType": "widget", "widgetType": "loop-grid",
  "settings": {
    "template_id": "",
    "query_post_type": "my_cpt",
    "query_query_id": "my_query_id",
    "query_id": "my_query_id",
    "columns": "1", "columns_tablet": "2", "columns_mobile": "1"
  }
}
```

Two hard requirements:

**1. `template_id` must be empty.** The Loop Item's ID is assigned by the target DB on import. A stale ID → widget fetches null → fatal. Blank → harmless editor notice, and the user selects the template once. Ship the Loop Item as a separate document with `"type": "loop-item"`.

**2. Scope it in PHP.** A grid with no filter lists every post of its type.

```php
add_action( 'elementor/query/my_query_id', function ( $query ) {
    $parent = (int) get_post_meta( get_the_ID(), 'volume', true );
    if ( ! $parent ) {
        $query->set( 'post__in', array( 0 ) );  // fail closed
        return;
    }
    $query->set( 'post_type', 'my_cpt' );
    $query->set( 'meta_query', array( array( 'key' => 'volume', 'value' => $parent ) ) );
    $query->set( 'meta_key', 'seq' );
    $query->set( 'orderby', 'meta_value_num' );
    $query->set( 'order', 'ASC' );
    $query->set( 'post__not_in', array( get_the_ID() ) ); // exclude self on a sibling list
} );
```

Ship this as an mu-plugin (`wp-content/mu-plugins/`) so it can't be deactivated by accident, and `php -l` it before delivering.

**Fail closed.** `post__in => [0]` shows nothing when context is missing. The alternative — an unfiltered query — silently dumps an entire archive into a sidebar, which is the kind of bug that ships.

**Ordering by a numeric meta** (`meta_key` + `orderby: meta_value_num`) beats ordering by date whenever the real-world sequence (issue number, chapter order) doesn't match publication order.

## Inside a Loop Item

Every tag resolves against the post currently being looped, not the page. So `post-title` is that row's title. This is what makes one Loop Item serve a Contents list, a sidebar, and an archive grid.

## Head meta for scholarly / SEO landing pages

Elementor widgets cannot write to `<head>`. Google Scholar wants `citation_title`, `citation_author`, `citation_doi`, `citation_pdf_url`, `citation_firstpage`, `citation_lastpage`. That's a `wp_head` snippet or an SEO plugin's custom-meta feature, fed from the same ACF fields. Flag it — a "canonical DOI landing page" that omits these isn't doing its job, and no amount of Elementor gets you there.
