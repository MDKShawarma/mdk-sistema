# -*- coding: utf-8 -*-
"""
Puente de impresion MDK
Recibe pedidos de la tablet por HTTP y los manda a la impresora por USB.

Uso:
    python puente_impresion.py

Queda escuchando en http://0.0.0.0:5001/imprimir
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import win32print
import threading

# ==========================================
# CONFIGURACION
# ==========================================
NOMBRE_IMPRESORA = "XP-80 (copy 1)"   # Tal cual aparece en Windows
PUERTO = 5001                          # Puerto donde escucha

# ==========================================
# FUNCION DE IMPRESION
# ==========================================
def imprimir_texto(texto):
    """Recibe un string y lo manda a la impresora en modo RAW (ESC/POS)"""
    data = texto.encode('cp437', errors='replace')

    handle = win32print.OpenPrinter(NOMBRE_IMPRESORA)
    try:
        job = win32print.StartDocPrinter(handle, 1, ("Comanda MDK", None, "RAW"))
        try:
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, data)
            win32print.EndPagePrinter(handle)
        finally:
            win32print.EndDocPrinter(handle)
    finally:
        win32print.ClosePrinter(handle)

# ==========================================
# SERVIDOR HTTP
# ==========================================
class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path != '/imprimir':
            self.send_response(404)
            self.end_headers()
            return

        try:
            largo = int(self.headers.get('Content-Length', 0))
            cuerpo = self.rfile.read(largo).decode('utf-8', errors='replace')

            print(f"[{threading.current_thread().name}] Recibido ticket ({len(cuerpo)} chars)")
            imprimir_texto(cuerpo)
            print("  -> Impreso OK")

            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        except Exception as e:
            print(f"  -> ERROR: {e}")
            self.send_response(500)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(f'{{"ok": false, "error": "{e}"}}'.encode())

    def do_GET(self):
        # Para chequear desde el navegador que el puente esta vivo
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Puente MDK activo')

    def log_message(self, formato, *args):
        # Silenciar logs por defecto (usamos nuestros propios prints)
        return

# ==========================================
# INICIO
# ==========================================
if __name__ == '__main__':
    print("=" * 50)
    print("PUENTE DE IMPRESION MDK")
    print("=" * 50)
    print(f"Impresora: {NOMBRE_IMPRESORA}")
    print(f"Puerto:    {PUERTO}")
    print()
    print("Esperando pedidos de la tablet...")
    print("Para frenar: Ctrl + C")
    print("=" * 50)

    servidor = HTTPServer(('0.0.0.0', PUERTO), Handler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando puente...")
        servidor.shutdown()