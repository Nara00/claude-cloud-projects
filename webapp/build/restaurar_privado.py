"""Recupera las fuentes de los tours privados desde la copia cifrada del repositorio.

Descifra audioguias/privado_cifrado/*.bin en audioguias/privado/ (ignorada por git).
El audio no se respalda aparte: se recupera descifrando webapp/privado/audio con --audio.
Uso: python webapp/build/restaurar_privado.py [--audio]
"""
import base64, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from armar_privado import FUENTE, RESPALDO, SALIDA, Cifrador, leer_clave, safe  # noqa: E402


def main():
    meta = json.load(open(os.path.join(SALIDA, "meta.json")))
    c = Cifrador(leer_clave(), base64.b64decode(meta["salt"]))
    indice = json.loads(c.descifrar(open(os.path.join(RESPALDO, "indice.bin"), "rb").read()))
    for nombre, rel in indice.items():
        dest = os.path.join(FUENTE, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(c.descifrar(open(os.path.join(RESPALDO, nombre), "rb").read()))
        print("  ", rel)
    if "--audio" in sys.argv:
        datos = json.loads(c.descifrar(open(os.path.join(SALIDA, "datos.bin"), "rb").read()))
        for city in datos["cities"].values():
            for t in city["tours"]:
                for s in t["stops"]:
                    src = os.path.join(SALIDA, s["file"].removeprefix("privado/"))
                    dest = os.path.join(FUENTE, "salida_gemini", t["id"], f"{s['n']:02d} - {safe(s['name'])}.mp3")
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    open(dest, "wb").write(c.descifrar(open(src, "rb").read()))
                print("   audio:", t["id"])


if __name__ == "__main__":
    main()
