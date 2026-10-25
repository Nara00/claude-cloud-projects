"""Arma webapp/data/tours.json desde audioguias/traducciones/*.md.

Lee los .md con el formato "# Título" + "## NN · Parada {en=mm:ss}" + texto.
Para cada parada, geocodifica el nombre contra Nominatim (con cache). Las paradas
no geocodificables (p. ej. 'Introducción') heredan las coordenadas de la anterior.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
TRAD = os.path.abspath(os.path.join(BASE, "audioguias", "traducciones"))
OUT = os.path.abspath(os.path.join(BASE, "webapp", "data", "tours.json"))
CACHE = os.path.abspath(os.path.join(BASE, "webapp", "build", "geo_cache.json"))
STOP_RE = re.compile(r"^## (\d+) · (.+?) \{en=(\d+):(\d+)\}\s*$")

CITIES = {
    "rome": {"name": "Roma", "country": "Italia", "nominatim_city": "Roma, Italia",
             "center": [41.9028, 12.4964], "zoom": 14,
             "tours": ["rome-pantheon", "rome-colosseum", "rome-forum", "rome-heart",
                       "rome-jewish-ghetto", "rome-ostia-antica", "rome-sistine-chapel",
                       "rome-st-peters-basilica", "rome-trastevere", "rome-vatican-museums",
                       "rome-vatican-pinacoteca"]},
    "florence": {"name": "Florencia", "country": "Italia", "nominatim_city": "Firenze, Italia",
                 "center": [43.7696, 11.2558], "zoom": 15,
                 "tours": ["florence-accademia-david", "florence-bargello",
                            "florence-renaissance-walk", "florence-san-marco-museum",
                            "florence-uffizi-gallery"]},
    "siena": {"name": "Siena", "country": "Italia", "nominatim_city": "Siena, Italia",
              "center": [43.3188, 11.3307], "zoom": 15, "tours": ["siena-city-walk"]},
    "barcelona": {"name": "Barcelona", "country": "España", "nominatim_city": "Barcelona, España",
                   "center": [41.3851, 2.1734], "zoom": 14,
                   "tours": ["barcelona-city-walk", "barcelona-eixample-walk"]},
    "madrid": {"name": "Madrid", "country": "España", "nominatim_city": "Madrid, España",
                "center": [40.4168, -3.7038], "zoom": 15, "tours": ["madrid-city-walk"]},
    "seville": {"name": "Sevilla", "country": "España", "nominatim_city": "Sevilla, España",
                 "center": [37.3886, -5.9823], "zoom": 15, "tours": ["sevilla-city-walk"]},
}

# Coordenadas aproximadas del punto de inicio de cada tour (centro del lugar).
# Las paradas internas heredan la coord del tour. Mejora futura: coord por parada.
TOUR_COORDS = {
    "rome-pantheon": [41.8986, 12.4769],
    "rome-colosseum": [41.8902, 12.4922],
    "rome-forum": [41.8925, 12.4853],
    "rome-heart": [41.9009, 12.4833],  # Piazza Venezia
    "rome-jewish-ghetto": [41.8921, 12.4777],
    "rome-ostia-antica": [41.7556, 12.2914],
    "rome-sistine-chapel": [41.9029, 12.4545],
    "rome-st-peters-basilica": [41.9022, 12.4539],
    "rome-trastevere": [41.8882, 12.4680],
    "rome-vatican-museums": [41.9064, 12.4536],
    "rome-vatican-pinacoteca": [41.9064, 12.4536],
    "florence-accademia-david": [43.7766, 11.2594],
    "florence-bargello": [43.7703, 11.2576],
    "florence-renaissance-walk": [43.7731, 11.2559],  # Piazza del Duomo
    "florence-san-marco-museum": [43.7786, 11.2585],
    "florence-uffizi-gallery": [43.7678, 11.2553],
    "siena-city-walk": [43.3188, 11.3307],
    "barcelona-city-walk": [41.3851, 2.1734],
    "barcelona-eixample-walk": [41.3917, 2.1649],
    "madrid-city-walk": [40.4168, -3.7038],
    "sevilla-city-walk": [37.3886, -5.9823],
}

TOUR_TITLES = {
    "rome-pantheon": "Panteón",
    "rome-colosseum": "Coliseo",
    "rome-forum": "Foro Romano",
    "rome-heart": "El corazón de Roma",
    "rome-jewish-ghetto": "Barrio Judío",
    "rome-ostia-antica": "Ostia Antica",
    "rome-sistine-chapel": "Capilla Sixtina",
    "rome-st-peters-basilica": "Basílica de San Pedro",
    "rome-trastevere": "Trastévere",
    "rome-vatican-museums": "Museos Vaticanos",
    "rome-vatican-pinacoteca": "Pinacoteca Vaticana",
    "florence-accademia-david": "Galería de la Accademia (David)",
    "florence-bargello": "Bargello",
    "florence-renaissance-walk": "Paseo del Renacimiento",
    "florence-san-marco-museum": "Museo de San Marcos",
    "florence-uffizi-gallery": "Galería Uffizi",
    "siena-city-walk": "Paseo por Siena",
    "barcelona-city-walk": "Paseo por Barcelona",
    "barcelona-eixample-walk": "Paseo por el Eixample",
    "madrid-city-walk": "Paseo por Madrid",
    "sevilla-city-walk": "Paseo por Sevilla",
}


def parse_md(path):
    title, stops = None, []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
        elif m := STOP_RE.match(line):
            stops.append({"n": int(m[1]), "name": m[2].strip(),
                          "en_start": int(m[3]) * 60 + int(m[4]), "text": ""})
        elif stops:
            stops[-1]["text"] += line + "\n"
    for s in stops:
        s["text"] = re.sub(r"\n{3,}", "\n\n", s["text"]).strip()
    return title, stops


def load_cache():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    return {}


def save_cache(c):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(c, open(CACHE, "w"), ensure_ascii=False, indent=1)


# Pistas: nombres de parada que no son lugares (se heredan). También traducciones.
NO_GEO_HINTS = [
    r"^introducci[oó]n", r"^bienvenid", r"^resumen", r"^fin\b",
    r"^despedida", r"^cierre", r"^pr[óo]ximo", r"salida\s+del",
    r"^conclusi[oó]n", r"^antes de empezar", r"^palabras finales",
]


def should_skip_geo(name):
    low = name.lower()
    return any(re.search(p, low) for p in NO_GEO_HINTS)


def geocode(query, cache):
    if query in cache:
        return cache[query]
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": query, "format": "json", "limit": 1, "accept-language": "es"})
    req = urllib.request.Request(url, headers={"User-Agent": "audioguias-personales/1 (noreply@anthropic.com)"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=20))
        time.sleep(1.1)  # política de Nominatim: 1 req/segundo
        if r:
            cache[query] = [float(r[0]["lat"]), float(r[0]["lon"])]
        else:
            cache[query] = None
    except Exception as e:
        print(f"  geocode ERROR '{query}': {e}", file=sys.stderr)
        cache[query] = None
    return cache[query]


def main():
    cache = load_cache()
    data = {"cities": {}, "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    for cid, city in CITIES.items():
        city_entry = {k: city[k] for k in ("name", "country", "center", "zoom")}
        city_entry["tours"] = []
        for tour in city["tours"]:
            md = os.path.join(TRAD, tour + ".md")
            if not os.path.exists(md):
                print(f"  AVISO: falta {md}", file=sys.stderr); continue
            full_title, stops = parse_md(md)
            tour_coord = TOUR_COORDS.get(tour, city["center"])
            for s in stops:
                s["coord"] = tour_coord
                s["coord_source"] = "tour"
            city_entry["tours"].append({
                "id": tour,
                "title": TOUR_TITLES.get(tour, tour),
                "full_title": full_title,
                "coord": tour_coord,
                "stops": [{"n": s["n"], "name": s["name"], "text": s["text"],
                            "en_start": s["en_start"], "coord": s["coord"]} for s in stops],
            })
            print(f"  {tour}: {len(stops)} paradas", file=sys.stderr)
        data["cities"][cid] = city_entry
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"Escrito {OUT}", file=sys.stderr)


main()
