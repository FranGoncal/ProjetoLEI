const CACHE_NAME = 'my-cache-v1'; // Nome do cache
const urlsToCache = [
  '/', // A página principal
  '/index.html', // Página de índice
  '/static/icon_web_1.png', // Ícones
  '/static/styles.css', // Arquivo CSS
  // Adicione outros arquivos estáticos que você deseja armazenar
];

self.addEventListener('install', (event) => {
  // Durante a instalação, cache os arquivos
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching all the static files');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('activate', (event) => {
  // Durante a ativação, remova os caches antigos
  const cacheWhitelist = [CACHE_NAME];
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            console.log('[Service Worker] Deleting old cache', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Intercepte as requisições e forneça a versão em cache se disponível
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Se o arquivo estiver no cache, use-o
        if (response) {
          console.log('[Service Worker] Returning from cache:', event.request.url);
          return response;
        }
        // Caso contrário, faça uma requisição de rede
        console.log('[Service Worker] Fetching from network:', event.request.url);
        return fetch(event.request);
      })
  );
});
