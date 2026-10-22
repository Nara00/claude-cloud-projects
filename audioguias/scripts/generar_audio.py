"""Genera el audio en español de un tour traducido y verifica el resultado.

Uso: generar_audio.py BASE tour1 [tour2 ...]
  BASE/traducciones/<tour>.md   -> BASE/salida/<tour>/NN - Parada.mp3
  BASE/transcripciones/<tour>.json (inglés, para comparar)
Escribe BASE/verificacion/<tour>.json con los chequeos por parada.
"""
import asyncio, difflib, json, os, re, shutil, subprocess, sys, unicodedata
import edge_tts
import numpy as np
from faster_whisper import WhisperModel

VOICE = "es-ES-AlvaroNeural"
BASE = sys.argv[1]
TOURS = sys.argv[2:]
STOP_RE = re.compile(r"^## (\d+) · (.+?) \{en=(\d+):(\d+)\}\s*$")


def parse(md_path):
    title, stops = None, []
    for line in open(md_path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
        elif m := STOP_RE.match(line):
            stops.append({"n": int(m[1]), "name": m[2].strip(), "en_start": int(m[3]) * 60 + int(m[4]), "text": ""})
        elif line.startswith("## "):
            raise ValueError(f"{md_path}: encabezado de parada mal formado: {line!r}")
        elif stops:
            stops[-1]["text"] += line + "\n"
    if not title or not stops:
        raise ValueError(f"{md_path}: falta título o paradas")
    for i, s in enumerate(stops, 1):
        if s["n"] != i:
            raise ValueError(f"{md_path}: numeración salteada en parada {s['n']}")
        s["text"] = re.sub(r"\n{3,}", "\n\n", s["text"]).strip()
    return title, stops


def words(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9ñ]+", text)


UNITS_RE = re.compile(r"\b\d+(\.\d+)?(-| )?(square )?(feet|foot|ft|miles?|tons?|degrees|yards?|inches|inch|pounds?|acres?|"
                      r"stories|story)\b|\b\d+(st|nd|rd|th|s)\b|\b\d+-?D\b", re.I)


def numbers(text):
    """Cifras de un texto, sin separadores de miles. Ignora medidas imperiales y ordinales (se convierten)."""
    text = re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text)
    return set(re.findall(r"\d+", UNITS_RE.sub(" ", text)))


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def load_audio(path):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768


async def tts_chunk(text, path):
    for attempt in range(5):
        try:
            await edge_tts.Communicate(text, VOICE, proxy=os.environ.get("HTTPS_PROXY")).save(path)
            return
        except Exception as e:  # el servicio corta conexiones de vez en cuando
            print(f"  reintento TTS ({e})", flush=True)
            await asyncio.sleep(2 ** attempt)
    raise RuntimeError(f"TTS falló: {path}")


async def tts(text, path):
    """Sintetiza párrafo por párrafo (los pedidos largos a veces pierden texto) y concatena."""
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts = []
    tmp = os.path.join(os.path.dirname(path), ".partes")  # nombres simples: el de la parada puede tener apóstrofos
    os.makedirs(tmp, exist_ok=True)
    for k, para in enumerate(paras):
        part = os.path.join(tmp, f"{k:03d}.mp3")
        n_words = len(re.findall(r"\w+", para))
        limit = 205 if n_words >= 40 else 225  # en párrafos cortos el ritmo varía más
        best = None
        for attempt in range(5):  # la voz a veces corta un párrafo por la mitad: se nota en que "lee" demasiado rápido
            await tts_chunk(para, part)
            wpm = n_words / (duration(part) / 60)
            if best is None or wpm < best[0]:
                best = (wpm, part + ".mejor")
                shutil.copy(part, best[1])
            if n_words < 15 or wpm <= limit:
                break
            print(f"  párrafo cortado ({n_words} palabras a {wpm:.0f} ppm), se repite", flush=True)
        else:
            print(f"  AVISO: párrafo sigue rápido tras 5 intentos ({best[0]:.0f} ppm): {para[:60]}", flush=True)
        os.replace(best[1], part)
        parts.append(part)
    lst = os.path.join(tmp, "lista.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{os.path.abspath(x)}'\n" for x in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", path + ".tmp.mp3"],
                   check=True)
    os.rename(path + ".tmp.mp3", path)
    for x in parts + [lst]:
        os.remove(x)
    os.rmdir(tmp)


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "", name).strip()


def main():
    model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    os.makedirs(os.path.join(BASE, "verificacion"), exist_ok=True)
    for tour in TOURS:
        title, stops = parse(os.path.join(BASE, "traducciones", tour + ".md"))
        en_segs = json.load(open(os.path.join(BASE, "transcripciones", tour + ".json")))
        en_total = en_segs[-1]["end"]
        out_dir = os.path.join(BASE, "salida", tour)
        os.makedirs(out_dir, exist_ok=True)
        for f in os.listdir(out_dir):  # regenerar limpio si cambiaron las paradas
            p = os.path.join(out_dir, f)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        report = {"tour": tour, "title": title, "stops": []}
        for i, s in enumerate(stops):
            en_end = stops[i + 1]["en_start"] if i + 1 < len(stops) else en_total
            en_text = " ".join(x["text"] for x in en_segs if s["en_start"] <= x["start"] < en_end)
            spoken = f"Parada {s['n']}. {s['name']}.\n\n{s['text']}"
            path = os.path.join(out_dir, f"{s['n']:02d} - {safe(s['name'])}.mp3")
            ws = words(spoken)
            for attempt in range(3):  # si el audio no coincide con el texto, se vuelve a sintetizar
                asyncio.run(tts(spoken, path))
                audio = load_audio(path)
                for beam in (1, 5):  # pasada rápida; si da baja, una más precisa para descartar errores de Whisper
                    segs, _ = model.transcribe(audio, language="es", beam_size=beam)
                    wh = words(" ".join(x.text for x in segs))
                    sm = difflib.SequenceMatcher(None, ws, wh, autojunk=False)
                    match = sm.ratio()
                    if match >= 0.95:
                        break
                wpm = len(ws) / (len(audio) / 16000 / 60)
                if match >= 0.93 and wpm <= 180:
                    break
                print(f"  {tour} {s['n']:02d}: match={match:.3f} ppm={wpm:.0f}, se regenera", flush=True)
            diffs = [f"{' '.join(ws[a:b])} -> {' '.join(wh[c:d])}" for op, a, b, c, d in sm.get_opcodes() if op != "equal"]
            es_dur = duration(path)
            en_dur = max(en_end - s["en_start"], 1)
            missing_nums = sorted(numbers(en_text) - numbers(s["text"]), key=int)
            report["stops"].append({
                "n": s["n"], "name": s["name"], "file": os.path.basename(path),
                "es_min": round(es_dur / 60, 1), "en_min": round(en_dur / 60, 1),
                "dur_ratio": round(es_dur / en_dur, 2),
                "word_ratio": round(len(words(s["text"])) / max(len(words(en_text)), 1), 2),
                "audio_match": round(match, 3), "ppm": round(wpm), "tts_attempts": attempt + 1, "missing_numbers": missing_nums, "diffs": diffs,
            })
            r = report["stops"][-1]
            print(f"{tour} {s['n']:02d} match={r['audio_match']} words={r['word_ratio']} "
                  f"dur={r['dur_ratio']} nums={missing_nums}", flush=True)
        json.dump(report, open(os.path.join(BASE, "verificacion", tour + ".json"), "w"), ensure_ascii=False, indent=1)


main()
