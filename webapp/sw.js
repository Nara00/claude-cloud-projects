// Service Worker con manejo de Range requests para audio offline.
const SHELL = "shell-v2";
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

// Devuelve una Response 206 Partial Content a partir de una Response completa cacheada,
// honrando el header Range del request original (necesario para <audio> en Safari/iOS).
async function rangedFromCache(cachedResponse, request) {
  const buffer = await cachedResponse.clone().arrayBuffer();
  const size = buffer.byteLength;
  const rangeHeader = request.headers.get("range");
  if (!rangeHeader) {
    return new Response(buffer, {
      status: 200,
      headers: {
        "Content-Type": cachedResponse.headers.get("Content-Type") || "audio/mpeg",
        "Content-Length": size,
        "Accept-Ranges": "bytes",
      },
    });
  }
  const match = /bytes=(\d*)-(\d*)/.exec(rangeHeader);
  const start = match && match[1] ? parseInt(match[1], 10) : 0;
  const end = match && match[2] ? parseInt(match[2], 10) : size - 1;
  const slice = buffer.slice(start, end + 1);
  return new Response(slice, {
    status: 206,
    statusText: "Partial Content",
    headers: {
      "Content-Type": cachedResponse.headers.get("Content-Type") || "audio/mpeg",
      "Content-Length": slice.byteLength,
      "Content-Range": `bytes ${start}-${end}/${size}`,
      "Accept-Ranges": "bytes",
    },
  });
}

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET") return;

  // Audio: cache-first contra el cache de la ciudad, con Range correcto.
  if (url.pathname.includes("/audio/")) {
    const m = url.pathname.match(/\/audio\/([^/]+)\//);
    const cacheName = m ? "city-" + m[1] : null;
    e.respondWith((async () => {
      // Buscamos por URL (no por request): la entrada guardada no tiene Range
      const cacheKey = new Request(url.pathname + url.search);
      let cached;
      if (cacheName) {
        const cache = await caches.open(cacheName);
        cached = await cache.match(cacheKey, { ignoreSearch: false });
        if (!cached) cached = await cache.match(e.request.url);
      }
      if (!cached) cached = await caches.match(e.request.url);
      if (cached) {
        try { return await rangedFromCache(cached, e.request); }
        catch (err) { /* seguir al fetch */ }
      }
      try {
        const res = await fetch(e.request);
        if (res.ok && cacheName && !e.request.headers.get("range")) {
          const cache = await caches.open(cacheName);
          cache.put(cacheKey, res.clone()).catch(() => null);
        }
        return res;
      } catch (err) {
        return new Response("Audio no disponible sin conexión", { status: 503 });
      }
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
