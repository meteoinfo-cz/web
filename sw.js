const CACHE_NAME = 'meteoinfo-v3';
const urlsToCache = [
  '/web/',
  '/web/index.html',
  '/web/manifest.json'
];

// Instalace a uložení souborů do cache
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
  // Vynutí okamžitou aktivaci nového Service Workeru
  self.skipWaiting();
});

// Aktivace a čištění staré cache
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Načítání ze sítě nebo z cache (Network falling back to cache nebo naopak)
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Pokud je soubor v cache, vrátí ho, jinak se podívá do sítě
        return response || fetch(event.request);
      })
  );
});