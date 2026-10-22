"""Busca huecos en las transcripciones (habla que el filtro de silencios pudo descartar) y los re-transcribe sin filtro.

Uso: huecos.py BASE tour1 [tour2 ...]
Escribe BASE/transcripciones/<tour>.huecos.txt con lo recuperado (vacío si no se perdió nada).
"""
import json, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

BASE = sys.argv[1]
MIN_GAP = 6.0
model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=2)


def mmss(t):
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


for tour in sys.argv[2:]:
    segs = json.load(open(f"{BASE}/transcripciones/{tour}.json"))
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  f"{BASE}/originales/{tour}.mp3"], capture_output=True, text=True).stdout)
    bounds = [0.0] + [x for s in segs for x in (s["start"], s["end"])] + [total]
    gaps = [(bounds[i], bounds[i + 1]) for i in range(0, len(bounds), 2) if bounds[i + 1] - bounds[i] >= MIN_GAP]
    found = []
    for a, b in gaps:
        start = max(a - 0.5, 0)
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(b - start + 0.5),
                              "-i", f"{BASE}/originales/{tour}.mp3", "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                             capture_output=True, check=True).stdout
        audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
        out, _ = model.transcribe(audio, language="en", vad_filter=False, beam_size=5,
                                  condition_on_previous_text=False)
        text = " ".join(s.text.strip() for s in out if s.no_speech_prob < 0.6).strip()
        if len(text.split()) >= 3:
            found.append(f"[{mmss(a)}–{mmss(b)}] {text}")
    with open(f"{BASE}/transcripciones/{tour}.huecos.txt", "w") as f:
        f.write("\n".join(found) + ("\n" if found else ""))
    print(f"{tour}: {len(gaps)} huecos, {len(found)} con habla", flush=True)
    for line in found:
        print("   ", line[:200], flush=True)
