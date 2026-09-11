import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Eliminar los Smudis viejos
cursor.execute("DELETE FROM ingredientes WHERE nombre LIKE 'JUGO - Smudis%'")

# Cargar los nuevos Smudis
smudis = [
    ("JUGO - Smudis Pomelo", "JUGOS", 7, "unidades", 3),
    ("JUGO - Smudis Manzana", "JUGOS", 7, "unidades", 3),
    ("JUGO - Smudis Multifruta", "JUGOS", 7, "unidades", 3),
    ("JUGO - Smudis Naranja/Frutilla", "JUGOS", 6, "unidades", 3),
]

for jugo in smudis:
    cursor.execute(
        "INSERT INTO ingredientes (nombre, categoria, stock_actual, unidad, stock_minimo) VALUES (?, ?, ?, ?, ?)",
        jugo
    )

# Agregar Fernet Cola
cursor.execute("SELECT id FROM productos WHERE nombre = 'FERNET COLA'")
if not cursor.fetchone():
    cursor.execute("""
        INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo)
        VALUES (?, ?, ?, ?, ?)
    """, ("FERNET COLA", "Bebidas con alcohol", 5000, 10, 2))
    print("✅ Fernet Cola agregado como producto")
else:
    cursor.execute("UPDATE productos SET precio = 5000 WHERE nombre = 'FERNET COLA'")
    print("✅ Fernet Cola actualizado")

cursor.execute("SELECT id FROM ingredientes WHERE nombre = 'TRAGO - Fernet Cola'")
if not cursor.fetchone():
    cursor.execute("""
        INSERT INTO ingredientes (nombre, categoria, stock_actual, unidad, stock_minimo)
        VALUES (?, ?, ?, ?, ?)
    """, ("TRAGO - Fernet Cola", "TRAGOS", 0, "unidades", 0))
    print("✅ Fernet Cola agregado al stock")

conn.commit()
conn.close()

print("\n✅ Actualización completada")
print("\nSmudis actualizados:")
for s in smudis:
    print(f"  - {s[0]}")