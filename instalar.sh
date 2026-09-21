#!/usr/bin/env bash
set -e

REPO="juliantellesalejandro-collab/trivia-para-jugar-en-la-terminal"
URL_TARBALL="https://github.com/$REPO/archive/refs/heads/main.tar.gz"
DEST="${JTE_DEST:-$HOME/juegos}"
BIN="$HOME/.local/bin"

detectar_pm() {
    if command -v brew >/dev/null 2>&1; then echo "brew"
    elif command -v apt-get >/dev/null 2>&1; then echo "apt"
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
        brew)   brew install python ;;
        apt)    sudo apt-get update && sudo apt-get install -y python3 ;;
        dnf)    sudo dnf install -y python3 ;;
        pacman) sudo pacman -Sy --noconfirm python ;;
        zypper) sudo zypper -n install python3 ;;
        apk)    sudo apk add python3 ;;
        *)
            echo "  ❌ No sé qué gestor de paquetes usas." >&2
            echo "     Instala Python 3 de https://www.python.org/downloads/ y vuelve a ejecutar." >&2
            exit 1 ;;
    esac
}

obtener_origen() {
    local local_origen
    local_origen="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
    if [ -r "$local_origen/trivia.py" ]; then
        printf '%s' "$local_origen"
        return 0
    fi

    echo "  ⬇ Descargando Trivia desde GitHub..." >&2
    command -v curl >/dev/null 2>&1 || { echo "  ❌ Necesitas 'curl' para descargar." >&2; exit 1; }
    local tmp; tmp="$(mktemp -d)"
    trap 'rm -rf "$tmp"' EXIT
    curl -fsSL "$URL_TARBALL" -o "$tmp/trivia.tar.gz" || {
        echo "  ❌ No pude descargar. ¿Tienes conexión a internet?" >&2
        exit 1
    }
    tar -xzf "$tmp/trivia.tar.gz" -C "$tmp"
    printf '%s' "$tmp/trivia-para-jugar-en-la-terminal-main"
}

main() {
    local pm; pm=$(detectar_pm)
    local origen; origen=$(obtener_origen)

    mkdir -p "$DEST"
    cp "$origen/trivia.py" "$origen/servidor.py" "$DEST/"

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
    elif [ -f "$HOME/.bash_profile" ]; then
        anadir_path "$HOME/.bash_profile"
    elif [ -f "$HOME/.bashrc" ]; then
        anadir_path "$HOME/.bashrc"
    else
        case "$(basename "${SHELL:-bash}")" in
            bash) anadir_path "$HOME/.bashrc" ;;
            zsh)  anadir_path "$HOME/.zshrc" ;;
            *)    anadir_path "$HOME/.bashrc" ;;
        esac
    fi

    echo
    echo "  ✅ Trivia instalado en $DEST"
    echo
    echo "  Abre una terminal nueva y escribe:"
    echo "     trivia"
    echo
    echo "  Para el servidor (modo online en tu red):"
    echo "     python3 \"$DEST/servidor.py\""
}

main "$@"