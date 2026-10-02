const CACHE_NAME = 'mdk-pwa-v2';
const urlsToCache = [
  '/static/manifest.json',
  '/static/logo.png',
  '/static/icon-192.png',
  '/static/icon-512.png'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;

  if (request.method !== 'GET') {
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match('/static/manifest.json'))
    );
    return;
  }

  const url = new URL(request.url);
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then((response) => {
        return response || fetch(request).then((resp) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, resp.clone());
            return resp;
          });
        });
      })
    );
    return;
  }

  event.respondWith(fetch(request));
});