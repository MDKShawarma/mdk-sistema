import pyautogui
import sqlite3
import time
import subprocess
import urllib.parse

def enviar_pedido_proveedor(proveedor_nombre, mensaje):
    conn = sqlite3.connect('mdk.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT nombre, telefono FROM proveedores WHERE nombre = ?", (proveedor_nombre,))
    proveedor = cursor.fetchone()
    
    if not proveedor:
        print(f"No se encontró al proveedor: {proveedor_nombre}")
        return
    
    nombre = proveedor[0]
    telefono = proveedor[1]
    
    if not telefono.startswith('+'):
        telefono = '+54' + telefono
    
    print(f"Enviando mensaje a {nombre} ({telefono})...")
    
    # Codificar mensaje
    mensaje_codificado = urllib.parse.quote(mensaje)
    
    # Crear URL
    url = f"https://web.whatsapp.com/send?phone={telefono}&text={mensaje_codificado}"
    
    # Abrir en Chrome
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.Popen([chrome_path, url])
    
    print("Esperando 20 segundos para que cargue...")
    time.sleep(20)
    
    # Presionar Enter DOS veces (por si acaso)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.press('enter')
    
    print("✅ Enter presionado - Mensaje enviado")
    print("(Verificá en WhatsApp Web si se envió)")

if __name__ == '__main__':
    mensaje = "*PRUEBA DEL SISTEMA - MDK SHAWARMA*\n\nHola Ezequiel, este es un mensaje de prueba.\n\nGracias,\nSistema MDK"
    
    enviar_pedido_proveedor("Ezequiel", mensaje)