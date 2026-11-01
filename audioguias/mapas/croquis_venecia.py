"""Genera los croquis (SVG en HTML -> PNG) de la Basílica de San Marcos y de los Frari.
Uso: python croquis_venecia.py  (escribe *.html en este directorio; el PNG se renderiza con Chromium)."""
import os

DIR = os.path.dirname(os.path.abspath(__file__))
CSS = """body{margin:0;background:#fbf7ee}svg{display:block}
.t{font-family:"DejaVu Serif",Georgia,serif;font-weight:bold;fill:#3b2a1a}
.s{font-family:"DejaVu Sans",Arial,sans-serif;fill:#3b2a1a}"""
DEFS = """<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/></marker>
<pattern id="stone" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="24" height="24" fill="#ece5d6"/>
<path d="M0,24 L24,0" stroke="#d9cfba" stroke-width="2"/></pattern></defs>"""


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.parts = w, h, []

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill="#f1e4c8", stroke="#5a4128", sw=3, rx=0, extra=""):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def circle(self, cx, cy, r, fill="none", stroke="#5a4128", sw=2, dash=""):
        d = f'stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {d}/>')

    def text(self, x, y, s, size=20, cls="s", anchor="middle", bold=False, italic=False, fill=None):
        st = (' font-weight="bold"' if bold else "") + (' font-style="italic"' if italic else "") + (f' style="fill:{fill}"' if fill else "")
        self.add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" font-size="{size}"{st}>{s}</text>')

    def num(self, cx, cy, n, r=20):
        fs = 22 if len(str(n)) == 1 else 18
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1d1d1d"/>'
                 f'<text x="{cx}" y="{cy + fs * 0.36:.0f}" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="{fs}" font-weight="bold" style="fill:#fff">{n}</text>')

    def route(self, pts, color="#c0392b"):
        d = " ".join(("M" if i == 0 else "L") + f"{x},{y}" for i, (x, y) in enumerate(pts))
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="6" stroke-dasharray="14 9" stroke-linejoin="round" marker-mid="url(#ar)" marker-end="url(#ar)"/>')

    def legend(self, y0, title, items, foot):
        self.add(f'<line x1="40" y1="{y0}" x2="1040" y2="{y0}" stroke="#5a4128" stroke-width="2"/>')
        self.text(40, y0 + 46, title, 30, "t", "start")
        y = y0 + 96
        for n, label, desc in items:
            self.num(58, y - 8, n, 18)
            self.add(f'<text x="90" y="{y}" class="s" font-size="23"><tspan font-weight="bold">{label}</tspan>'
                     + (f" {desc}" if desc else "") + "</text>")
            y += 44
        for line in foot:
            self.text(40, y + 10, line, 20, "s", "start", italic=True, fill="#6b5a44")
            y += 32
        self.h = y + 30

    def html(self, title):
        body = "\n".join(self.parts)
        return (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>'
                f'<svg width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg">'
                f'{DEFS}{body}</svg></body></html>')


def basilica():
    s = SVG(1080, 0)
    s.text(540, 60, "BASÍLICA DE SAN MARCOS", 44, "t")
    s.text(540, 100, "Planta baja: paradas 2 a 14 · Museo (piso de arriba): 15 a 20", 23)
    # Planta en cruz griega: entrada abajo (oeste), altar arriba (este)
    s.add('<g transform="translate(0,-170)">')
    C = 220
    x0, y0 = 430, 560  # cuadrado central
    arms = {"centro": (x0, y0), "este": (x0, y0 - C), "oeste": (x0, y0 + C), "norte": (x0 - C, y0), "sur": (x0 + C, y0)}
    for k, (x, y) in arms.items():
        s.rect(x, y, C, C, fill="#fbe9a6" if k == "centro" else "#f1e4c8")
        s.circle(x + C / 2, y + C / 2, 82, dash="8 6")
    s.text(540, y0 - 20, "PRESBITERIO", 18, bold=True)
    s.text(610, y0 + 2 * C - 16, "NAVE", 18, bold=True)
    s.text(320, y0 + C - 16, "TRANSEPTO NORTE", 16, bold=True)
    s.text(760, y0 + C - 16, "TRANSEPTO SUR", 16, bold=True)
    s.text(600, y0 + 135, "cúpula de la", 17)
    s.text(600, y0 + 156, "Ascensión", 17, bold=True)
    s.text(540, y0 + C + 150, "cúpula de", 16)
    s.text(540, y0 + C + 170, "Pentecostés", 16, bold=True)
    # Tesoro y Pala d'Oro
    s.rect(870, 560, 120, 110, fill="#fbe9a6")
    s.text(930, 600, "TESORO", 18, bold=True)
    s.add('<rect x="505" y="365" width="70" height="40" fill="#e6c766" stroke="#5a4128" stroke-width="2"/>')
    s.text(540, 358, "Pala d'Oro", 16, bold=True)
    s.add('<rect x="515" y="440" width="50" height="40" fill="none" stroke="#5a4128" stroke-width="2" stroke-dasharray="4 3"/>')
    s.text(600, 470, "altar", 15, anchor="start")
    # Atrio y fachada
    s.rect(230, 1000, 620, 100, fill="url(#stone)", stroke="#8a7a60")
    s.text(360, 1058, "ATRIO", 22, "t")
    s.add('<rect x="700" y="1030" width="120" height="40" rx="6" fill="#fff" stroke="#5a4128" stroke-width="2"/>')
    s.text(760, 1057, "↑ escalera", 16, bold=True)
    s.text(760, 1124, "al museo", 15)
    s.add('<path d="M540,1180 L540,1108" stroke="#2e7d32" stroke-width="6" fill="none"/><path d="M528,1118 L540,1098 L552,1118 z" fill="#2e7d32"/>')
    s.text(540, 1210, "ENTRADA desde la Plaza San Marcos", 20, bold=True, fill="#2e7d32")
    s.text(990, 760, "Palacio", 17, italic=True)
    s.text(990, 782, "Ducal →", 17, italic=True)
    # Recorrido planta baja
    s.route([(540, 1170), (540, 1065), (640, 1065), (560, 1020), (540, 900), (540, 700), (720, 700),
             (760, 640), (880, 620), (700, 600), (600, 500), (560, 420), (470, 520), (360, 600), (290, 700),
             (300, 900), (660, 1050), (735, 1050)])
    s.num(500, 1150, 2)
    s.num(470, 1135, 3, 18)
    s.num(655, 1035, 4)
    s.num(500, 975, 5)
    s.num(470, 905, 6)
    s.num(470, 830, 7)
    s.num(470, 690, 8)
    s.num(470, 735, 9, 18)
    s.num(760, 795, 10)
    s.num(930, 635, 11)
    s.num(470, 455, 12)
    s.num(470, 390, 13)
    s.num(320, 585, 14)
    s.add('</g>')
    # Piso de arriba (esquema)
    y = 1100
    s.text(40, y, "PISO DE ARRIBA: MUSEO Y BALCÓN (esquema)", 26, "t", "start")
    boxes = [(40, "Entrada", "museo", 15), (230, "Mosaicos", "antiguos", 16), (420, "Sala dei", "Banchetti", 17),
             (610, "Caballos", "originales", 18), (800, "Balcón", "interior", 19)]
    for x, a, b, n in boxes:
        s.rect(x, y + 30, 170, 110, fill="#fbe9a6" if n in (17, 18) else "#f1e4c8")
        s.text(x + 85, y + 80, a, 19, bold=True)
        s.text(x + 85, y + 104, b, 18)
        s.num(x + 24, y + 54, n, 18)
    s.rect(610, y + 175, 360, 70, fill="#d8e6f0", stroke="#4a7c99")
    s.text(805, y + 218, "Loggia: vista a la plaza", 18, bold=True)
    s.num(634, y + 210, 20, 18)
    s.route([(130, y + 150), (300, y + 150), (480, y + 150), (520, y + 160), (690, y + 160), (880, y + 155), (880, y + 170)])
    s.text(500, y + 196, "(vuelvan sobre sus pasos)", 16, italic=True)
    items = [(2, "El exterior:", "mírenlo desde la plaza."), (3, "La entrada:", "la fila y las normas."),
             (4, "Atrio:", "arco del arca de Noé, a la derecha."), (5, "La nave:", "dejen que los ojos se acostumbren."),
             (6, "Cúpula de Pentecostés", ""), (7, "La cruz griega:", "caminando al centro."),
             (8, "Cúpula de la Ascensión", "(8 y 9)"), (10, "Mosaico del hallazgo de san Marcos", ""),
             (11, "El Tesoro", "(entrada aparte)"), (12, "Tumba de san Marcos", "(entrada Pala d'Oro)"),
             (13, "La Pala d'Oro", ""), (14, "La Virgen Nicopeia", ""), (15, "Museo:", "suban la escalera del atrio."),
             (17, "Sala dei Banchetti", ""), (18, "Los caballos de bronce", ""), (20, "Loggia:", "la gran vista de la plaza.")]
    s.legend(y + 290, "QUÉ HAY EN CADA NÚMERO", items,
             ["Croquis esquemático, no a escala: sigan el recorrido señalizado.",
              "Pala d'Oro, Tesoro y Museo tienen entrada aparte, que se paga adentro."])
    return s


def frari():
    s = SVG(1080, 0)
    s.text(540, 60, "IGLESIA DE LOS FRARI", 44, "t")
    s.text(540, 100, "Santa Maria Gloriosa dei Frari · paradas 3 a 11", 23)
    # Presbiterio con ábside
    s.add('<g transform="translate(0,-220)">')
    s.add('<path d="M460,560 L460,400 Q540,330 620,400 L620,560 z" fill="#fbe9a6" stroke="#5a4128" stroke-width="3"/>')
    s.text(540, 455, "altar mayor", 17, italic=True)
    # Capillas a los lados del presbiterio
    for x in (300, 380, 620, 700):
        s.rect(x, 470, 80, 90, fill="#fbe9a6" if x == 620 else "#f1e4c8")
    s.text(660, 600, "capilla", 14)
    # Transepto
    s.rect(200, 560, 680, 140, fill="#f1e4c8")
    # Sacristía y sala capitular
    s.rect(880, 540, 150, 180, fill="#fbe9a6")
    s.text(955, 580, "SACRISTÍA", 17, bold=True)
    s.rect(880, 390, 150, 150, fill="#fbe9a6")
    s.text(955, 420, "SALA", 16, bold=True)
    s.text(955, 440, "contigua", 15)
    # Nave con naves laterales
    s.rect(380, 700, 320, 620, fill="#f1e4c8")
    s.add('<line x1="460" y1="700" x2="460" y2="1320" stroke="#5a4128" stroke-width="1.5" stroke-dasharray="5 6"/>')
    s.add('<line x1="620" y1="700" x2="620" y2="1320" stroke="#5a4128" stroke-width="1.5" stroke-dasharray="5 6"/>')
    for yy in range(760, 1320, 110):
        s.circle(460, yy, 9, fill="#9c8f7a")
        s.circle(620, yy, 9, fill="#9c8f7a")
    s.rect(475, 720, 130, 200, fill="url(#stone)", stroke="#8a7a60", sw=2)
    s.text(540, 805, "coro de", 16, bold=True)
    s.text(540, 826, "los frailes", 16, bold=True)
    s.text(540, 1290, "NAVE", 20, "t")
    s.text(330, 1120, "Pirámide", 15, anchor="end")
    s.text(330, 1140, "de Canova", 15, anchor="end")
    s.text(330, 1000, "tumba Pesaro", 15, anchor="end")
    s.text(330, 1020, "(esclavos)", 15, anchor="end")
    # Entrada
    s.add('<path d="M540,1400 L540,1335" stroke="#2e7d32" stroke-width="6" fill="none"/><path d="M528,1345 L540,1325 L552,1345 z" fill="#2e7d32"/>')
    s.text(540, 1430, "ENTRADA y boletería (sigan los carteles)", 20, bold=True, fill="#2e7d32")
    s.text(540, 1460, "Campo dei Frari · a 10 min de la parada de vaporetto San Tomà", 18, italic=True)
    # Recorrido
    s.route([(540, 1320), (540, 1180), (540, 980), (540, 600), (540, 520), (600, 520), (660, 540),
             (660, 630), (900, 630), (990, 630), (955, 520), (955, 470)])
    s.route([(880, 470), (700, 650), (640, 1000), (650, 1230), (430, 1230), (420, 1100), (420, 960)], color="#d9776b")
    s.num(500, 1180, 3)
    s.num(540, 380, 4)
    s.num(595, 478, 5, 18)
    s.num(660, 505, 6)
    s.num(1000, 680, 7)
    s.num(925, 480, 8)
    s.num(675, 1255, 9)
    s.num(400, 1180, 10)
    s.num(420, 920, 11)
    s.add('</g>')
    items = [(2, "Cómo llegar y el exterior:", "Campo dei Frari."), (3, "La nave:", "luminosa y sencilla."),
             (4, "Tiziano, La Asunción", "(detrás del altar mayor)."), (5, "Tumba del dux Foscari:", "pared derecha."),
             (6, "Donatello, San Juan Bautista:", "1ª capilla a la derecha."),
             (7, "Bellini, la Virgen con santos:", "en la sacristía."),
             (8, "Paolo Veneziano:", "en la sala contigua."), (9, "Tumba de Tiziano:", "nave derecha, cerca de la entrada."),
             (10, "Monumento a Canova:", "la pirámide, enfrente."),
             (11, "Tiziano, La Virgen de Ca' Pesaro:", "nave izquierda.")]
    s.legend(1280, "QUÉ HAY EN CADA NÚMERO", items,
             ["Croquis esquemático, no a escala.", "Del 8 al 9 vuelvan hasta el fondo de la iglesia (línea más clara)."])
    return s


if __name__ == "__main__":
    for name, fn, title in (("basilica-san-marcos-croquis", basilica, "Basílica de San Marcos"),
                            ("frari-croquis", frari, "Iglesia de los Frari")):
        open(os.path.join(DIR, name + ".html"), "w").write(fn().html(title))
        print(name)
