"""Transcribe MP3s al inglés con Gemini (Vertex AI), en tramos de 10 min en paralelo.
Uso: transcribir_gemini.py OUT_DIR file1.mp3 ...  -> OUT_DIR/<tour>.json y .txt (mismo formato que transcribir.py)."""
import base64, json, os, subprocess, sys, tempfile, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

MODEL = os.environ.get("TRANSCRIBE_MODEL", "gemini-2.5-flash")
TRAMO = 600
URL = (f"https://aiplatform.googleapis.com/v1/publishers/google/models/{MODEL}:generateContent"
       f"?key={os.environ['GOOGLE_VERTEX_API_KEY']}")
PROMPT = ("Transcribe this English audio verbatim (an audio tour). Return ONLY a JSON array of segments, "
          "each {\"start\": seconds, \"end\": seconds, \"text\": \"...\"}, one or two sentences per segment, "
          "timestamps in seconds relative to the start of this clip. Include every spoken word, including "
          "street and place names as heard. Skip music and silence. Do not summarize.")


def duracion(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout)


def transcribir_tramo(path, inicio, tmpdir):
    clip = os.path.join(tmpdir, f"{os.path.basename(path)}.{int(inicio)}.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(inicio), "-t", str(TRAMO), "-i", path,
                    "-ac", "1", "-ar", "16000", "-b:a", "32k", clip], check=True)
    data = base64.b64encode(open(clip, "rb").read()).decode()
    body = {"contents": [{"role": "user", "parts": [{"inlineData": {"mimeType": "audio/mpeg", "data": data}},
                                                    {"text": PROMPT}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    for intento in range(6):
        try:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=600))
            segs = json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
            return [{"start": round(inicio + float(s["start"]), 1), "end": round(inicio + float(s["end"]), 1),
                     "text": s["text"].strip()} for s in segs if s.get("text", "").strip()]
        except (urllib.error.URLError, OSError, KeyError, IndexError, ValueError) as e:
            msg = e.read().decode()[:200] if isinstance(e, urllib.error.HTTPError) else repr(e)[:200]
            print(f"  reintento {os.path.basename(path)} @{int(inicio)}s: {msg}", flush=True)
            time.sleep(5 * (intento + 1))
    raise RuntimeError(f"falló {path} @{inicio}")


def main():
    out_dir = sys.argv[1]
    with tempfile.TemporaryDirectory() as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        trabajos = {}
        for path in sys.argv[2:]:
            dur = duracion(path)
            trabajos[path] = [pool.submit(transcribir_tramo, path, t, tmp) for t in range(0, int(dur) + 1, TRAMO)]
        for path, futs in trabajos.items():
            name = os.path.splitext(os.path.basename(path))[0]
            segs = [s for f in futs for s in f.result()]
            json.dump(segs, open(os.path.join(out_dir, name + ".json"), "w"), ensure_ascii=False, indent=1)
            with open(os.path.join(out_dir, name + ".txt"), "w") as f:
                for s in segs:
                    f.write(f"[{int(s['start'] // 60):02d}:{int(s['start'] % 60):02d}] {s['text']}\n")
            print(f"{name}: {len(segs)} segmentos, {segs[-1]['end'] / 60:.1f} min", flush=True)


main()
