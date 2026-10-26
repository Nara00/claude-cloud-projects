#!/bin/bash
# Cola paralela: Roma primero (4 en paralelo), después Florencia (4 en paralelo).
cd /home/user/claude-cloud-projects/audioguias
source venv/bin/activate
export HF_HUB_DISABLE_XET=1
MODELO=gemini-3.1-flash-tts-preview
VOZ=Charon
ROMA="rome-pantheon rome-colosseum rome-forum rome-heart rome-jewish-ghetto rome-ostia-antica rome-sistine-chapel rome-st-peters-basilica rome-trastevere rome-vatican-museums rome-vatican-pinacoteca"
FLORENCIA="florence-accademia-david florence-bargello florence-renaissance-walk florence-san-marco-museum florence-uffizi-gallery"
PARALELO=8
export SKIP_VERIFY=1
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
export MODELO VOZ LOGS SKIP_VERIFY

echo "=== $(date -Iseconds) ROMA ($PARALELO procesos) ==="
echo "$ROMA" | tr ' ' '\n' | xargs -n1 -P $PARALELO -I {} bash -c 'procesar "$@"' _ {}
echo "=== $(date -Iseconds) FLORENCIA ($PARALELO procesos) ==="
echo "$FLORENCIA" | tr ' ' '\n' | xargs -n1 -P $PARALELO -I {} bash -c 'procesar "$@"' _ {}
echo "=== $(date -Iseconds) FIN ==="
