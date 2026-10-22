"""Palabras por minuto de cada parada generada (detecta texto que la voz se salteó). Uso: ppm.py BASE tour..."""
import json, re, subprocess, sys
STOP_RE = re.compile(r"^## (\d+) · (.+?) \{en=\d+:\d+\}\s*$", re.M)
B = sys.argv[1]
for t in sys.argv[2:]:
    r = json.load(open(f"{B}/verificacion/{t}.json"))
    parts = STOP_RE.split(open(f"{B}/traducciones/{t}.md").read())[1:]
    texts = {int(parts[i]): (parts[i + 1], parts[i + 2]) for i in range(0, len(parts), 3)}
    bad = []
    for s in r["stops"]:
        name, txt = texts[s["n"]]
        n = len(re.findall(r"\w+", f"Parada {s['n']}. {name}. {txt}"))
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  f"{B}/salida/{t}/{s['file']}"], capture_output=True, text=True).stdout)
        if not 130 <= n / (d / 60) <= 175:
            bad.append((s["n"], round(n / (d / 60))))
    print(t, "ppm OK" if not bad else f"ppm fuera de rango: {bad}")
