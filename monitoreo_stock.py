import sqlite3
import pywhatkit
import time
from datetime import datetime

def revisar_stock():
    conn = sqlite3.connect('mdk.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT nombre, stock_actual, stock_minimo
        FROM ingredientes
        WHERE stock_actual <= stock_minimo
        AND stock_minimo > 0
    """)
    
    productos_bajos = cursor.fetchall()
    
    if not productos_bajos:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] OK - Stock bien")
        conn.close()
        return
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Productos con stock bajo:")
    
    mensajes_por_proveedor = {}
    
    for producto in productos_bajos:
        nombre = producto[0]
        stock = producto[1]
        minimo = producto[2]
        
        print(f"  - {nombre}: {stock} (minimo: {minimo})")
        
        if any(x in nombre.lower() for x in ['pan', 'kebbe', 'postre', 'pasta', 'garam', 'aceite']):
            proveedor = "Sergio"
        else:
            proveedor = "Ezequiel"
        
        if proveedor not in mensajes_por_proveedor:
            mensajes_por_proveedor[proveedor] = []
        
        nombre_limpio = nombre.replace('Bola de lomo', 'Carne (Bola de lomo)')
        mensajes_por_proveedor[proveedor].append(f"* {nombre_limpio}")
    
    for proveedor_nombre, productos in mensajes_por_proveedor.items():
        cursor.execute("SELECT telefono FROM proveedores WHERE nombre = ?", (proveedor_nombre,))
        proveedor = cursor.fetchone()
        
        if not proveedor:
            continue
        
        telefono = proveedor[0]
        if not telefono.startswith('+'):
            telefono = '+54' + telefono
        
        lista_productos = "\n".join(productos)
        mensaje = f"*PEDIDO AUTOMATICO - MDK SHAWARMA*\n\nHola {proveedor_nombre}, hace falta:\n\n{lista_productos}\n\n¿Podes conseguirlo?\n\nGracias,\nSistema MDK"
        
        print(f"\nEnviando a {proveedor_nombre} ({telefono})...")
        print(mensaje)
        
        try:
            pywhatkit.sendwhatmsg_instantly(
                phone_no=telefono,
                message=mensaje,
                wait_time=30,
                tab_close=False,
                close_time=2
            )
            print(f"OK - Enviado a {proveedor_nombre}")
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
    
    conn.close()

if __name__ == '__main__':
    revisar_stock()