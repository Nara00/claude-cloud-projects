#!/bin/bash
# Worker de audio. Varios pueden correr a la vez: cada tour se reserva con mkdir (atómico).
# Pendiente = está en cola_audio.txt y no en hechos_audio.txt. Para regenerar un tour, sacarlo de hechos_audio.txt.
cd /tmp/claude-0/-home-user-claude-cloud-projects/fe2a2dea-07e6-5a6d-b5f6-0accbd6a6eda/scratchpad
W=$1
while true; do
  for t in $(cat cola_audio.txt); do
    grep -qx "$t" hechos_audio.txt && continue
    mkdir "locks/$t" 2>/dev/null || continue
    echo "INICIO $t $(date +%H:%M) [$W]" >> log_audio.txt
    if HF_HUB_DISABLE_XET=1 ./venv/bin/python -I scripts/generar_audio.py /tmp/claude-0/-home-user-claude-cloud-projects/fe2a2dea-07e6-5a6d-b5f6-0accbd6a6eda/scratchpad $t >> log_audio_$W.txt 2>&1; then
      echo "$t" >> hechos_audio.txt; echo "FIN $t $(date +%H:%M) [$W]" >> log_audio.txt
    else
      echo "ERROR $t [$W]" >> log_audio.txt
    fi
    rmdir "locks/$t"
  done
  sleep 20
done
