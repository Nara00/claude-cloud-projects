"""Sintetiza texto con Gemini TTS (API de Gemini) y lo guarda como MP3.
Uso como módulo: synth(text, out_mp3, model, voice, style)."""
import base64, json, os, subprocess, time, urllib.error, urllib.request

STYLE = ("Leé el siguiente texto como un guía turístico cálido y cercano que acompaña a una pareja mayor "
         "en un paseo. Español latinoamericano neutro, ritmo pausado y natural, con entonación expresiva "
         "pero sin exagerar. Leé solo el texto, sin agregar nada")


def synth(text, out_mp3, model, voice="Charon", style=STYLE, retries=5):
    body = {"contents": [{"parts": [{"text": f"{style}:\n\n{text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
           f"?key={os.environ['GEMINI_API_KEY']}")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=600))
            part = r["candidates"][0]["content"]["parts"][0]["inlineData"]
            pcm = base64.b64decode(part["data"])
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "-",
                            "-b:a", "64k", out_mp3], input=pcm, check=True)
            return r.get("usageMetadata", {})
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code in (429, 500, 503) and attempt < retries - 1:
                time.sleep(10 * (attempt + 1)); continue
            raise RuntimeError(f"{e.code}: {msg}")
        except (KeyError, IndexError) as e:
            if attempt < retries - 1:
                time.sleep(5); continue
            raise RuntimeError(f"respuesta sin audio: {json.dumps(r)[:300]}")
