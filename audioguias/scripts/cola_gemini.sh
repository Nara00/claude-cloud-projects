#!/bin/bash
# Cola paralela de generación con Gemini: 4 tours al mismo tiempo.
# Cada tour tiene resume por parada; si uno falla, se reintenta solo.
cd /home/user/claude-cloud-projects/audioguias
source venv/bin/activate
export HF_HUB_DISABLE_XET=1
MODELO=gemini-3.1-flash-tts-preview
VOZ=Charon
TOURS="rome-pantheon rome-colosseum rome-forum rome-heart rome-jewish-ghetto rome-ostia-antica rome-sistine-chapel rome-st-peters-basilica rome-trastevere rome-vatican-museums rome-vatican-pinacoteca florence-accademia-david florence-bargello florence-renaissance-walk florence-san-marco-museum florence-uffizi-gallery"
PARALELO=4
LOGS=/tmp/claude-0/-home-user-claude-cloud-projects/b4aa56bb-52a3-5976-b787-c53d98d8e7cc/scratchpad/por_tour
mkdir -p "$LOGS"

procesar() {
  local t=$1
  for i in 1 2 3 4; do
    echo "[$(date -Iseconds)] [$t] intento $i"
    python scripts/generar_audio_gemini.py . $MODELO $VOZ $t 2>&1 | tee "$LOGS/$t.log" && return 0
    sleep 15
  done
  echo "[$t] FALLÓ después de 4 intentos"
  return 1
}

export -f procesar
export MODELO VOZ LOGS

echo "=== $(date -Iseconds) INICIO cola paralela ($PARALELO procesos) ==="
echo "$TOURS" | tr ' ' '\n' | xargs -n1 -P $PARALELO -I {} bash -c 'procesar "$@"' _ {}
echo "=== $(date -Iseconds) FIN ==="
