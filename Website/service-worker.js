const CACHE_NAME = 'churn-predictor-cache-v2';
const urlsToCache = [
  '/',
  '/static/app.js',
  '/static/styles.css',
  '/static/icon_web_white.png',
  '/static/so_icon_web2.png',
  '/static/so_icon_web.png',
  '/static/offline.html',
];

// Evento de instalação — faz cache dos ficheiros essenciais
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Installed');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .catch(err => {
        console.error('[ServiceWorker] Cache failed:', err);
      })
  );
});

// Evento de ativação — remove caches antigos
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activated');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
});

// Evento de fetch — tenta ir ao cache primeiro, depois à rede, se nao funcionar mostra a pag offline.html
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Se existir no cache, devolve
        if (response) {
          return response;
        }
        // Senão, tenta fetch normal
        return fetch(event.request)
          .catch(() => {
            // Se falhar (offline), devolve offline.html se for um pedido de página (HTML)
            if (event.request.mode === 'navigate') {
              return caches.match('/static/offline.html');
            }
          });
      })
  );
});
