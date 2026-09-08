import sqlite3
from datetime import datetime

def simular_pedido():
    conn = sqlite3.connect('mdk.db')
    cursor = conn.cursor()
    
    # Buscar al proveedor Sergio
    cursor.execute("SELECT nombre, telefono FROM proveedores WHERE nombre = 'Sergio'")
    proveedor = cursor.fetchone()
    
    if not proveedor:
        print("No se encontró al proveedor Sergio")
        return
    
    nombre = proveedor[0]
    telefono = proveedor[1]
    
    # Crear mensaje
    mensaje = f"""
=========================================
📱 SIMULACIÓN DE ENVÍO WHATSAPP
=========================================
Para: {nombre} ({telefono})
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
-----------------------------------------
Mensaje:

*PEDIDO AUTOMÁTICO - MDK SHAWARMA*

Hola {nombre}, el sistema detectó que hace falta:

• 10 bolsas de pan

¿Podés conseguirlas?

Gracias,
Sistema MDK
=========================================
"""
    
    print(mensaje)
    print("✅ Simulación completada")
    print("(El mensaje NO fue enviado, es solo una simulación)")
    
    conn.close()

if __name__ == '__main__':
    simular_pedido()