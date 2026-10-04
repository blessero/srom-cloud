---
name: wp-acf-plugin-builder
description: Build and maintain WordPress plugins that own an ACF content model — registering custom post types, taxonomies and field groups as native editable ACF records, plus spreadsheet/CSV importers, admin screens, and batch jobs. Use this skill whenever the user mentions a WordPress plugin, a custom post type or CPT, ACF / Advanced Custom Fields field groups, importing a spreadsheet or CSV into WordPress, a WP admin screen or settings page, or wp-admin behaviour — and also whenever working on the SROM / Studia Romologica journal site (srom_article, srom_volume, srom-importer, srom-scholarly). Reach for it even when the request sounds small ("just add a field", "rename this post type", "why is ACF not seeing my CPT"), because the failure modes here are silent (double registration, phantom meta keys, non-editable field groups) rather than loud. For building Elementor templates/JSON from the resulting fields, use wp-elementor-builder instead.
---

# WordPress plugins that own an ACF content model

The presentation layer (Elementor JSON, templates, dynamic tags) belongs to **wp-elementor-builder**. This skill is the layer underneath: the plugin that *defines and fills* the data — post types, taxonomies, field groups, importers, admin UI.

## The two rules that actually prevent disasters

**1. Read the ACF/WP source before using an API you're not certain of.** ACF's internal registration API is thinly documented and version-specific. Guessing produces code that *looks* right, runs without error, and silently does the wrong thing (duplicate records, non-editable field groups). Find the plugin on disk (`wp-content/plugins/advanced-custom-fields/includes/post-types/class-acf-*.php`) and read it. A five-minute probe test beats an hour of plausible wrongness.

**2. "It greps clean" is not "it works."** The worst bugs in this domain are silent. In this skill's own history: renaming an ACF field to `volume` made it collide with a spreadsheet column named `volume`; auto-mapping hijacked the field, the import reported *"8 created, 0 errors"*, and produced **zero** linked volumes. Static inspection looked perfect. Only an end-to-end run on a real WordPress install caught it. Before you claim something works, run it against real data and assert on the resulting database state — not on the absence of errors.

Corollary: watch for **false-positive assertions**. A check like `article->volume_id === $volume->ID` passes when *both* sides are 0. Assert on concrete expected values, not on equality between two things that can both be empty.

## Choosing how to register the content model

This is the highest-leverage decision and it is not reversible for free. Four ways to get a CPT into WordPress:

| Method | Appears in ACF UI? | Editable there? | Use when |
|---|---|---|---|
| `register_post_type()` in your plugin | **No** | No | Nobody will ever need to edit it in ACF. Note: ACF genuinely cannot see it — this surprises clients. |
| `acf_add_local_internal_post_type()` (local PHP) | Yes | **No** (read-only) | You want visibility but hard-code ownership. |
| Local JSON (`acf-json/`) | Yes, as **"Sync available"** | Only after a sync click | Version-controlled model, dev→prod sync workflow. |
| **`acf_import_post_type()` / `_taxonomy()` / `_field_group()`** → real DB records | Yes | **Yes, immediately** | **The client must manage the model in ACF's own UI.** |

If the user says anything like *"ACF doesn't see my post types"*, *"I need it native to ACF"*, or *"I want to add fields myself"* — they need the **DB-import** route. See `references/acf-native-content-model.md` for the full API, the required array shapes, and the idempotency trap that will otherwise create duplicate records on every page load.

## Plugin lifecycle for an ACF-owned model

Activation hooks fire **before ACF is loaded**, so you cannot create ACF records there. The pattern that works:

```
register_activation_hook  → set an option: autoinstall_pending = 1
add_action('acf/init')    → if pending: install(), stamp version, clear pending, flush_rewrite_rules(false)
add_action('acf/init')    → maybe_upgrade(): if stored version != current, create newly-added definitions
```

Three invariants that keep this safe over the plugin's life:

- **Install must be create-missing-only by default.** `install($overwrite = false)` never clobbers a record the user has edited in the ACF UI. Offer a separate explicit "Reset to defaults" for overwrite.
- **Respect deliberate removal.** A `setup_done` option means "the user has made their choice." If they deleted the definitions on purpose, an upgrade must not silently resurrect them.
- **Renames need legacy cleanup.** If v2 renames `srom_issue` → `srom_volume`, an in-place upgrade creates the new record but leaves the old one — now you have *two* post types double-registering. Explicitly retire the old keys on upgrade.

**Definitions are not data.** Removing field groups/post types must never delete the user's posts or postmeta. Say so in the UI copy; users are (rightly) scared of destructive buttons.

## The cross-team contract: persisted vs derived

When other developers build templates against your model, the assumption they *will* make is **field name → meta key**. That assumption is wrong for most of your columns, and it fails silently (blank fields, not errors).

Document explicitly which inputs become which, because each has a different read path:

| Becomes | Read via | Trap |
|---|---|---|
| ACF field | `get_field('name', $id)` | the only case where field-name→meta-key holds |
| Core post field | `menu_order`, `post_name`, `post_content`… | e.g. a `seq` column → `menu_order`, **not** a `seq` meta key |
| Taxonomy term | `get_the_terms($id, 'tax')` | a `section` *select* replaced by a `section` *taxonomy* leaves no meta |
| Derived | `get_permalink()` etc. | never store a canonical URL as meta — it drifts from the real one |
| Ignored | — | extra spreadsheet columns |

Ship this as a table in a `HANDOVER.md` alongside the plugin. It is the single artifact that stops other devs building against phantom keys.

Also remember: **WordPress' native search indexes `post_title`/`post_content`/`post_excerpt` and never ACF meta.** If a field must be findable by site search (an abstract, a description), mirror it into `post_content`/`post_excerpt` on import, regenerated from the same source each run so the copies cannot drift.

## Building importers and other long-running jobs

If you're writing a CSV/XLSX importer or any batch operation, the architecture in `references/plugin-architecture.md` is battle-tested and worth copying wholesale: server-side job state, dry-run preview before any write, upsert-by-key (so re-running is both idempotent *and* the recovery path), row- and field-level isolation so one bad cell never kills a run, and batched AJAX so a timeout cannot corrupt anything.

The working reference implementation is bundled: `assets/srom-importer/` — a complete, tested ACF-native importer plugin. Read its `includes/class-srom-imp-setup.php` for the registration lifecycle and `class-srom-imp-runner.php` for the batch/upsert/coercion engine.

## Test on a real WordPress install. Always.

There is no meaningful substitute, and it is cheaper than you think: WordPress + SQLite + ACF-free, no MySQL, bootstrapped in about a minute.

```bash
bash scripts/setup-wp-test-site.sh /path/to/scratch/wp-test /path/to/your-plugin
```

This script exists because rebuilding the harness by hand costs 20 minutes and has three non-obvious failure modes (SQLite drop-in placeholders, a database-upgrade gate that blocks wp-admin, and a single-threaded PHP server that deadlocks on admin loopback requests). Read `references/testing-wp-plugins.md` for how to write the two kinds of test that matter — engine tests via `wp eval-file`, and real-HTTP admin-flow tests — plus the harness gotchas that will otherwise eat an hour.

Test both layers. Engine tests prove the data is right; only an HTTP test proves the *admin form* actually posts the field name your handler reads.

## Gotcha index

Full detail and the reasoning behind each in `references/wp-gotchas.md`. The ones that cost real time:

- `wp_nonce_url()` **HTML-escapes** the URL — feeding it to `wp_safe_redirect()` produces a broken `Location` header. Use `add_query_arg()`.
- **Only top-level menu items can have an icon.** `add_management_page()` (a Tools submenu) has no icon slot at all. Custom SVG icons go in as a base64 `data:` URI.
- `sanitize_title()` **percent-encodes** non-ASCII punctuation. A title like `SROM·18·2025` becomes the slug `srom%c2%b718%c2%b72025`. Set `post_name` explicitly from clean components.
- ACF **omits** `rewrite['slug']` when it equals the post type/taxonomy key (WP then defaults to the key) — so asserting on that array key gives a false failure. Assert on the actual `get_permalink()` / `get_term_link()` output.
- ACF **skips registration** for a post type/taxonomy that already exists, so re-registering within one request is a silent no-op.

## SROM (Studia Romologica) project

If the work touches `srom_article`, `srom_volume`, the importer, or the journal site, read `references/srom-project.md` first. It carries the content model, the CSV conventions, the three-plugin ownership split (importer / scholarly mu-plugin / Elementor templates), and the rename history — enough to avoid re-litigating decisions that are already settled.
