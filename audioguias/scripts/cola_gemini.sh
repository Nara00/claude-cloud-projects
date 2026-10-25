#!/bin/bash
# Cola de generación con Gemini. Procesa tour por tour; cada tour puede resumirse.
cd /home/user/claude-cloud-projects/audioguias
source venv/bin/activate
export HF_HUB_DISABLE_XET=1
MODELO=gemini-3.1-flash-tts-preview
VOZ=Charon
TOURS="rome-pantheon rome-colosseum rome-forum rome-heart rome-jewish-ghetto rome-ostia-antica rome-sistine-chapel rome-st-peters-basilica rome-trastevere rome-vatican-museums rome-vatican-pinacoteca florence-accademia-david florence-bargello florence-renaissance-walk florence-san-marco-museum florence-uffizi-gallery"
for t in $TOURS; do
  echo "=== $(date -Iseconds) $t ==="
  for i in 1 2 3 4; do
    python scripts/generar_audio_gemini.py . $MODELO $VOZ $t && break
    echo "---RELANZANDO $t (intento $i)---"
    sleep 15
  done
done
echo "=== $(date -Iseconds) FIN ==="
