#!/usr/bin/env bash
# Bootstrap a disposable WordPress + SQLite + ACF(free) site for plugin testing.
# No MySQL required. Idempotent-ish: pass --fresh to wipe the database first.
#
#   bash setup-wp-test-site.sh <target-dir> [path/to/your-plugin ...] [--fresh]
#
# Then:
#   cd <target-dir>/wordpress
#   php -d error_reporting='E_ALL & ~E_DEPRECATED' ../wp-cli.phar eval-file ../my-test.php
#   PHP_CLI_SERVER_WORKERS=6 php -S localhost:8899   # admin at /wp-admin (admin/admin)
#
# Encodes four things that silently break a hand-rolled harness:
#   1. the SQLite drop-in needs its placeholders substituted
#   2. `core update-db` or wp-admin shows "Database Update Required" instead of your plugin
#   3. the PHP dev server must be multi-worker or WP admin loopback requests deadlock
#   4. pretty permalinks must be ON before bootstrap for rewrite-slug assertions
set -euo pipefail

TARGET="${1:?usage: setup-wp-test-site.sh <target-dir> [plugin-dir ...] [--fresh]}"; shift
FRESH=0; PLUGINS=()
for arg in "$@"; do
  if [ "$arg" = "--fresh" ]; then FRESH=1; else PLUGINS+=("$arg"); fi
done

PHP="${PHP:-php}"
WP="$TARGET/wordpress"
CLI="$TARGET/wp-cli.phar"
# memory_limit: wp-cli's zip extractor blows PHP's default 128M unpacking current
# WordPress and dies mid-extract, leaving a half-built wordpress/ with no wp-content.
PHPARGS=(-d error_reporting='E_ALL & ~E_DEPRECATED' -d memory_limit=512M)
# Filter deprecation noise from stderr but PRESERVE the exit code — swallowing it
# (`|| true`) turns a fatal into a silent half-built install that fails later,
# somewhere confusing.
wpcli() { "$PHP" "${PHPARGS[@]}" "$CLI" "$@" 2> >(grep -v 'Deprecated' >&2 || true); }

mkdir -p "$TARGET"

# --- wp-cli -----------------------------------------------------------------
if [ ! -f "$CLI" ]; then
  echo "==> fetching wp-cli"
  curl -sL --max-time 90 -o "$CLI" \
    https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
fi

# --- core -------------------------------------------------------------------
if [ ! -f "$WP/wp-load.php" ]; then
  echo "==> downloading WordPress core"
  wpcli core download --path="$WP" --force >/dev/null
fi
# Fail fast and loudly rather than several steps later with an unrelated error.
if [ ! -f "$WP/wp-load.php" ] || [ ! -d "$WP/wp-content/plugins" ]; then
  echo "FATAL: WordPress core is incomplete at $WP (extraction failed?)." >&2
  exit 1
fi
cd "$WP"

# --- SQLite drop-in ---------------------------------------------------------
if [ ! -f "$WP/wp-content/db.php" ]; then
  echo "==> installing SQLite integration"
  curl -sL --max-time 90 -o /tmp/sqlite-int.zip \
    https://downloads.wordpress.org/plugin/sqlite-database-integration.zip
  rm -rf "$WP/wp-content/plugins/sqlite-database-integration"
  unzip -q -o /tmp/sqlite-int.zip -d "$WP/wp-content/plugins/"
  mkdir -p "$WP/wp-content/database"
  cp "$WP/wp-content/plugins/sqlite-database-integration/db.copy" "$WP/wp-content/db.php"
  # The drop-in ships with placeholders; unsubstituted, WordPress demands MySQL.
  "$PHP" -r '
    $f = "wp-content/db.php"; $s = file_get_contents($f);
    $s = str_replace("{SQLITE_IMPLEMENTATION_FOLDER_PATH}",
          dirname(__FILE__)."/wp-content/plugins/sqlite-database-integration", $s);
    $s = str_replace("{SQLITE_PLUGIN}", "sqlite-database-integration/load.php", $s);
    file_put_contents($f, $s);'
fi

[ -f "$WP/wp-config.php" ] || wpcli config create --dbname=wp --dbuser=root --dbpass= \
  --dbhost=localhost --skip-check --force >/dev/null

[ "$FRESH" = "1" ] && rm -f "$WP/wp-content/database/.ht.sqlite"

# --- ACF (free) -------------------------------------------------------------
if [ ! -d "$WP/wp-content/plugins/advanced-custom-fields" ]; then
  echo "==> installing ACF (free)"
  curl -sL --max-time 120 -o /tmp/acf.zip \
    https://downloads.wordpress.org/plugin/advanced-custom-fields.zip
  unzip -q -o /tmp/acf.zip -d "$WP/wp-content/plugins/"
fi

# --- your plugin(s) ---------------------------------------------------------
ACTIVATE=(advanced-custom-fields)
for p in "${PLUGINS[@]:-}"; do
  [ -z "$p" ] && continue
  name="$(basename "$p")"
  echo "==> linking plugin: $name"
  rm -rf "$WP/wp-content/plugins/$name"
  cp -R "$p" "$WP/wp-content/plugins/"
  ACTIVATE+=("$name")
done

# --- install ----------------------------------------------------------------
echo "==> installing WordPress"
wpcli core install --url=http://localhost:8899 --title="Test" \
  --admin_user=admin --admin_password=admin --admin_email=test@example.com --skip-email >/dev/null

# Pretty permalinks BEFORE anything registers, so rewrite slugs actually materialise.
wpcli option update permalink_structure '/%postname%/' >/dev/null
# Without this, every wp-admin page over HTTP is the "Database Update Required" screen.
wpcli core update-db >/dev/null

wpcli plugin activate "${ACTIVATE[@]}" >/dev/null
wpcli rewrite flush >/dev/null

cat <<EOF

Ready: $WP   (admin / admin)

  engine test:  cd "$WP" && $PHP -d error_reporting='E_ALL & ~E_DEPRECATED' ../wp-cli.phar eval-file ../my-test.php
  http  test:   cd "$WP" && PHP_CLI_SERVER_WORKERS=6 $PHP -S localhost:8899
                (PHP_CLI_SERVER_WORKERS is required — the single-threaded server
                 deadlocks on WordPress admin loopback requests)
EOF
