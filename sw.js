/* ============================================================
   THE OPERATOR'S CODEX — the offline copy

   Twenty-six layers of study material are worth more on a phone in a
   tunnel than on a desk with fibre, so the whole Codex is cached on
   this device and read from there first.

   Three strategies, one per kind of thing:

     the shell   (HTML, CSS, JS, fonts, doors, icons)
                 stale-while-revalidate — answered from the cache
                 instantly, refreshed in the background, so the next
                 load has the new deploy without ever showing a blank
                 page waiting for one.
     updates.json
                 network-first, cache fallback — the feed is the one
                 thing that must be current when there is signal and
                 must still be legible when there is not.
     images      cache-first, filled on first sight. The diagrams are
                 warmed in the background after install; the six
                 photographs are large, so they are only kept once
                 you have actually scrolled past them.

   Nothing here talks to any origin but this one, and nothing is ever
   sent anywhere — see privacy.html.
   ============================================================ */

/* Bump VERSION to force every device to throw its copy away and
   refetch. Ordinary deploys do not need it: the shell revalidates
   itself in the background on each load. */
var VERSION = 'v1';
var CACHE = 'codex-' + VERSION;

/* The smallest set that renders the whole Codex with the network
   switched off. Paths are relative so this works the same on a
   project path (/codex/) and on a custom domain. */
var SHELL = [
  './',
  'index.html',
  'privacy.html',
  'manifest.json',
  'icon.svg',
  'assets/codex.css',
  'assets/fonts.css',
  'assets/codex.js',
  'assets/doors.json',
  'node-log.json',
  'assets/fonts/fraunces-latin.woff2',
  'assets/fonts/fraunces-latin-ext.woff2',
  'assets/fonts/lexend-latin.woff2',
  'assets/fonts/lexend-latin-ext.woff2',
  'assets/fonts/spline-sans-mono-latin.woff2',
  'assets/fonts/spline-sans-mono-latin-ext.woff2',
  'images/icon-192.png',
  'images/icon-512.png',
  'images/icon-512-maskable.png',
  'updates.json'
];

function isFeed(url) {
  return url.pathname.split('/').pop() === 'updates.json';
}

function isImage(url) {
  return /\/images\//.test(url.pathname) ||
         /\.(?:svg|png|jpe?g|webp|woff2?)$/i.test(url.pathname);
}

/* ---------------------------------------------------------- install */
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      /* one at a time and forgiving: a single 404 must not leave the
         browser with no service worker at all */
      return Promise.all(SHELL.map(function (u) {
        return c.add(new Request(u, { cache: 'reload' })).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

/* --------------------------------------------------------- activate */
self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        return k === CACHE ? null : caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
      .then(warmFigures)
  );
});

/* Every diagram the page references, pulled quietly after install so
   the layers are complete offline on the first visit. Read out of the
   shipped HTML rather than a list kept here, so a new figure needs no
   change to this file. Only the vector diagrams — the photographs are
   hundreds of kilobytes each and are cached when they are first seen. */
function warmFigures() {
  return caches.open(CACHE).then(function (c) {
    return c.match('index.html').then(function (r) {
      if (!r) return null;
      return r.text().then(function (html) {
        var seen = {}, want = [], m;
        var re = /src="(images\/[^"]+\.svg)"/g;
        while ((m = re.exec(html))) {
          if (!seen[m[1]]) { seen[m[1]] = 1; want.push(m[1]); }
        }
        return Promise.all(want.map(function (u) {
          return c.match(u).then(function (hit) {
            return hit ? null : c.add(u).catch(function () {});
          });
        }));
      });
    });
  }).catch(function () {});
}

/* ------------------------------------------------------------ fetch */
self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  var url;
  try { url = new URL(req.url); } catch (err) { return; }
  if (url.origin !== self.location.origin) return;

  if (isFeed(url)) { e.respondWith(feedFirst(req)); return; }
  if (isImage(url)) { e.respondWith(cacheFirst(req)); return; }
  e.respondWith(shell(req));
});

/* the feed: fresh whenever there is signal, readable when there is not.
   ignoreSearch because a cache-busting query must not hide the copy. */
function feedFirst(req) {
  return fetch(req).then(function (res) {
    if (res && res.ok) {
      var copy = res.clone();
      caches.open(CACHE).then(function (c) { c.put('updates.json', copy); });
    }
    return res;
  }).catch(function () {
    return caches.match(req, { ignoreSearch: true }).then(function (hit) {
      return hit || Response.error();
    });
  });
}

function cacheFirst(req) {
  return caches.match(req, { ignoreSearch: true }).then(function (hit) {
    if (hit) return hit;
    return fetch(req).then(function (res) {
      if (res && res.ok && res.type === 'basic') {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    });
  });
}

/* stale-while-revalidate, with index.html as the offline landing for
   any navigation that has never been visited before */
function shell(req) {
  return caches.match(req, { ignoreSearch: true }).then(function (hit) {
    var live = fetch(req).then(function (res) {
      if (res && res.ok && res.type === 'basic') {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () {
      return hit || (req.mode === 'navigate' ? caches.match('index.html') : Response.error());
    });
    return hit || live;
  });
}
