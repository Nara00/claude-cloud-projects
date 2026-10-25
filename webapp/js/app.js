// Audioguías PWA. Rutas por hash. Descarga por ciudad.
const DATA_URL = "data/tours.json";
const AUDIO_PATH = (city, tour, n, name) => `audio/${city}/${tour}/${String(n).padStart(2,"0")} - ${name}.mp3`;

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
  let done = 0, failed = 0;
  for (const u of urls) {
    try {
      const match = await cache.match(u);
      if (!match) {
        const res = await fetch(u, { cache: "no-cache" });
        if (res.ok) await cache.put(u, res.clone());
        else failed++;
      }
    } catch (e) { failed++; }
    done++;
    onProgress({ done, total: urls.length, failed });
  }
  return { done, total: urls.length, failed };
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
    el("div", { class: "dot d2" }),
    el("div", { class: "dot d3" }),
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

    const refresh = async () => {
      const { done, total } = await cityStatus(cid);
      if (total === 0) { status.textContent = "sin tours"; dl.disabled = true; rm.disabled = true; return; }
      if (done === 0) { status.textContent = `0 / ${total}`; status.className = "status"; rm.disabled = true; }
      else if (done < total) { status.textContent = `${done} / ${total} descargados`; status.className = "status err"; rm.disabled = false; }
      else { status.textContent = `${total} / ${total} ✓ sin internet`; status.className = "status ok"; rm.disabled = false; }
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

  for (const s of tour.stops) {
    const audioUrl = AUDIO_PATH(cityId, tourId, s.n, s.name);
    const stopEl = el("div", { class: "stop", id: `stop-${s.n}` },
      el("header", {},
        el("span", { class: "n" }, String(s.n).padStart(2, "0")),
        el("div", { class: "meta" },
          el("div", { class: "title" }, s.name),
          el("div", { class: "sub" }, "Tocá para leer · ▶ para escuchar"),
        ),
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

AUDIO.addEventListener("ended", next);
AUDIO.addEventListener("timeupdate", () => {
  if (!AUDIO.duration) return;
  $("#np-seek").value = (AUDIO.currentTime / AUDIO.duration) * 100;
});
$("#np-seek").addEventListener("input", () => {
  if (AUDIO.duration) AUDIO.currentTime = (Number($("#np-seek").value) / 100) * AUDIO.duration;
});
$("#np-play").addEventListener("click", togglePlay);
$("#np-prev").addEventListener("click", prev);
$("#np-next").addEventListener("click", next);

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
