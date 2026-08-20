const CACHE_NAME = 'meteoinfo-v5';
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

// Načítání: Nejprve zkusit síť, když není internet, vzít z cache
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        // Pokud síť odpověděla úspěšně, vrátíme čerstvá data
        return networkResponse;
      })
      .catch(() => {
        // Pokud nejde internet, zkusíme nouzově cache
        return caches.match(event.request);
      })
  );
});