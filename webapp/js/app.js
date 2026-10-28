// Audioguías PWA. Rutas por hash. Descarga por ciudad.
const DATA_URL = "data/tours.json";
// safe() replica scripts/generar_audio_gemini.py: quita los caracteres no permitidos del filename.
const safeFilename = (name) => name.replace(/[\\/:*?"<>|]/g, "").trim();
const AUDIO_PATH = (city, tour, n, name) => `audio/${city}/${tour}/${String(n).padStart(2,"0")} - ${safeFilename(name)}.mp3`;

const $ = sel => document.querySelector(sel);
const el = (tag, props = {}, ...children) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === "class") n.className = v;
    else if (k === "html") n.innerHTML = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v);
  }
  for (const c of children.flat()) {
    if (c == null) continue;
    n.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return n;
};

let DATA;              // tours.json
let AUDIO = $("#audio");
let PLAYING = null;    // {cityId, tourId, stopN}
let QUEUE = null;      // array of stops in current tour

// -------- Service worker + descargas por ciudad --------
async function registerSW() {
  if ("serviceWorker" in navigator) {
    try { await navigator.serviceWorker.register("sw.js"); }
    catch (e) { console.warn("SW no registrado:", e); }
  }
}

function cityUrls(city, cityId) {
  const urls = [];
  for (const t of city.tours) {
    for (const s of t.stops) {
      urls.push(AUDIO_PATH(cityId, t.id, s.n, s.name));
    }
    if (t.map_url) urls.push(t.map_url);
  }
  return urls;
}

async function cityStatus(cityId) {
  // Devuelve {done, total} con cuántos MP3 de esa ciudad están en el cache.
  if (!("caches" in window)) return { done: 0, total: 0 };
  const cache = await caches.open("city-" + cityId);
  const keys = await cache.keys();
  const urls = cityUrls(DATA.cities[cityId], cityId);
  const have = new Set(keys.map(r => new URL(r.url).pathname.replace(/^\//, "")));
  const done = urls.filter(u => have.has(u) || have.has("/" + u) || have.has(u.replace(/\s/g, "%20"))).length;
  return { done, total: urls.length };
}

async function downloadCity(cityId, onProgress) {
  const city = DATA.cities[cityId];
  const urls = cityUrls(city, cityId);
  const cache = await caches.open("city-" + cityId);
  let done = 0, failed_urls = [];
  for (const u of urls) {
    try {
      const match = await cache.match(u);
      if (!match) {
        const isExternal = /^https?:\/\//.test(u) && !u.startsWith(location.origin);
        const req = isExternal ? new Request(u, { mode: "no-cors" }) : new Request(u, { cache: "no-cache" });
        const res = await fetch(req);
        if (res.ok || res.type === "opaque") await cache.put(u, res.clone());
        else failed_urls.push({ url: u, reason: `HTTP ${res.status}` });
      }
    } catch (e) { failed_urls.push({ url: u, reason: e.message || "error de red" }); }
    done++;
    onProgress({ done, total: urls.length, failed: failed_urls.length });
  }
  try { localStorage.setItem("fallidos_" + cityId, JSON.stringify(failed_urls)); } catch {}
  return { done, total: urls.length, failed: failed_urls };
}

function getFailed(cityId) {
  try { return JSON.parse(localStorage.getItem("fallidos_" + cityId) || "[]"); }
  catch { return []; }
}

async function stopIsCached(cityId, tourId, stopN, stopName) {
  if (!("caches" in window)) return false;
  const url = AUDIO_PATH(cityId, tourId, stopN, stopName);
  const cache = await caches.open("city-" + cityId);
  const match = await cache.match(url);
  return !!match;
}

async function deleteCity(cityId) {
  if (!("caches" in window)) return;
  await caches.delete("city-" + cityId);
}

// -------- Vistas --------
function viewCities() {
  $("#title").textContent = "Audioguías";
  $("#back").hidden = true;
  $("#appbar").classList.remove("on-dark");
  const root = $("#root");
  root.innerHTML = "";
  root.append(el("section", { class: "hero" },
    el("div", { class: "dot d1" }),
    el("h2", {}, "Elegí tu próxima parada"),
    el("p", {}, "Descargá una ciudad, salí a caminar y escuchá sin internet."),
  ));
  const grid = el("div", { class: "city-grid" });
  let i = 0;
  for (const [cid, city] of Object.entries(DATA.cities)) {
    const n_tours = city.tours.length;
    const n_stops = city.tours.reduce((s, t) => s + t.stops.length, 0);
    const card = el("div", { class: "city-card c-" + (i % 6), onclick: () => (location.hash = "#/ciudad/" + cid) },
      el("div", { class: "blob" }),
      el("div", { class: "arrow" }, "›"),
      el("div", {},
        el("h3", {}, city.name),
        el("div", { class: "sub" }, `${n_tours} ${n_tours === 1 ? "tour" : "tours"} · ${n_stops} paradas`),
      ),
    );
    const row = el("div", { class: "pkg-row", onclick: ev => ev.stopPropagation() });
    const status = el("span", { class: "status" }, "...");
    const dl = el("button", { class: "small" }, "Descargar");
    const rm = el("button", { class: "small danger" }, "Eliminar");
    const prog = el("progress", { max: 100, value: 0 });
    row.append(status, prog, dl, rm);
    card.append(row);
    grid.append(card);
    i++;

    const errList = el("div", { class: "err-list" });
    card.append(errList);
    const refresh = async () => {
      const { done, total } = await cityStatus(cid);
      const failed = getFailed(cid);
      if (total === 0) { status.textContent = "sin tours"; dl.disabled = true; rm.disabled = true; return; }
      if (done === 0) { status.textContent = `0 / ${total}`; status.className = "status"; rm.disabled = true; }
      else if (done < total) { status.textContent = `${done} / ${total} descargados`; status.className = "status err"; rm.disabled = false; }
      else { status.textContent = `${total} / ${total} ✓ sin internet`; status.className = "status ok"; rm.disabled = false; }
      errList.innerHTML = "";
      if (failed.length) {
        const names = failed.map(f => f.url.split("/").slice(-2).join(" / "));
        errList.append(el("details", {},
          el("summary", {}, `${failed.length} con error — tocá para ver`),
          el("ul", {}, ...names.map(n => el("li", {}, n))),
          el("button", { class: "small", onclick: async () => {
            dl.disabled = true; row.classList.add("loading");
            await downloadCity(cid, ({ done, total, failed }) => {
              prog.value = Math.round(done / total * 100);
              status.textContent = `${done} / ${total}` + (failed ? ` (${failed})` : "");
            });
            row.classList.remove("loading"); dl.disabled = false; await refresh();
          } }, "Reintentar los que fallaron"),
        ));
      }
    };
    refresh();

    dl.onclick = async () => {
      dl.disabled = true; rm.disabled = true; row.classList.add("loading");
      status.textContent = "Descargando..."; status.className = "status";
      await downloadCity(cid, ({ done, total, failed }) => {
        prog.value = Math.round(done / total * 100);
        status.textContent = `${done} / ${total}` + (failed ? ` (${failed} con error)` : "");
      });
      row.classList.remove("loading");
      dl.disabled = false; await refresh();
    };
    rm.onclick = async () => {
      if (!confirm(`¿Eliminar los audios de ${city.name}?`)) return;
      await deleteCity(cid); await refresh();
    };
  }
  root.append(grid);
}

function viewCity(cityId) {
  const city = DATA.cities[cityId];
  if (!city) { location.hash = ""; return; }
  $("#title").textContent = city.name;
  $("#back").hidden = false;
  $("#appbar").classList.remove("on-dark");
  $("#back").onclick = () => (location.hash = "");
  const root = $("#root");
  root.innerHTML = "";

  const mapDiv = el("div", { id: "map" });
  root.append(mapDiv);

  const grid = el("div", { class: "tour-grid" });
  let i = 0;
  for (const t of city.tours) {
    const minutes = Math.round(t.stops.length * 2.5); // estimación aproximada
    const card = el("div", { class: "tour-card t-" + (i % 11), onclick: () => (location.hash = `#/tour/${cityId}/${t.id}`) },
      el("div", { class: "face" }),
      el("div", { class: "time" }, `${t.stops.length} paradas`),
      el("h3", {}, t.title),
      el("div", { class: "sub" }, "Tocá para empezar"),
    );
    grid.append(card);
    i++;
  }
  root.append(grid);

  // Mapa
  const map = L.map("map").setView(city.center, city.zoom);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19, attribution: "© OpenStreetMap",
  }).addTo(map);
  const group = L.featureGroup().addTo(map);
  for (const t of city.tours) {
    const m = L.marker(t.coord).bindPopup(`<strong>${escapeHtml(t.title)}</strong><br><a href="#/tour/${cityId}/${t.id}">Abrir tour</a>`);
    m.on("click", () => m.openPopup());
    group.addLayer(m);
  }
  if (group.getLayers().length) map.fitBounds(group.getBounds().pad(0.15));
}

function viewTour(cityId, tourId) {
  const city = DATA.cities[cityId];
  const tour = city && city.tours.find(t => t.id === tourId);
  if (!tour) { location.hash = "#/ciudad/" + cityId; return; }
  $("#title").textContent = tour.title;
  $("#back").hidden = false;
  $("#appbar").classList.remove("on-dark");
  $("#back").onclick = () => (location.hash = "#/ciudad/" + cityId);
  const root = $("#root");
  root.innerHTML = "";
  QUEUE = tour.stops.map(s => ({ ...s, cityId, tourId }));

  const header = el("div", { class: "tour-header" });
  if (tour.map_url) {
    header.append(
      el("a", { class: "map-btn", href: tour.map_url, target: "_blank", rel: "noopener" },
        el("span", { class: "map-ico" }, "🗺"),
        el("span", {}, "Ver mapa oficial del tour"),
        el("span", { class: "map-ext" }, "↗"),
      ),
    );
  }
  const dirUrl = `https://github.com/Nara00/claude-cloud-projects/tree/audioguias-rick-steves/webapp/audio/${cityId}/${tourId}`;
  header.append(
    el("a", { class: "zip-btn", href: `https://download-directory.github.io/?url=${encodeURIComponent(dirUrl)}`,
      target: "_blank", rel: "noopener" },
      el("span", { class: "map-ico" }, "⬇"),
      el("span", {}, "Descargar MP3 del tour como ZIP"),
      el("span", { class: "map-ext" }, "↗"),
    ),
  );
  root.append(header);

  for (const s of tour.stops) {
    const dot = el("span", { class: "cache-dot", title: "..." }, "·");
    const audioUrl = AUDIO_PATH(cityId, tourId, s.n, s.name);
    const stopEl = el("div", { class: "stop", id: `stop-${s.n}` },
      el("header", {},
        el("span", { class: "n" }, String(s.n).padStart(2, "0")),
        el("div", { class: "meta" },
          el("div", { class: "title" }, s.name),
          el("div", { class: "sub" }, dot, " ", el("span", { class: "sub-text" }, "cargando estado…")),
        ),
        el("a", { class: "dl-btn", href: audioUrl, download: `${String(s.n).padStart(2,"0")} - ${safeFilename(s.name)}.mp3`,
          "aria-label": "Descargar MP3", title: "Descargar MP3",
          onclick: ev => ev.stopPropagation() }, "⬇"),
        el("button", { class: "play-btn", "aria-label": "Reproducir",
          onclick: ev => { ev.stopPropagation(); play(cityId, tourId, s.n); } }, "▶"),
      ),
      el("div", { class: "text" }, s.text),
    );
    stopEl.querySelector("header").addEventListener("click", (ev) => {
      if (ev.target.closest(".play-btn")) return;
      stopEl.classList.toggle("open");
    });
    root.append(stopEl);
    stopIsCached(cityId, tourId, s.n, s.name).then(ok => {
      dot.textContent = ok ? "●" : "○";
      dot.className = "cache-dot " + (ok ? "ok" : "miss");
      dot.title = ok ? "Descargado, funciona sin internet" : "No descargado";
      stopEl.querySelector(".sub-text").textContent = ok ? "Sin internet ✓" : "Requiere internet";
    });
  }
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// -------- Reproductor --------
function play(cityId, tourId, n) {
  const city = DATA.cities[cityId];
  const tour = city.tours.find(t => t.id === tourId);
  const stop = tour.stops.find(s => s.n === n);
  if (!stop) return;
  PLAYING = { cityId, tourId, stopN: n };
  QUEUE = tour.stops;
  AUDIO.src = AUDIO_PATH(cityId, tourId, n, stop.name);
  AUDIO.play().catch(e => console.warn("play fail:", e));
  $("#player").hidden = false;
  $("#np-title").textContent = `${String(n).padStart(2, "0")} · ${stop.name}`;
  $("#np-sub").textContent = `${tour.title} · ${city.name}`;
  $("#np-play").textContent = "⏸";
  document.querySelectorAll(".stop.playing").forEach(e => e.classList.remove("playing"));
  const cur = document.getElementById(`stop-${n}`);
  if (cur) cur.classList.add("playing");
  updateMediaSession(city, tour, stop);
}

function updateMediaSession(city, tour, stop) {
  if ("mediaSession" in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: `${String(stop.n).padStart(2, "0")} · ${stop.name}`,
      artist: tour.title, album: city.name,
    });
    navigator.mediaSession.setActionHandler("previoustrack", prev);
    navigator.mediaSession.setActionHandler("nexttrack", next);
    navigator.mediaSession.setActionHandler("play", togglePlay);
    navigator.mediaSession.setActionHandler("pause", togglePlay);
    try {
      navigator.mediaSession.setActionHandler("seekbackward", (d) => { AUDIO.currentTime = Math.max(0, AUDIO.currentTime - (d?.seekOffset || 5)); });
      navigator.mediaSession.setActionHandler("seekforward",  (d) => { AUDIO.currentTime = Math.min(AUDIO.duration || 0, AUDIO.currentTime + (d?.seekOffset || 5)); });
    } catch (e) {}
  }
}

function togglePlay() {
  if (!AUDIO.src) return;
  if (AUDIO.paused) { AUDIO.play(); $("#np-play").textContent = "⏸"; }
  else { AUDIO.pause(); $("#np-play").textContent = "▶"; }
}

function prev() {
  if (!PLAYING) return;
  const idx = QUEUE.findIndex(s => s.n === PLAYING.stopN);
  if (idx > 0) play(PLAYING.cityId, PLAYING.tourId, QUEUE[idx - 1].n);
}

function next() {
  if (!PLAYING) return;
  const idx = QUEUE.findIndex(s => s.n === PLAYING.stopN);
  if (idx >= 0 && idx + 1 < QUEUE.length) play(PLAYING.cityId, PLAYING.tourId, QUEUE[idx + 1].n);
}

const RATES = [1, 1.25, 1.5, 2, 0.75];
let RATE_IDX = Number(localStorage.getItem("rate_idx") || 0);
AUDIO.playbackRate = RATES[RATE_IDX];
$("#np-rate").textContent = RATES[RATE_IDX] + "×";
$("#np-rate").classList.toggle("active", RATES[RATE_IDX] !== 1);

function fmt(t) {
  if (!isFinite(t)) return "0:00";
  const m = Math.floor(t / 60), s = Math.floor(t % 60);
  return m + ":" + String(s).padStart(2, "0");
}

AUDIO.addEventListener("ended", next);
AUDIO.addEventListener("timeupdate", () => {
  if (!AUDIO.duration) return;
  $("#np-seek").value = (AUDIO.currentTime / AUDIO.duration) * 100;
  $("#np-cur").textContent = fmt(AUDIO.currentTime);
});
AUDIO.addEventListener("loadedmetadata", () => {
  $("#np-dur").textContent = fmt(AUDIO.duration);
});
$("#np-seek").addEventListener("input", () => {
  if (AUDIO.duration) AUDIO.currentTime = (Number($("#np-seek").value) / 100) * AUDIO.duration;
});
$("#np-play").addEventListener("click", togglePlay);
$("#np-prev").addEventListener("click", prev);
$("#np-next").addEventListener("click", next);
$("#np-back").addEventListener("click", () => { AUDIO.currentTime = Math.max(0, AUDIO.currentTime - 5); });
$("#np-fwd").addEventListener("click", () => { AUDIO.currentTime = Math.min(AUDIO.duration || 0, AUDIO.currentTime + 5); });
$("#np-rate").addEventListener("click", () => {
  RATE_IDX = (RATE_IDX + 1) % RATES.length;
  AUDIO.playbackRate = RATES[RATE_IDX];
  $("#np-rate").textContent = RATES[RATE_IDX] + "×";
  $("#np-rate").classList.toggle("active", RATES[RATE_IDX] !== 1);
  localStorage.setItem("rate_idx", RATE_IDX);
});
// Teclado (iPad / escritorio)
document.addEventListener("keydown", (e) => {
  if (e.target.matches("input,textarea")) return;
  if (e.code === "Space") { e.preventDefault(); togglePlay(); }
  else if (e.code === "ArrowLeft") { AUDIO.currentTime = Math.max(0, AUDIO.currentTime - 5); }
  else if (e.code === "ArrowRight") { AUDIO.currentTime = Math.min(AUDIO.duration || 0, AUDIO.currentTime + 5); }
});

// -------- Router --------
function route() {
  const h = location.hash.replace(/^#\/?/, "");
  if (!h) return viewCities();
  const parts = h.split("/");
  if (parts[0] === "ciudad" && parts[1]) return viewCity(parts[1]);
  if (parts[0] === "tour" && parts[1] && parts[2]) return viewTour(parts[1], parts[2]);
  viewCities();
}
window.addEventListener("hashchange", route);

// -------- Init --------
(async () => {
  await registerSW();
  const r = await fetch(DATA_URL);
  DATA = await r.json();
  route();
})();
