#!/usr/bin/env python3
import hashlib
import json
import os
import sys
import threading
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "servidor_datos")
USUARIOS = os.path.join(DATOS, "usuarios.json")
RANKINGS = os.path.join(DATOS, "rankings.json")
RESULTADOS = os.path.join(DATOS, "resultados.json")

LOCKS = {"usuarios": threading.Lock(), "rankings": threading.Lock(), "resultados": threading.Lock()}


def cargar(ruta, por_defecto):
    if not os.path.exists(ruta):
        return por_defecto
    try:
        with open(ruta) as f:
            datos = json.load(f)
        return datos if isinstance(datos, type(por_defecto)) else por_defecto
    except (ValueError, OSError):
        return por_defecto


def guardar(ruta, datos):
    os.makedirs(DATOS, exist_ok=True)
    tmp = ruta + ".tmp"
    with open(tmp, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ruta)


def hash_clave(nombre, clave):
    d = hashlib.sha256()
    d.update(nombre.encode())
    d.update(b":")
    d.update(clave.encode())
    return d.hexdigest()


def registrar(nombre, clave):
    with LOCKS["usuarios"]:
        usuarios = cargar(USUARIOS, {})
        if nombre in usuarios:
            return False
        usuarios[nombre] = hash_clave(nombre, clave)
        guardar(USUARIOS, usuarios)
    return True


def login(nombre, clave):
    usuarios = cargar(USUARIOS, {})
    return usuarios.get(nombre) == hash_clave(nombre, clave)


def registrar_resultado(nombre, aciertos, total):
    with LOCKS["resultados"]:
        resultados = cargar(RESULTADOS, [])
        resultados.append({"usuario": nombre, "aciertos": aciertos, "total": total,
                           "fecha": date.today().isoformat()})
        guardar(RESULTADOS, resultados)

    with LOCKS["rankings"]:
        datos = cargar(RANKINGS, {})
        jugador = datos.get(nombre, {"rating": 1200, "partidas": 0, "racha": 0, "mejor": 0})
        pct = aciertos / total if total else 0
        delta = round(32 * (pct - 0.5) * 2)
        jugador["rating"] = max(100, jugador["rating"] + delta)
        jugador["partidas"] += 1
        jugador["mejor"] = max(jugador["mejor"], aciertos)
        if pct >= 0.5:
            jugador["racha"] += 1
        else:
            jugador["racha"] = 0
        datos[nombre] = jugador
        guardar(RANKINGS, datos)
        orden = sorted(datos.items(), key=lambda kv: kv[1]["rating"], reverse=True)
        pos = next((i for i, (n, _) in enumerate(orden, 1) if n == nombre), None)
    return {"rating": jugador["rating"], "delta": delta, "pos": pos, "racha": jugador["racha"]}


def ranking_ordenado():
    datos = cargar(RANKINGS, {})
    return sorted(datos.items(), key=lambda kv: kv[1]["rating"], reverse=True)


def mejores_periodo(dias, limite=10):
    resultados = cargar(RESULTADOS, [])
    desde = (date.today() - timedelta(days=dias)).isoformat()
    acum = {}
    for r in resultados:
        if r.get("fecha", "") < desde:
            continue
        d = acum.setdefault(r.get("usuario", ""), {"aciertos": 0, "partidas": 0})
        d["aciertos"] += r.get("aciertos", 0)
        d["partidas"] += 1
    orden = sorted(acum.items(), key=lambda kv: kv[1]["aciertos"], reverse=True)
    return [{"usuario": n, "aciertos": d["aciertos"], "partidas": d["partidas"]}
            for n, d in orden[:limite]]


class Manejador(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respuesta(self, codigo, obj):
        cuerpo = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def consultas(self):
        if "?" in self.path:
            return parse_qs(self.path.split("?", 1)[1])
        return {}

    def cuerpo(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
        except ValueError:
            n = 0
        if n <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(n))
        except ValueError:
            return {}

    def do_GET(self):
        ruta = self.path.split("?", 1)[0]
        q = self.consultas()
        if ruta == "/api/ping":
            return self.respuesta(200, {"ok": True, "juego": "jte-trivia"})
        if ruta == "/api/existe":
            nombre = q.get("nombre", [""])[0]
            return self.respuesta(200, {"existe": nombre in cargar(USUARIOS, {})})
        if ruta == "/api/jugadores":
            nombres = sorted(cargar(USUARIOS, {}).keys())
            return self.respuesta(200, {"nombres": nombres})
        if ruta == "/api/stats":
            nombre = q.get("nombre", [""])[0]
            partidas = aciertos = total = 0
            for r in cargar(RESULTADOS, []):
                if r.get("usuario") == nombre:
                    partidas += 1
                    aciertos += r.get("aciertos", 0)
                    total += r.get("total", 0)
            return self.respuesta(200, {"partidas": partidas, "aciertos": aciertos, "total": total})
        if ruta == "/api/ranking":
            return self.respuesta(200, {"ranking": ranking_ordenado()})
        if ruta == "/api/periodo":
            try:
                dias = int(q.get("dias", ["7"])[0])
            except ValueError:
                dias = 7
            return self.respuesta(200, {"tabla": mejores_periodo(dias)})
        return self.respuesta(404, {"ok": False, "error": "no encontrado"})

    def do_POST(self):
        cuerpo = self.cuerpo()
        nombre = str(cuerpo.get("nombre", ""))
        clave = str(cuerpo.get("clave", ""))
        ruta = self.path.split("?", 1)[0]

        if ruta == "/api/registrar":
            if not nombre or not clave:
                return self.respuesta(400, {"ok": False, "error": "faltan datos"})
            if not registrar(nombre, clave):
                return self.respuesta(200, {"ok": False, "error": "El nombre ya está registrado"})
            return self.respuesta(200, {"ok": True})

        if ruta == "/api/login":
            return self.respuesta(200, {"ok": login(nombre, clave)})

        if ruta == "/api/resultado":
            if not login(nombre, clave):
                return self.respuesta(200, {"ok": False, "error": "nombre o contraseña incorrectos"})
            try:
                aciertos = int(cuerpo.get("aciertos", 0))
                total = int(cuerpo.get("total", 1))
            except ValueError:
                return self.respuesta(400, {"ok": False, "error": "datos inválidos"})
            if total < 1 or aciertos < 0 or aciertos > total:
                return self.respuesta(400, {"ok": False, "error": "resultado no válido"})
            info = registrar_resultado(nombre, aciertos, total)
            return self.respuesta(200, {"ok": True, **info})

        return self.respuesta(404, {"ok": False, "error": "no encontrado"})


def main():
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    print("  ╭─────────────────────────────────╮")
    print("  │   🏆 SERVIDOR JTE TRIVIA        │")
    print("  │   Compartiendo nombres y récords │")
    print("  ╰─────────────────────────────────╯")
    print()
    print(f"  Escuchando en 0.0.0.0:{puerto} (toda la red local)")
    print(f"  Datos en: {DATOS}")
    print("  Otros jugadores deben configurar TRIVIA_SERVIDOR=http://IP_DEL_SERVIDOR:8090")
    ThreadingHTTPServer(("0.0.0.0", puerto), Manejador).serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Servidor detenido. 👋")
        sys.exit(0)