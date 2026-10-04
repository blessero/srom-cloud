/* Scholar Audit — offline shell.
   Network-first for the app itself, so a redeploy is picked up on the next
   load rather than being pinned by the cache. API calls are never cached:
   this is a verification tool and a stale citation count is worse than no
   answer at all. Bump CACHE on every deploy. */
const CACHE = "srom-audit-v6";
const SHELL = ["./", "./index.html", "./app.css", "./fonts.css", "./js/i18n.js", "./js/core.js", "./js/scholar.js", "./js/dossier.js", "./js/library.js", "./js/directory.js", "./js/reviewers.js", "./js/app.js", "./manifest.webmanifest", "./icons/wheel.svg", "./icons/icon-192.png", "./icons/icon-512.png", "./fonts/epilogue-normal-400-800-latin-ext.woff2", "./fonts/epilogue-normal-400-800-latin.woff2", "./fonts/fraunces-italic-400-600-latin-ext.woff2", "./fonts/fraunces-italic-400-600-latin.woff2", "./fonts/fraunces-normal-400-650-latin-ext.woff2", "./fonts/fraunces-normal-400-650-latin.woff2", "./fonts/plexmono-normal-400-latin-ext.woff2", "./fonts/plexmono-normal-400-latin.woff2", "./fonts/plexmono-normal-500-latin-ext.woff2", "./fonts/plexmono-normal-500-latin.woff2", "./fonts/plexmono-normal-600-latin-ext.woff2", "./fonts/plexmono-normal-600-latin.woff2"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const { request } = e;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;   // never touch the APIs

  // Fonts and icons never change under a given name: cache-first.
  if (/\/(fonts|icons)\//.test(url.pathname)){
    e.respondWith(caches.match(request).then(r => r || fetch(request)));
    return;
  }
  e.respondWith(
    fetch(request)
      .then(r => {
        if (r.ok){ const copy = r.clone(); caches.open(CACHE).then(c => c.put(request, copy)).catch(() => {}); }
        return r;
      })
      .catch(() => caches.match(request, { ignoreSearch:true }).then(r => r || caches.match("./index.html")))
  );
});
