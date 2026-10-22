"""Re-verifica con beam 5 paradas ya generadas y actualiza su informe. Uso: reverificar.py BASE tour n1 [n2 ...]"""
import difflib, json, os, re, subprocess, sys, unicodedata
import numpy as np
from faster_whisper import WhisperModel

BASE, TOUR, NUMS = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
STOP_RE = re.compile(r"^## (\d+) · (.+?) \{en=\d+:\d+\}\s*$")


def words(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return re.findall(r"[a-z0-9ñ]+", "".join(c for c in text if not unicodedata.combining(c)))


stops, cur = {}, None
for line in open(f"{BASE}/traducciones/{TOUR}.md", encoding="utf-8"):
    if m := STOP_RE.match(line.rstrip("\n")):
        cur = int(m[1]); stops[cur] = [m[2].strip(), ""]
    elif cur:
        stops[cur][1] += line
rep_path = f"{BASE}/verificacion/{TOUR}.json"
rep = json.load(open(rep_path))
model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
for n in NUMS:
    name, text = stops[n]
    entry = next(s for s in rep["stops"] if s["n"] == n)
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{BASE}/salida/{TOUR}/{entry['file']}", "-f", "s16le",
                          "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
    segs, _ = model.transcribe(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768, language="es", beam_size=5)
    ws, wh = words(f"Parada {n}. {name}.\n\n{text.strip()}"), words(" ".join(s.text for s in segs))
    sm = difflib.SequenceMatcher(None, ws, wh, autojunk=False)
    entry["audio_match"] = round(sm.ratio(), 3)
    entry["diffs"] = [f"{' '.join(ws[a:b])} -> {' '.join(wh[c:d])}" for op, a, b, c, d in sm.get_opcodes() if op != "equal"]
    print(TOUR, n, entry["audio_match"]); [print("   ", d) for d in entry["diffs"][:15]]
json.dump(rep, open(rep_path, "w"), ensure_ascii=False, indent=1)
