#!/usr/bin/env bash
set -e

DEST="${1:-$HOME/Documentos}"
ORIGEN="$HOME/juegos"

mkdir -p "$DEST"
FECHA=$(date +%F)
ARCHIVO="$DEST/jte-trivia-respaldo-$FECHA.tar.gz"

tar -czf "$ARCHIVO" -C "$HOME" "$(basename "$ORIGEN")"
chmod 700 "$ARCHIVO"

cd "$DEST" || exit 1
ls -t jte-trivia-respaldo-*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm -f

echo "  ✅ Respaldo creado: $ARCHIVO"
echo "     (se conservan los últimos 7 respaldos en $DEST)"
ls -lh "$DEST" | grep jte-trivia-respaldo