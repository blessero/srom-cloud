# Architecture for importers and long-running WordPress jobs

Patterns from a production CSV/XLSX→ACF importer that survives timeouts, bad data, and repeated runs. Reference implementation: `assets/srom-importer/`.

## Non-negotiable safety properties

Users import into a live site. These properties are what make that acceptable — design for them from the start, they're painful to retrofit.

| Property | Mechanism |
|---|---|
| **Nothing written by surprise** | Dry-run preview processes every row and writes nothing. The Import button stays disabled until a preview completes. |
| **Re-running is safe** | Upsert by a key field. Re-import updates, never duplicates. This doubles as the recovery path after any interruption. |
| **One bad row can't kill the run** | Row isolation: log it, skip it, continue. |
| **One bad cell can't kill a row** | Field isolation: skip that field with a note, import the rest. Fix the cell, re-import later to fill it. |
| **A timeout can't corrupt anything** | Small server-side batches; job state persisted between them; resume from the exact row. |

## Job model

State lives **server-side** in an option keyed by a random token. The browser only ever says "process the next batch". A closed tab or dropped connection loses nothing.

```php
$job = array(
  'token' => …, 'file' => …, 'post_type' => …,
  'header' => [...], 'total_rows' => N, 'mapping' => [...], 'key_target' => …,
  'options' => array( 'update_existing'=>1, 'new_status'=>'draft', 'empty_cells'=>'keep', … ),
  'state' => 'mapped|preview_running|previewed|import_running|done',
  'next_row' => 0,
  'counts' => array('created'=>0,'updated'=>0,'skipped'=>0,'errors'=>0,'warnings'=>0),
  'log' => [...],           // cap it; truncate with a flag
  'seen_keys' => [...],     // in-run duplicate detection
);
```

Guard the state machine server-side: an `import` request when `state !== 'previewed'` must be refused. Don't rely on the disabled button.

## The targets abstraction

Don't hard-code fields. Enumerate everything a column can be mapped **to**, normalized into one shape:

```php
array(
  'id'    => 'acf:field_abc123' | 'core:post_title' | 'tax:dzial',
  'kind'  => 'acf' | 'core' | 'taxonomy',
  'name'  => 'article_id',        // ACF field name / core field / taxonomy slug
  'type'  => 'text' | 'post_object' | 'taxonomy' | …,
  'label' => 'Human label',
  'field' => $acf_field_array,     // for kind=acf
)
```

Sources: ACF field groups for the post type (`acf_get_field_groups(['post_type'=>$pt])` → `acf_get_fields()`), core fields (title, slug, content, excerpt, date, menu_order), and taxonomies attached to the post type (`get_object_taxonomies()`, filtered to public/UI ones, excluding `post_format`).

This is what makes the importer generic instead of a SROM-specific script, and it's why a new field added in the ACF UI is immediately mappable with no code change.

## Auto-mapping (and the collision bug that will bite you)

Two passes:
1. **Name match** — column name == target name (with normalization and aliases).
2. **Preset** — project-specific `target => [source_column, transform, override]`.

**The bug:** a `post_object` field named `volume` and an unrelated numeric column named `volume`. Pass 1 name-matches the relationship field onto the number column. Pass 2's preset (which should point it at the signature column) can't win because `override` was false. Result: the import reported success and created zero linked posts.

**The fix — and the general rule:** name-matching a relationship field to a same-named *scalar* column is never meaningful. So a `post_object`/`relationship` target always takes its preset source:

```php
if ( in_array( $t['type'], array('post_object','relationship'), true ) ) {
    $override = true;
}
```

Generalize the lesson: **whenever two namespaces (spreadsheet columns and field names) are matched by string equality, look for collisions where the types are incompatible.** Type-awareness resolves them; string matching alone cannot.

## Value coercion

One coercion function per ACF type, returning `['status'=>'ok'|'skip', 'value'=>…, 'msgs'=>[…]]`. Never throw; a bad value skips one field.

- date → accept `Y-m-d`, `d.m.Y`, `d/m/Y`, and Excel date serials; emit the field's `return_format`
- true_false → `1/0`, `yes/no`, `tak/nie`, `true/false`
- select/radio/checkbox → match the stored value **or** the visible label
- number → tolerate `11,5` and NBSP thousands separators
- post_object/relationship → resolve by ID, exact title, slug — plus domain lookups (e.g. by a `signature` meta) with optional auto-create
- file/image → attachment ID, a filename already in the media library, or a URL (downloading must be opt-in)
- taxonomy → term names or slugs; `Parent > Child` for hierarchical; create missing terms behind a toggle

Multi-value splitting: newlines first, then `;`, then `,` only when the data can't legitimately contain commas.

## Upsert

Match by key (a text/number ACF field, or `post_name`/`post_title`), via a direct `$wpdb` meta lookup. Handle **ambiguity explicitly** — if two posts share the key, that's an error for that row, not a coin flip. Track `seen_keys` within a run so a duplicated key inside one file is reported rather than silently overwriting itself.

## Auto-creating related posts

When article rows carry their parent's data (signature/volume/year/theme), create the parent once, cache it in the job (`volume_cache`), and link every subsequent row to it. In dry-run, return a placeholder and report "will be created" — don't write.

Set the child's `post_name` explicitly from clean components (see the `sanitize_title` gotcha in `wp-gotchas.md`) rather than letting WordPress derive it from a title containing punctuation.

## Admin UI

Steps as separate screens (upload → map → preview/import), each addressable by the job token. Use `admin-post.php` handlers for form posts and `admin-ajax.php` for the batch loop. Everything under `manage_options` + nonces. Uploads go to a protected directory (`.htaccess`, `index.php`) and are garbage-collected (e.g. 48h).

Report honestly in the log: what was created, what was updated, what was skipped **and why**. "8 created, 0 errors" while silently doing nothing is the failure mode to design against — count and surface the *interesting* things (terms created, parents auto-created, fields skipped).
