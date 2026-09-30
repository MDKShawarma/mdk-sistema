import json
import sqlite3
import re

def normalizar_tel(tel):
    d = re.sub(r'\D', '', tel or '')
    if d.startswith('549'):
        d = d[3:]
    elif d.startswith('54'):
        d = d[2:]
    if d.startswith('9') and len(d) > 10:
        d = d[1:]
    return d

with open('clientes_importar.json', 'r', encoding='utf-8') as f:
    clientes = json.load(f)

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

cursor.execute("SELECT telefono FROM clientes")
existentes = set()
for (tel,) in cursor.fetchall():
    if tel:
        existentes.add(normalizar_tel(tel))

insertados = 0
duplicados = 0

for c in clientes:
    tn = normalizar_tel(c['telefono'])
    if tn and tn in existentes:
        duplicados += 1
        continue
    cursor.execute(
        "INSERT INTO clientes (nombre, telefono, total_compras, cantidad_pedidos, puntos) VALUES (?, ?, 0, 0, 0)",
        (c['nombre'], c['telefono'])
    )
    existentes.add(tn)
    insertados += 1

conn.commit()
conn.close()
print(f"Insertados: {insertados}")
print(f"Duplicados saltados: {duplicados}")