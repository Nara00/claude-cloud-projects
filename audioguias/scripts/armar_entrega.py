"""Arma la entrega final: carpetas por ciudad con los MP3, un PDF por ciudad (avisos + textos) y ZIPs para descargar.

Uso: armar_entrega.py BASE DESTINO
"""
import os, re, shutil, subprocess, sys, tempfile, zipfile

BASE, DEST = sys.argv[1], sys.argv[2]
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
# (carpeta, archivo de avisos, [(grupo para el zip, [tours en orden sugerido])])
CITIES = [
    ("1 Roma", "roma", [
        ("Roma 1 - Paseos", ["rome-heart", "rome-pantheon", "rome-jewish-ghetto", "rome-trastevere"]),
        ("Roma 2 - Roma antigua", ["rome-colosseum", "rome-forum", "rome-ostia-antica"]),
        ("Roma 3 - Vaticano", ["rome-vatican-museums", "rome-sistine-chapel", "rome-vatican-pinacoteca",
                               "rome-st-peters-basilica"]),
    ]),
    ("2 Florencia", "florencia", [("Florencia", ["florence-renaissance-walk", "florence-accademia-david",
                                                 "florence-uffizi-gallery", "florence-bargello",
                                                 "florence-san-marco-museum"])]),
    ("3 Siena", "siena", [("Siena", ["siena-city-walk"])]),
    ("4 Barcelona", "barcelona", [("Barcelona", ["barcelona-city-walk", "barcelona-eixample-walk"])]),
    ("5 Sevilla", "sevilla", [("Sevilla", ["sevilla-city-walk"])]),
    ("6 Madrid", "madrid", [("Madrid", ["madrid-city-walk"])]),
]
CSS = """
@page { size: A4; margin: 1.6cm 1.4cm; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 13pt; line-height: 1.5; color: #222; }
h1 { font-size: 21pt; margin: 0 0 0.4em; page-break-before: always; color: #5a2d0c; }
h2 { font-size: 15pt; margin-top: 1.3em; color: #7a3b00; page-break-after: avoid; }
p { margin: 0.5em 0; }
li { margin: 0.25em 0; }
.portada { text-align: center; margin-top: 7cm; page-break-after: always; }
.portada .ciudad { font-size: 34pt; font-weight: bold; color: #5a2d0c; }
.portada .sub { font-size: 15pt; margin-top: 0.6em; }
.indice { font-size: 13pt; margin-top: 2cm; text-align: left; display: inline-block; }
.avisos h1 { page-break-before: avoid; }
"""


def title_of(tour):
    return open(os.path.join(BASE, "traducciones", tour + ".md"), encoding="utf-8").readline()[2:].strip()


def clean(name):
    return re.sub(r'[\\/:*?"<>|]', "", name).strip()


def md_to_html(md):
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html"], input=md, capture_output=True,
                          text=True, check=True).stdout


def pdf(html, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", f.name], check=True, capture_output=True)
    os.remove(f.name)


def main():
    if os.path.exists(DEST):
        shutil.rmtree(DEST)
    zips_dir = os.path.join(DEST, "_zips")
    os.makedirs(zips_dir)
    for folder, avisos_name, groups in CITIES:
        n = 0  # numeración dentro de cada ciudad
        city = folder.split(" ", 1)[1]
        city_dir = os.path.join(DEST, folder)
        os.makedirs(city_dir)
        tours = [t for _, ts in groups for t in ts]
        texts, index, dirs = [], [], {}
        for t in tours:
            n += 1
            title = title_of(t)
            index.append(f"{n}. {title}")
            md = open(os.path.join(BASE, "traducciones", t + ".md"), encoding="utf-8").read()
            md = re.sub(r" \{en=\d+:\d+\}", "", md)
            texts.append(re.sub(r"^# (.+)$", lambda m: f"# {n}. {m[1]}", md, count=1, flags=re.M))
            src = os.path.join(BASE, "salida", t)
            files = sorted(f for f in os.listdir(src) if f.endswith(".mp3"))
            assert files, f"sin audio: {t}"
            dirs[t] = clean(f"{n:02d} {title}")
            shutil.copytree(src, os.path.join(city_dir, dirs[t]),
                            ignore=lambda d, names: [x for x in names if not x.endswith(".mp3")])
        avisos_md = open(os.path.join(BASE, "avisos", avisos_name + ".md"), encoding="utf-8").read()
        html = (f"<!doctype html><html lang='es'><meta charset='utf-8'><style>{CSS}</style>"
                f"<div class='portada'><div class='ciudad'>{city}</div>"
                f"<div class='sub'>Audioguías de Rick Steves en español</div>"
                f"<div class='indice'>{'<br>'.join(index)}</div></div>"
                f"<div class='avisos'>{md_to_html(avisos_md)}</div>{md_to_html(chr(10).join(texts))}</html>")
        pdf_path = os.path.join(city_dir, f"{city} - avisos y textos.pdf")
        pdf(html, pdf_path)
        for gname, ts in groups:
            zpath = os.path.join(zips_dir, f"{gname}.zip")
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_STORED) as z:  # los mp3 no se comprimen más
                z.write(pdf_path, os.path.join(folder, os.path.basename(pdf_path)))
                for t in ts:
                    full = os.path.join(city_dir, dirs[t])
                    for f in sorted(os.listdir(full)):
                        z.write(os.path.join(full, f), os.path.join(folder, dirs[t], f))
            print(f"{gname}: {os.path.getsize(zpath) / 1e6:.0f} MB", flush=True)


main()
