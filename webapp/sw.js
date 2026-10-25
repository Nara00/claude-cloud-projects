// Service Worker: cachea el shell y responde desde los caches city-<id>/* para audios.
const SHELL = "shell-v1";
const SHELL_URLS = [
  "./",
  "index.html",
  "css/styles.css",
  "js/app.js",
  "data/tours.json",
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
  "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
];

self.addEventListener("install", (e) => {
  e.waitUntil((async () => {
    const cache = await caches.open(SHELL);
    await Promise.all(SHELL_URLS.map(u => cache.add(u).catch(() => null)));
    self.skipWaiting();
  })());
});

self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith("shell-") && k !== SHELL).map(k => caches.delete(k)));
    self.clients.claim();
  })());
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET") return;

  // Audio: cache-first contra el cache de la ciudad correspondiente
  if (url.pathname.includes("/audio/")) {
    const m = url.pathname.match(/\/audio\/([^/]+)\//);
    const cacheName = m ? "city-" + m[1] : "shell-fallback";
    e.respondWith((async () => {
      const cached = await caches.match(e.request);
      if (cached) return cached;
      try {
        const res = await fetch(e.request);
        if (res.ok && m) {
          const cache = await caches.open(cacheName);
          cache.put(e.request, res.clone());
        }
        return res;
      } catch (err) { return new Response("Offline y no está en el cache", { status: 503 }); }
    })());
    return;
  }

  // Tiles de mapa: cache-first con fallback a red
  if (url.hostname.endsWith(".tile.openstreetmap.org")) {
    e.respondWith((async () => {
      const cached = await caches.match(e.request);
      if (cached) return cached;
      try {
        const res = await fetch(e.request);
        if (res.ok) { const c = await caches.open("tiles-osm"); c.put(e.request, res.clone()); }
        return res;
      } catch { return new Response("", { status: 503 }); }
    })());
    return;
  }

  // Shell: cache-first con revalidación simple
  e.respondWith((async () => {
    const cached = await caches.match(e.request);
    if (cached) return cached;
    try {
      const res = await fetch(e.request);
      if (res.ok && (url.origin === self.location.origin || url.hostname === "unpkg.com")) {
        const c = await caches.open(SHELL);
        c.put(e.request, res.clone());
      }
      return res;
    } catch { return new Response("Offline", { status: 503 }); }
  })());
});
