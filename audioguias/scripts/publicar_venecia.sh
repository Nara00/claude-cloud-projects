#!/bin/bash
# Publica en la webapp los tours de Venecia completos y verifica nombres contra tours.json.
cd /home/user/claude-cloud-projects
for t in "$@"; do
  mkdir -p webapp/audio/venice/$t
  cp audioguias/salida_gemini/$t/*.mp3 webapp/audio/venice/$t/
done
python3 - "$@" <<'PY'
import json, os, re, sys
d = json.load(open('webapp/data/tours.json'))
v = d['cities']; v = v['venice'] if isinstance(v, dict) else [c for c in v if c.get('id') == 'venice'][0]
safe = lambda s: re.sub(r'[\\/:*?"<>|]', '', s).strip()
for t in v['tours']:
    if t['id'] not in sys.argv[1:]: continue
    files = set(os.listdir(f"webapp/audio/venice/{t['id']}"))
    faltan = [f"{s['n']:02d} - {safe(s['name'])}.mp3" for s in t['stops']
              if f"{s['n']:02d} - {safe(s['name'])}.mp3" not in files]
    print(t['id'], len(t['stops']), 'paradas;', 'OK' if not faltan else f'FALTAN {faltan}')
PY
