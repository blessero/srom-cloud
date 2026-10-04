# ACF-native content model: registering CPTs, taxonomies, field groups as editable DB records

Verified against **ACF 6.8 (free)** by reading the plugin source. If the installed ACF differs materially, re-read `wp-content/plugins/advanced-custom-fields/includes/post-types/class-acf-post-type.php` (and `-taxonomy.php`) rather than trusting this file.

## How ACF stores a content model

ACF keeps post types / taxonomies / field groups as **ordinary WordPress posts** of post_type `acf-post-type`, `acf-taxonomy`, `acf-field-group`:
- `post_name` = your key (e.g. `post_type_srom_article`)
- `post_content` = serialized settings array

On `acf/init`, ACF reads all of these (DB + local) and calls the real `register_post_type()` / `register_taxonomy()`. So your plugin never calls those itself — it hands ACF definitions and lets ACF own registration.

## The API

```php
acf_import_post_type( array $settings );    // returns the saved record array (has ['ID'])
acf_import_taxonomy( array $settings );
acf_import_field_group( array $settings );

acf_get_acf_post_types();                   // all post-type records
acf_get_acf_taxonomies();
acf_get_field_group( $key );                // single field group by key

acf_delete_post_type( $key );               // also _taxonomy / _field_group
```

Availability check before use (ACF may be inactive):
```php
function_exists('acf_import_post_type') && function_exists('acf_get_acf_post_types') // etc.
```

**Distinguishing a DB record from a local one:** a record array has a `local` key (`'php'` or `'json'`) when it comes from local registration. A real, editable DB record has **empty `local`** and a non-zero `ID`. That test is how you know your import actually landed as editable.

## THE trap: `acf_import_*` does not dedupe by key

It **INSERTs a new record whenever the incoming array has `ID = 0`**. It does not look up your key. Call it twice → two records → two registrations of the same post type. On every page load if you wire it naively.

You must guard by key yourself:

```php
$existing = find_existing( $type, $key );   // scan acf_get_acf_post_types() etc. for ['key'] === $key
if ( $existing && empty( $existing['local'] ) && $existing['ID'] ) {
    if ( ! $overwrite ) { return 'kept'; }  // never clobber the user's UI edits
    $def['ID'] = (int) $existing['ID'];     // pass the ID → ACF updates in place
}
acf_import_post_type( $def );
```

Default to **create-missing-only**. Overwriting is a separate, explicit, confirmed user action ("Reset to plugin defaults").

## Registration modes compared (why DB import)

| Mode | In ACF UI | Editable | Notes |
|---|---|---|---|
| `register_post_type()` | **invisible to ACF** | – | ACF has no record of it. Clients find this baffling. |
| `acf_add_local_internal_post_type()` | visible | **no** | Read-only in the UI. |
| local JSON (`acf-json/`) | visible as "Sync available" | after sync | Requires a manual sync click before it's a DB record. |
| `acf_import_*` | visible | **yes, immediately** | What you want when the client manages the model themselves. |

## Required array shapes

### Post type
```php
array(
  'key'          => 'post_type_srom_article',   // fixed, deterministic → makes re-install detectable
  'title'        => 'Artykuł',
  'active'       => true,
  'post_type'    => 'srom_article',             // the actual registered slug
  'labels'       => array( 'name' => 'Artykuły', 'singular_name' => 'Artykuł', /* … */ ),
  'public'       => true,
  'show_in_rest' => true,                       // Gutenberg + REST + many Elementor dynamic features
  'supports'     => array( 'title','editor','thumbnail','custom-fields','revisions','excerpt' ),
  'taxonomies'   => array( 'dzial', 'slowa_kluczowe' ),   // ← links taxonomies to this CPT
  'menu_icon'    => 'dashicons-media-document',
  'has_archive'  => true,
  'has_archive_slug' => 'artykuly',
  'rewrite'      => array(
      'permalink_rewrite' => 'custom_permalink',  // ACF-specific selector; required for a custom slug
      'slug'              => 'artykul',
      'with_front'        => false,
  ),
)
```

### Taxonomy
```php
array(
  'key'         => 'taxonomy_srom_dzial',
  'title'       => 'Dział',
  'active'      => true,
  'taxonomy'    => 'dzial',                  // the registered key
  'object_type' => array( 'srom_article' ),  // ← the other half of the two-way link
  'labels'      => array( /* … */ ),
  'hierarchical'      => true,               // true = categories, false = flat tags
  'public'            => true,
  'show_in_rest'      => true,
  'show_admin_column' => true,
  'rewrite'     => array( 'permalink_rewrite' => 'custom_permalink', 'slug' => 'dzial', 'with_front' => false ),
)
```

The CPT's `taxonomies[]` and the taxonomy's `object_type[]` are **both** needed — set them consistently.

### Field group
```php
array(
  'key'      => 'group_srom_article',
  'title'    => 'Artykuł',
  'active'   => true,
  'location' => array( array( array(
      'param' => 'post_type', 'operator' => '==', 'value' => 'srom_article',
  ) ) ),                                     // note: array of OR-groups of AND-rules
  'fields'   => array(
      array( 'key' => 'field_x_article_id', 'name' => 'article_id', 'label' => 'article_id', 'type' => 'text' ),
      array( 'key' => 'field_x_volume', 'name' => 'volume', 'label' => 'volume',
             'type' => 'post_object', 'post_type' => array('srom_volume'),
             'return_format' => 'id', 'allow_null' => 1, 'multiple' => 0, 'ui' => 1 ),
  ),
)
```

Field `key` must be globally unique and stable — it is the join between the definition and stored meta. Field `name` is the meta key and what everyone else reads.

## Ordering

Import **taxonomies → post types → field groups**. Post types reference taxonomies; field groups reference post types via their location rules.

Afterwards call `flush_rewrite_rules( false )` **once** (not on every load — it's expensive).

## Return formats matter to consumers, not to storage

`return_format` only changes what `get_field()` returns; it does not change what's in the database. An ACF **file** field always stores the attachment ID regardless. So flipping `'return_format' => 'id'` to `'url'` is a safe, read-time-only change — useful when a template needs to bind a download button directly to a URL. Say this out loud when someone worries it will migrate data; it won't.

Common: `post_object` with `'return_format' => 'id'` returns a plain post ID (not an array/object) — the cleanest thing for other code to consume.

## ACF Free limitations that shape the model

No **repeater / flexible content / group** fields. Structured repeating data must be flattened, e.g. a textarea holding one record per line with pipe-delimited parts:

```
Given names | Surname | Affiliation | ORCID-URL
```

Document the delimiter contract, keep separators out of the data, and provide a parser (or a shortcode) so consumers don't each invent their own.

## Registration behaviours that break tests

- ACF's `register_post_types()` / `register_taxonomies()` **skip anything already registered**. Re-registering inside one request is a silent no-op — so a test that deletes and recreates a definition mid-request won't see the change reflected in the live object.
- ACF **omits `rewrite['slug']`** from the args it passes to WordPress when the slug equals the post type/taxonomy key (WP defaults to the key anyway). Asserting `rewrite['slug'] === 'autor'` therefore *fails* even though the URL is correct. Assert on `get_term_link()` / `get_permalink()` instead.
- Rewrite slugs only materialise when **pretty permalinks are on**. In a test harness, enable them *before* bootstrap.
