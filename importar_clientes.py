import json
import sqlite3
import re

def normalizar_telefono(tel):
    if not tel:
        return ""
    tel = str(tel)
    tel = re.sub(r'[^\d]', '', tel)
    if tel.startswith('549') and len(tel) > 10:
        tel = tel[3:]
    elif tel.startswith('54') and len(tel) > 10:
        tel = tel[2:]
    elif tel.startswith('9') and len(tel) > 10:
        tel = tel[1:]
    return tel

with open('clientes_importar.json', 'r', encoding='utf-8') as f:
    clientes = json.load(f)

print("JSON cargado:", len(clientes), "clientes")

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

cursor.execute("SELECT telefono FROM clientes")
telefonos_existentes = set()
for row in cursor.fetchall():
    tel_norm = normalizar_telefono(row[0])
    if tel_norm:
        telefonos_existentes.add(tel_norm)

print("Clientes actuales en BD:", len(telefonos_existentes))

importados = 0
omitidos = 0

for c in clientes:
    nombre = c.get('nombre', 'Cliente MDK').strip()
    telefono = str(c.get('telefono', '')).strip()
    if not telefono:
        continue
    tel_norm = normalizar_telefono(telefono)
    if tel_norm in telefonos_existentes:
        omitidos += 1
    else:
        cursor.execute(
            "INSERT INTO clientes (nombre, telefono, total_compras, cantidad_pedidos, puntos) VALUES (?, ?, 0, 0, 0)",
            (nombre, telefono)
        )
        telefonos_existentes.add(tel_norm)
        importados += 1

conn.commit()
conn.close()

print("")
print("IMPORTACION FINALIZADA")
print("Nuevos clientes agregados:", importados)
print("Clientes omitidos (ya existian):", omitidos)
print("Total en BD ahora:", len(telefonos_existentes))