self.addEventListener("install", event => {
  event.waitUntil(
    caches.open("static-cache").then(cache => {
      return cache.addAll([
        "/",
        "/login",
        "/register",
        "/static/manifest.json",
        "/static/icon-192.png",
        "/static/icon-512.png"
      ]);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});

