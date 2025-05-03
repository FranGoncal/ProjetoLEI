self.addEventListener('install', function(e) {
    console.log('[ServiceWorker] Installed');
});
  
self.addEventListener('activate', function(e) {
    console.log('[ServiceWorker] Activated');
});

self.addEventListener('fetch', function(event) {
    event.respondWith(fetch(event.request));
});
  


