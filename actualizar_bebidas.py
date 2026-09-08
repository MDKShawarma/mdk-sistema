import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# 1. Actualizar nombres en ingredientes para que coincidan con productos
cursor.execute("UPDATE ingredientes SET nombre = 'COCAS' WHERE nombre = 'Coca Cola'")
cursor.execute("UPDATE ingredientes SET nombre = 'AGUAS' WHERE nombre = 'Agua con gas' OR nombre = 'Agua sin gas'")
cursor.execute("UPDATE ingredientes SET nombre = 'Smudis' WHERE nombre LIKE 'Smudis%'")

# 2. Eliminar Smudis divididos si existen
cursor.execute("DELETE FROM ingredientes WHERE nombre LIKE 'Smudis%'")

# 3. Agregar Sprite, Sprite Zero y Fanta al stock
nuevos = [
    ("SPRITE", "bebidas", 4, "unidades", 3),
    ("SPRITE ZERO", "bebidas", 6, "unidades", 3),
    ("FANTA", "bebidas", 9, "unidades", 3),
]

for item in nuevos:
    cursor.execute("SELECT id FROM ingredientes WHERE nombre = ?", (item[0],))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO ingredientes (nombre, categoria, stock_actual, unidad, stock_minimo) VALUES (?, ?, ?, ?, ?)",
            item
        )

# 4. Verificar si los productos existen en la tabla productos (ventas)
# Si no existen, los agregamos
productos_ventas = [
    ("SPRITE", "Bebidas", 4000, 4),
    ("SPRITE ZERO", "Bebidas", 4000, 6),
    ("FANTA", "Bebidas", 4000, 9),
]

for prod in productos_ventas:
    cursor.execute("SELECT id FROM productos WHERE nombre = ?", (prod[0],))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            prod
        )

conn.commit()
conn.close()

print("Cambios realizados correctamente")
print("- Nombres actualizados en stock")
print("- Sprite, Sprite Zero y Fanta agregados")
print("- Smudis unificados")