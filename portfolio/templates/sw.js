var staticCacheName = "django-pwa-v" + new Date().getTime();

var filesToCache = [
    '/offline/',
    '/pl/offline/',
    '/manifest.json',
    '/static/css/django-pwa-app.css',
    '/static/images/icons/icon-72x72.png',
    '/static/images/icons/icon-96x96.png',
    '/static/images/icons/icon-128x128.png',
    '/static/images/icons/icon-144x144.png',
    '/static/images/icons/icon-152x152.png',
    '/static/images/icons/icon-192x192.png',
    '/static/images/icons/icon-384x384.png',
    '/static/images/icons/icon-512x512.png',
    '/static/images/icons/splash-640x1136.png',
    '/static/images/icons/splash-750x1334.png',
    '/static/images/icons/splash-1242x2208.png',
    '/static/images/icons/splash-1125x2436.png',
    '/static/images/icons/splash-828x1792.png',
    '/static/images/icons/splash-1242x2688.png',
    '/static/images/icons/splash-1536x2048.png',
    '/static/images/icons/splash-1668x2224.png',
    '/static/images/icons/splash-1668x2388.png',
    '/static/images/icons/splash-2048x2732.png'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from cache (Network-first, GET requests only!)
self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') {
        event.respondWith(fetch(event.request));
        return;
    }

    if (event.request.url.startsWith('chrome-extension://')) {
        return; // Skip caching for chrome extensions
    }

    if (event.request.url.match('amazonaws.com')) {
        return; // Skip caching for chrome extensions
    }

    if(event.request.url.match(/googletagmanager/)){
        return; // Hack for GTM
    }

    event.respondWith(
        fetch(event.request)
            .then(response => {
                const clonedResponse = response.clone();
                caches.open(staticCacheName).then(cache => {
                    cache.put(event.request, clonedResponse);
                });
                return response;
            })
            .catch(() => {
                return caches.match(event.request).then(cachedResponse => {
                    return cachedResponse || caches.match('/offline/');
                })
            })
    );
});
