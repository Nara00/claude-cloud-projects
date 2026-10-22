"""Transcribe Rick Steves MP3s to timestamped English text. Usage: transcribir.py OUT_DIR file1.mp3 ..."""
import json, os, subprocess, sys, time
import numpy as np
from faster_whisper import WhisperModel

out_dir = sys.argv[1]
model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=2)
for path in sys.argv[2:]:
    name = os.path.splitext(os.path.basename(path))[0]
    txt_path = os.path.join(out_dir, name + ".txt")
    if os.path.exists(txt_path):
        continue
    t0 = time.time()
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = model.transcribe(audio, language="en", vad_filter=True, beam_size=5)
    segs = [{"start": round(s.start, 1), "end": round(s.end, 1), "text": s.text.strip()} for s in segs]
    with open(os.path.join(out_dir, name + ".json"), "w") as f:
        json.dump(segs, f, ensure_ascii=False, indent=1)
    with open(txt_path + ".tmp", "w") as f:
        for s in segs:
            f.write(f"[{int(s['start']//60):02d}:{int(s['start']%60):02d}] {s['text']}\n")
    os.rename(txt_path + ".tmp", txt_path)
    print(f"{name}: {len(audio)/16000/60:.1f} min in {(time.time()-t0)/60:.1f} min", flush=True)
