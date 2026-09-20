# 🏆 JTE Trivia

Juego de preguntas y respuestas en español para terminal, con modo **online** en red local, récords personales y clasificación tipo Elo.

## Características

- **120 preguntas** repartidas en 6 categorías y 20 preguntas personalizadas.
- **Registro de jugadores con contraseña** (hash SHA-256), sin dependencias externas: solo stdlib de Python 3.
- **Ranking Elo**: rating inicial 1200, con rangos 👑 Maestro, 💎 Diamante, 🥇 Oro, 🥈 Plata y 🥉 Bronce, además de rachas 🔥.
- **Mejores de la semana / mes / año**.
- **Modo servidor central**: varias máquinas comparten nombres, récords y tablas a través de la red local; si no hay servidor, todo funciona en modo local automáticamente.

## Instalación

El proyecto es 100% portable: solo usa la biblioteca estándar de Python 3, no instala dependencias, y funciona en cualquier distro de Linux (Debian/Ubuntu, Fedora, Arch, openSUSE, Alpine, ...).

### Opción rápida — instalador

Detecta tu distro, instala `python3` si falta, copia los archivos a `~/juegos` y deja el comando `trivia` listo:

```bash
git clone https://github.com/juliantellesalejandro-collab/jte-trivia.git
cd jte-trivia
./instalar.sh
```

Al terminar, abre una terminal nueva y escribe `trivia`.

### Opción manual — según distro

```bash
# Debian / Ubuntu / Mint
sudo apt-get install -y python3
cd jte-trivia
python3 trivia.py

# Fedora / RHEL / Rocky
sudo dnf install -y python3
cd jte-trivia
python3 trivia.py

# Arch / Manjaro
sudo pacman -S python
cd jte-trivia
python3 trivia.py

# openSUSE
sudo zypper install python3
cd jte-trivia
python3 trivia.py

# Alpine
sudo apk add python3
cd jte-trivia
python3 trivia.py
```

### Sin git (solo descargar el zip)

```bash
curl -L -o jte-trivia.zip https://github.com/juliantellesalejandro-collab/jte-trivia/archive/refs/heads/main.zip
unzip jte-trivia.zip && cd jte-trivia-main
python3 trivia.py
```

## Modo online (opcional)

1. Elige una máquina de tu red como **servidor** y ejecuta:

   ```bash
   python3 servidor.py
   ```

2. En las demás máquinas, indica dónde está el servidor:

   ```bash
   export TRIVIA_SERVIDOR="http://IP_DEL_SERVIDOR:8090"
   python3 trivia.py
   ```

   También puedes guardar la URL en `servidor_config.txt` (junto a `trivia.py`) y así no hay que exportar la variable en cada sesión.

Si el servidor no responde en ~3 segundos, el juego pasa a modo local sin romper la partida.

## Archivos de datos

- En modo local se guardan junto a `trivia.py`: `usuarios.json`, `rankings.json`, `resultados.json`, `.trivia_records.txt`, `.historial.json`.
- El servidor guarda su copia en `servidor_datos/`.
- Todos estos archivos y la config de red están en `.gitignore`.