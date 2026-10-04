# Testing WordPress plugins for real

A disposable WordPress + SQLite + ACF install costs ~1 minute to build and is the only thing that catches the bugs that matter in this domain. `scripts/setup-wp-test-site.sh` automates it.

## Why bother (the case that settles it)

An ACF field rename passed every static check — clean grep, clean lint, no leftover references. The import then reported **"8 created, 0 errors"** and created **zero** of the linked posts it was supposed to create, because a field name collided with a spreadsheet column. Nothing short of running it against real data and asserting on the resulting database state would have found it.

## Two kinds of test — you need both

**Engine tests** (`wp eval-file`) — fast, cover the data layer: definitions install, import runs, values land, idempotency holds.

**HTTP tests** (Python + `urllib` + `http.cookiejar`) — cover what engine tests structurally cannot:
- the admin form actually emits the field name the handler reads (`opt_link_volumes` on both ends)
- nonces, capabilities, redirects (the `wp_nonce_url` bug is *only* visible here)
- the AJAX batch loop
- rendered admin screens contain what you claim (e.g. that ACF's own Post Types screen really lists your CPT as an editable row)

An engine test that sets `$job['options']['link_volumes'] = 1` directly proves nothing about whether the checkbox is named `opt_link_volumes`.

## Harness gotchas (each cost ~20 minutes)

**Raise `memory_limit` for wp-cli.** `wp core download` extracts the WordPress zip in-process and blows PHP's default 128M on current WP, dying *mid-extract*. It leaves a `wordpress/` directory with no `wp-content`, so the next step fails with a baffling "cannot create extraction directory". Run wp-cli with `-d memory_limit=512M`.

**Never `|| true` a setup step.** Swallowing a wp-cli exit code turns a fatal into a half-built install that explodes three steps later somewhere unrelated. Fail loudly, and assert the install is complete (`wp-load.php` **and** `wp-content/plugins` both exist) before continuing.

**SQLite drop-in placeholders.** Copy `sqlite-database-integration/db.copy` → `wp-content/db.php` and substitute `{SQLITE_IMPLEMENTATION_FOLDER_PATH}` and `{SQLITE_PLUGIN}`. Skip this and WP demands MySQL.

**Run `wp core update-db` after install.** Otherwise every wp-admin page over HTTP returns *"Database Update Required"* instead of your plugin, and every content assertion fails confusingly.

**`PHP_CLI_SERVER_WORKERS=6`.** PHP's built-in server is single-threaded; WordPress admin makes loopback requests to itself and **deadlocks**. Symptom: login POST hangs until timeout.

**Enable pretty permalinks *before* bootstrap** if you assert on slugs (`wp option update permalink_structure '/%postname%/'`). ACF/WP only materialise rewrite slugs when they're on.

**`wp eval-file` scope.** Top-level `$vars` in an eval-file are **not** globals. A counter incremented via `global $F;` inside a helper won't be the same `$F` you read at the end (you'll print "all 0 checks passed"). Use `$GLOBALS['F']` consistently in both places.

**Test isolation.** Suites sharing one database leak: posts from a previous run make the next import report `updated` instead of `created`. Either drop the DB between suites or delete the CPT's posts at the top of each test.

## Assertion discipline

**Guard against false positives.** `(int) get_field('volume',$a) === (int) $vol->ID` passes when both are 0 — i.e. exactly when the feature is broken. Assert concrete expected values (`'18-2025' === $vol->post_name`), and assert the *count* of things created, not just their equality to each other.

**Assert on observable behaviour, not config.** Not `$tax->rewrite['slug'] === 'autor'` (ACF omits that key legitimately) but `str_contains( get_term_link($id,'autor'), '/autor/' )`.

**Print distinct log messages** from a preview/import rather than only counts. Counts hide "this field was skipped 8 times".

## Test skeleton (engine)

```php
error_reporting( E_ALL & ~E_DEPRECATED );
$GLOBALS['F'] = 0; $GLOBALS['T'] = 0;
function ck( $label, $cond, $detail = '' ) {
    $GLOBALS['T']++;
    if ( $cond ) { echo "  ok   $label\n"; }
    else { $GLOBALS['F']++; echo "  FAIL $label" . ( '' !== $detail ? "  [$detail]" : '' ) . "\n"; }
}
wp_set_current_user( 1 );

// clean slate so created/updated counts mean something
foreach ( array('srom_article','srom_volume') as $pt ) {
    foreach ( get_posts(array('post_type'=>$pt,'post_status'=>'any','numberposts'=>-1,'fields'=>'ids')) as $id ) {
        wp_delete_post( $id, true );
    }
}

// … exercise the plugin, assert on DB state …

echo $GLOBALS['F'] ? "RESULT: {$GLOBALS['F']} of {$GLOBALS['T']} FAILED\n" : "RESULT: all {$GLOBALS['T']} passed\n";
```

Run: `php -d error_reporting='E_ALL & ~E_DEPRECATED' wp-cli.phar eval-file ../test-x.php`

## Test skeleton (HTTP admin)

```python
import urllib.request as rq, http.cookiejar as cj
from urllib.parse import urlencode
BASE = "http://localhost:8899"
jar = cj.CookieJar(); op = rq.build_opener(rq.HTTPCookieProcessor(jar))
def get(u):     return op.open(u, timeout=20).read().decode("utf-8","replace")
def post(u, d): return op.open(rq.Request(u, data=urlencode(d).encode()), timeout=20).read().decode("utf-8","replace")

get(BASE + "/wp-login.php")   # sets the test cookie
post(BASE + "/wp-login.php", {"log":"admin","pwd":"admin","wp-submit":"Log In",
                              "redirect_to":BASE+"/wp-admin/","testcookie":"1"})

html = get(BASE + "/wp-admin/admin.php?page=my-plugin")
assert "Fatal error" not in html
```
If admin pages come back without expected content, check you're not looking at the login form or the DB-upgrade gate — assert positively (`"Dashboard" in html`) before trusting any negative assertion.

## Verify against the *packaged* artifact

Before declaring done, unzip the built plugin zip into the test site and run the suite against **that**, not your working directory. It's the only proof the thing you're shipping is the thing you tested.
