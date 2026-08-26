const CACHE_VERSION = "giosmart-v20260826-5";
const CACHE_PREFIX = "giosmart-v";
const APP_SHELL = [
  "/",
  "/services",
  "/contact",
  "/css/bootstrap.min.css",
  "/css/custom.css?v=20260826-5",
  "/css/slicknav.min.css",
  "/css/all.min.css",
  "/js/jquery-3.7.1.min.js",
  "/js/jquery.slicknav.js",
  "/js/function.js?v=20260826-5",
  "/images/logo.svg",
  "/images/favicon.png",
  "/images/apple-touch-icon.png",
  "/images/pwa-icon-192.png",
  "/images/pwa-icon-512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((key) => key.startsWith(CACHE_PREFIX) && key !== CACHE_VERSION)
          .map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(async () => (
          await caches.match(request) || await caches.match("/")
        ))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        if (!response.ok) return response;
        const copy = response.clone();
        caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy));
        return response;
      });
    })
  );
});
