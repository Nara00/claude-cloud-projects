# Audioguías de Rick Steves en español

Traducción para uso personal (viaje familiar) de 21 audioguías gratuitas de Rick Steves: Roma (11), Florencia (5), Siena, Barcelona (2), Sevilla y Madrid. Granada no tiene tour de Rick Steves. Los oyentes son personas mayores latinoamericanas que solo hablan español.

## Estado (22 de octubre de 2026)

- `transcripciones/`: transcripción en inglés de los 21 tours (Whisper `small.en`), con `.json` (segmentos con tiempos), `.txt` y `.huecos.txt` (habla que el filtro de silencios había perdido y se recuperó).
- `traducciones/`: los 21 tours traducidos y revisados. Formato: `# Título`, luego `## NN · Parada {en=mm:ss}` (marca de tiempo del inglés donde empieza la parada). Cada tour tiene `.notas.md` con correcciones, indicaciones dudosas o corregidas y datos actualizados.
- `avisos/`: avisos prácticos por ciudad (lo que conviene confirmar antes de ir). Van al principio de cada PDF.
- `verificacion/`: informes de la versión de audio ya entregada (voz `es-ES-AlvaroNeural` de Edge TTS).
- `scripts/`: todo el proceso. `guia_traduccion.md` tiene las reglas de traducción y revisión.
- `orden.txt`: lista de los MP3 originales. Se descargan de `https://podcasts.ricksteves.com/audio-tours/<tour>.mp3`.

Ya se entregó una primera versión completa (8 ZIP, 331 paradas, 17,4 h) con la voz de Edge. A la usuaria la entonación le resultó poco natural.

## Próximo paso: regenerar el audio con Google Chirp 3 HD

- La clave de API llega como variable de entorno `GOOGLE_TTS_API_KEY`. No pedirla por el chat.
- Primero, una muestra: la misma parada (por ejemplo Panteón, parada 02) con 3 o 4 voces Chirp 3 HD, latinoamericanas (`es-US-Chirp3-HD-*`) y de España (`es-ES-Chirp3-HD-*`), para que elija. Listar las voces con `GET https://texttospeech.googleapis.com/v1/voices?languageCode=es-US&key=...`.
- Después, cambiar `tts_chunk` en `scripts/generar_audio.py` por la API REST: `POST https://texttospeech.googleapis.com/v1/text:synthesize?key=$GOOGLE_TTS_API_KEY` con `{"input":{"text":...},"voice":{"languageCode":...,"name":...},"audioConfig":{"audioEncoding":"MP3"}}`; la respuesta trae `audioContent` en base64. El límite es 5000 bytes por pedido; los párrafos entran.
- Total aproximado: 960.000 caracteres. Chirp 3 HD es gratis hasta 1 millón de caracteres por mes, y después cuesta US$ 30 por millón. Evitar regeneraciones innecesarias.
- Mantener todos los controles: síntesis por párrafo con control de palabras por minuto (detecta párrafos que la voz cortó), re-transcripción de cada parada con Whisper `small` en español y comparación con el texto (`scripts/resumen.py`, `scripts/cortes.py`, `scripts/ppm.py`). Hay que recalibrar el rango normal de palabras por minuto para la voz nueva (Álvaro: unas 155).
- Opcional, que se ofreció: una versión continua por tour, con pausas donde el original tenía música (25 tramos, unos 10 minutos en total), para que funcione como el inglés sin tocar "siguiente".

## Lecciones del proceso (para no repetir errores)

- Entorno: los scripts tienen rutas absolutas del scratchpad de la sesión anterior; hay que ajustarlas. Usar un venv con `faster-whisper` y `edge-tts` (si se sigue usando), `HF_HUB_DISABLE_XET=1` para bajar modelos de Hugging Face, y decodificar audio con ffmpeg a numpy (la versión de PyAV instalada no es compatible con `decode_audio` de faster-whisper).
- Los procesos largos van con `setsid nohup` (el límite de los comandos en segundo plano es de 2 horas). Al usar `pkill -f`, poner el patrón como `[c]ola_audio` para no matar el propio comando.
- La voz de Edge a veces cortaba párrafos en silencio: se detecta por párrafo (palabras por minuto fuera de rango) y con `cortes.py` (8 o más palabras seguidas faltantes en la re-transcripción).
- Los nombres de parada pueden tener apóstrofos (Campo de' Fiori): no usarlos en las listas de concat de ffmpeg.
- La entrega se hace con 8 ZIP por grupo o ciudad (`scripts/armar_entrega.py`, que también arma el PDF de cada ciudad con Chromium), enviados con SendUserFile. Subirlos por el conector de Google Drive no es viable por el tamaño.
