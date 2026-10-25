#!/bin/bash
# Arma el bundle final de la PWA (webapp/ + audio/<ciudad>/) listo para
# subir a tiiny.host o cualquier host estático.
#
# Uso: armar_bundle.sh OUT_ZIP
set -euo pipefail

ROOT=/home/user/claude-cloud-projects
WEBAPP="$ROOT/webapp"
AUDIO_SRC="$ROOT/audioguias/salida_gemini"
OUT="${1:-/tmp/audioguias.zip}"

STAGE=$(mktemp -d)
echo "Stage: $STAGE"
cp -r "$WEBAPP/." "$STAGE/"
rm -rf "$STAGE/build"  # no empaquetamos los scripts de build
mkdir -p "$STAGE/audio"

# Mapa de tour → ciudad
declare -A CITY=(
  [rome-pantheon]=rome [rome-colosseum]=rome [rome-forum]=rome [rome-heart]=rome
  [rome-jewish-ghetto]=rome [rome-ostia-antica]=rome [rome-sistine-chapel]=rome
  [rome-st-peters-basilica]=rome [rome-trastevere]=rome [rome-vatican-museums]=rome
  [rome-vatican-pinacoteca]=rome
  [florence-accademia-david]=florence [florence-bargello]=florence
  [florence-renaissance-walk]=florence [florence-san-marco-museum]=florence
  [florence-uffizi-gallery]=florence
)

for tour in "${!CITY[@]}"; do
  src="$AUDIO_SRC/$tour"
  city="${CITY[$tour]}"
  dst="$STAGE/audio/$city/$tour"
  if [ -d "$src" ]; then
    mkdir -p "$dst"
    cp "$src"/*.mp3 "$dst/" 2>/dev/null || echo "  (vacío) $tour"
  else
    echo "  (sin audio) $tour"
  fi
done

# robots.txt para evitar indexación
cat > "$STAGE/robots.txt" <<'EOF'
User-agent: *
Disallow: /
EOF

cd "$STAGE"
rm -f "$OUT"
zip -qr "$OUT" .
du -sh "$OUT"
rm -rf "$STAGE"
echo "OK: $OUT"
