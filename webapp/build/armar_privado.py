"""Arma los tours privados (sacados del libro, contenido pago) CIFRADOS para la app.

Nada de esto se publica en claro: el repositorio y GitHub Pages son públicos.

Entrada (carpeta audioguias/privado/, ignorada por git):
  .clave                      contraseña de la familia (o variable PRIVADO_CLAVE)
  tours_privados.json         ciudades y tours privados (ver formato abajo)
  traducciones/<tour>.md      mismo formato que los tours públicos
  salida_gemini/<tour>/NN - Nombre.mp3   audio generado con generar_audio_gemini.py
  mapas/<archivo>.png         mapas del libro

Salida (se publica, todo cifrado con AES-GCM):
  webapp/privado/meta.json            sal + verificador de la contraseña (no revela nada)
  webapp/privado/datos.bin            ciudades, tours, paradas y textos
  webapp/privado/audio/<ciudad>/*.bin audio de cada parada (nombres opacos)
  webapp/privado/mapas/*.bin          mapas
  audioguias/privado_cifrado/*.bin    copia cifrada de las fuentes, para no perderlas
                                      (se recuperan con restaurar_privado.py)

Formato de tours_privados.json:
  {"cities": {"barcelona": {"name": "Barcelona", "country": "España", "center": [41.38, 2.17], "zoom": 14,
     "tours": [{"id": "bcn-libro-barri-gotic", "title": "...", "coord": [41.38, 2.17],
                "maps": [{"file": "mapas/bcn-gotic.png", "label": "Ver mapa del libro"}],
                "points": [...mismo formato que TOUR_POINTS...]}]}}}

Uso: python webapp/build/armar_privado.py
"""
import base64, hashlib, hmac, json, os, re, sys

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

sys.path.insert(0, os.path.dirname(__file__))
from armar_datos import parse_md  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FUENTE = os.path.join(RAIZ, "audioguias", "privado")
RESPALDO = os.path.join(RAIZ, "audioguias", "privado_cifrado")
SALIDA = os.path.join(RAIZ, "webapp", "privado")
ITER = 250_000
VERIF = b"audioguias-familia-ok"


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "", name).strip()


def leer_clave():
    if os.environ.get("PRIVADO_CLAVE"):
        return os.environ["PRIVADO_CLAVE"]
    p = os.path.join(FUENTE, ".clave")
    if not os.path.exists(p):
        sys.exit(f"Falta la contraseña: creá {p} o definí PRIVADO_CLAVE")
    return open(p).read().strip()


class Cifrador:
    def __init__(self, clave, sal):
        self.key = PBKDF2HMAC(hashes.SHA256(), 32, sal, ITER).derive(clave.encode())
        self.aes = AESGCM(self.key)

    def _mac(self, *partes):
        return hmac.new(self.key, b"|".join(partes), hashlib.sha256).digest()

    def nombre(self, etiqueta):
        """Nombre de archivo opaco y estable para una etiqueta (p. ej. 'tour/03')."""
        return self._mac(b"nombre", etiqueta.encode()).hex()[:24]

    def cifrar(self, datos, etiqueta):
        # IV derivado del contenido: el mismo archivo da los mismos bytes (sin cambios en git
        # ni re-descargas); solo coincide si el contenido es idéntico.
        iv = self._mac(b"iv", etiqueta.encode(), hashlib.sha256(datos).digest())[:12]
        return iv + self.aes.encrypt(iv, datos, None)

    def descifrar(self, blob):
        return self.aes.decrypt(blob[:12], blob[12:], None)


def escribir_si_cambia(path, datos):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and open(path, "rb").read() == datos:
        return False
    open(path, "wb").write(datos)
    return True


def cargar_meta(clave):
    p = os.path.join(SALIDA, "meta.json")
    if os.path.exists(p):
        meta = json.load(open(p))
        c = Cifrador(clave, base64.b64decode(meta["salt"]))
        try:
            assert c.descifrar(base64.b64decode(meta["verif"])) == VERIF
        except Exception:
            sys.exit("La contraseña no coincide con la de webapp/privado/meta.json. "
                     "Para cambiarla, borrá webapp/privado/ y audioguias/privado_cifrado/ y volvé a armar.")
        return c, meta
    sal = os.urandom(16)
    c = Cifrador(clave, sal)
    iv = os.urandom(12)
    meta = {"v": 1, "kdf": "PBKDF2-SHA256", "iter": ITER, "salt": base64.b64encode(sal).decode(),
            "verif": base64.b64encode(iv + c.aes.encrypt(iv, VERIF, None)).decode()}
    os.makedirs(SALIDA, exist_ok=True)
    json.dump(meta, open(p, "w"), indent=1)
    return c, meta


def main():
    clave = leer_clave()
    c, _ = cargar_meta(clave)
    cfg_path = os.path.join(FUENTE, "tours_privados.json")
    cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {"cities": {}}
    usados, datos, respaldo = set(), {"cities": {}}, {}

    for cid, city in cfg["cities"].items():
        tours = []
        for t in city.get("tours", []):
            md = os.path.join(FUENTE, "traducciones", t["id"] + ".md")
            if not os.path.exists(md):
                print(f"  AVISO: falta {md}", file=sys.stderr); continue
            full_title, stops = parse_md(md)
            faltan = [s["n"] for s in stops if not os.path.exists(
                os.path.join(FUENTE, "salida_gemini", t["id"], f"{s['n']:02d} - {safe(s['name'])}.mp3"))]
            if faltan:
                print(f"  AVISO: {t['id']} sin audio en paradas {faltan}: no se publica", file=sys.stderr); continue
            paradas = []
            for s in stops:
                mp3 = os.path.join(FUENTE, "salida_gemini", t["id"], f"{s['n']:02d} - {safe(s['name'])}.mp3")
                rel = f"audio/{cid}/{c.nombre(t['id'] + '/' + str(s['n']))}.bin"
                escribir_si_cambia(os.path.join(SALIDA, rel), c.cifrar(open(mp3, "rb").read(), rel))
                usados.add(rel)
                paradas.append({"n": s["n"], "label": s.get("label"), "name": s["name"], "text": s["text"],
                                "file": "privado/" + rel})
            mapas = []
            for m in t.get("maps", []):
                rel = f"mapas/{c.nombre(t['id'] + '/mapa/' + m['file'])}.bin"
                escribir_si_cambia(os.path.join(SALIDA, rel),
                                   c.cifrar(open(os.path.join(FUENTE, m["file"]), "rb").read(), rel))
                usados.add(rel)
                mapas.append({"url": "privado/" + rel, "label": m.get("label", "Ver mapa del libro"),
                              "enc": True, "type": "image/png"})
            tours.append({"id": t["id"], "title": t["title"], "full_title": full_title, "private": True,
                          "coord": t.get("coord", city["center"]), "maps": mapas, "map_url": None,
                          "points": t.get("points"), "stops": paradas})
            for extra in (t["id"] + ".md", t["id"] + ".notas.md"):
                p = os.path.join(FUENTE, "traducciones", extra)
                if os.path.exists(p):
                    respaldo["traducciones/" + extra] = p
            print(f"  {t['id']}: {len(paradas)} paradas, {len(mapas)} mapas", file=sys.stderr)
        if tours:
            datos["cities"][cid] = {k: city[k] for k in ("name", "country", "center", "zoom")} | {"tours": tours}

    escribir_si_cambia(os.path.join(SALIDA, "datos.bin"),
                       c.cifrar(json.dumps(datos, ensure_ascii=False).encode(), "datos.bin"))
    # Borrar archivos cifrados que ya no se usan
    for sub in ("audio", "mapas"):
        for raiz, _, files in os.walk(os.path.join(SALIDA, sub)):
            for f in files:
                rel = os.path.relpath(os.path.join(raiz, f), SALIDA).replace(os.sep, "/")
                if rel not in usados:
                    os.remove(os.path.join(raiz, f))

    # Respaldo cifrado de las fuentes (el contenedor es efímero)
    if os.path.exists(cfg_path):
        respaldo["tours_privados.json"] = cfg_path
    for sub in ("mapas",):
        d = os.path.join(FUENTE, sub)
        for f in (sorted(os.listdir(d)) if os.path.isdir(d) else []):
            respaldo[f"{sub}/{f}"] = os.path.join(d, f)
    indice = {}
    for rel, path in respaldo.items():
        nombre = c.nombre("respaldo/" + rel) + ".bin"
        escribir_si_cambia(os.path.join(RESPALDO, nombre), c.cifrar(open(path, "rb").read(), "respaldo/" + rel))
        indice[nombre] = rel
    escribir_si_cambia(os.path.join(RESPALDO, "indice.bin"),
                       c.cifrar(json.dumps(indice, ensure_ascii=False).encode(), "respaldo/indice"))
    n_tours = sum(len(x["tours"]) for x in datos["cities"].values())
    print(f"Listo: {n_tours} tours privados cifrados en {SALIDA}", file=sys.stderr)


if __name__ == "__main__":
    main()
