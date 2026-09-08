import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Crear tabla de proveedores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        productos TEXT
    )
''')

# Eliminar proveedores viejos
cursor.execute("DELETE FROM proveedores")

# Cargar proveedores
proveedores = [
    ("Carnicero", "1149925802", "carne"),
    ("Ezequiel", "1166204775", "verduras,bebidas,papas,garbanzos,queso,especias,vinagre,harina,sal"),
    ("Sergio", "1170634208", "pan,kebbes,postres,pasta_mani,garam_masala,aceite_freidora"),
]

for prov in proveedores:
    cursor.execute(
        "INSERT INTO proveedores (nombre, telefono, productos) VALUES (?, ?, ?)",
        prov
    )

conn.commit()
conn.close()

print("Proveedores cargados correctamente")
print(f"Total: {len(proveedores)}")