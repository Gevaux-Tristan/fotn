// fotn service worker — offline app shell + asset cache
const CACHE = 'fotn-v18';
const CORE = [
  './', './index.html', './manifest.webmanifest',
  './generic.jpg?v=2',
  './fonts/anaheim-latin.woff2?v=1',
  './favicon.svg?v=11', './icon.svg?v=11', './icon-192.png?v=11', './icon-512.png?v=11', './apple-touch-icon.png?v=11',
  './luts/portra400.png', './luts/pro400h.png', './luts/gold200.png', './luts/colorplus200.png',
  './luts/kodacolor100.png', './luts/ultramax400.png', './luts/velvia100.png', './luts/hp5.png',
  './luts/signature1.png',
  './luts/ilford-xp2-super400.png', './luts/lomochrome-purple-xr.png', './luts/neopan-acros-100.png', './luts/polaroid-type100-sepia.png', './luts/rollei-cn-200.png', './luts/lomochrome-metropolis-xr100.jpg',
  './luts/kodachrome40.png',
  './luts/agfaoptima.png', './luts/fujiinstax.png',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.all(CORE.map(u => c.add(u).catch(() => {})))) // tolerate any 404
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Page loads: serve the cached shell INSTANTLY (no blank wait on the network),
  // then refetch a fresh copy in the background so the next open is up to date.
  if (req.mode === 'navigate') {
    e.respondWith(
      caches.match('./index.html').then(hit => {
        const update = fetch('./index.html', {cache: 'reload'}).then(res => {
          caches.open(CACHE).then(c => c.put('./index.html', res.clone()));
          return res;
        }).catch(() => hit);
        return hit || update;
      })
    );
    return;
  }

  // Same-origin assets: cache-first, then network (and cache it).
  if (url.origin === self.location.origin) {
    e.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
        return res;
      }).catch(() => hit))
    );
  }
});
