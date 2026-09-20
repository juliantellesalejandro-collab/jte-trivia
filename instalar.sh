#!/usr/bin/env bash
set -e

DEST="${JTE_DEST:-$HOME/juegos}"
BIN="$HOME/.local/bin"

detectar_pm() {
    if command -v apt-get >/dev/null 2>&1; then echo "apt"
    elif command -v dnf >/dev/null 2>&1; then echo "dnf"
    elif command -v pacman >/dev/null 2>&1; then echo "pacman"
    elif command -v zypper >/dev/null 2>&1; then echo "zypper"
    elif command -v apk >/dev/null 2>&1; then echo "apk"
    else echo ""; fi
}

instalar_python() {
    if command -v python3 >/dev/null 2>&1; then return; fi
    local pm; pm=$(detectar_pm)
    echo "  ⚠ No se encontró python3. Instalándolo..."
    case "$pm" in
        apt)  sudo apt-get update && sudo apt-get install -y python3 ;;
        dnf)  sudo dnf install -y python3 ;;
        pacman) sudo pacman -Sy --noconfirm python ;;
        zypper) sudo zypper -n install python3 ;;
        apk)  sudo apk add python3 ;;
        *) echo "  ❌ No sé qué gestor de paquetes usas." >&2; exit 1 ;;
    esac
}

main() {
    local pm; pm=$(detectar_pm)
    local origen
    origen=$(cd "$(dirname "$0")" && pwd)

    case "$origen" in
        $HOME/juegos|"$DEST") : ;;
        *) mkdir -p "$DEST"; cp "$origen/trivia.py" "$origen/servidor.py" "$DEST/"; echo "  📦 Copiados trivia.py y servidor.py a $DEST" ;;
    esac

    for f in "$DEST/trivia.py" "$DEST/servidor.py"; do
        [ -r "$f" ] || { echo "  ❌ No encuentro $f" >&2; exit 1; }
    done

    instalar_python

    mkdir -p "$BIN"
    printf '#!/usr/bin/env bash\nexec python3 "%s/trivia.py" "$@"\n' "$DEST" > "$BIN/trivia"
    chmod +x "$BIN/trivia" "$DEST/trivia.py" "$DEST/servidor.py"

    anadir_path() {
        local rc="$1"
        local linea="export PATH=\"$HOME/.local/bin:\$PATH\""
        [ -f "$rc" ] || touch "$rc"
        if ! grep -qF "$linea" "$rc" 2>/dev/null; then
            echo "$linea" >> "$rc"
            echo "  ➕ Añadido ~/.local/bin al PATH en $(basename "$rc")"
        fi
    }
    if command -v zsh >/dev/null 2>&1 && [ -f "$HOME/.zshrc" ]; then
        anadir_path "$HOME/.zshrc"
    fi
    if [ -n "$SHELL" ] && [[ "$(basename "$SHELL")" == bash ]]; then
        anadir_path "$HOME/.bashrc"
    elif ! command -v zsh >/dev/null 2>&1; then
        anadir_path "$HOME/.bashrc"
    fi

    echo
    echo "  ✅ Instalado. Abre una terminal nueva y escribe:"
    echo "     trivia"
    echo
    echo "  Para el servidor (modo online en tu red):"
    echo "     python3 \"$DEST/servidor.py\""
}

if [ -n "$BASH_SOURCE" ] && [ "$0" = "$BASH_SOURCE" ]; then
    main
fi