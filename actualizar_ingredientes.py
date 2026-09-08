import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS ingredientes")

cursor.execute('''
    CREATE TABLE ingredientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        stock_actual REAL,
        unidad TEXT,
        stock_minimo REAL
    )
''')

ingredientes = [
    ("Bola de lomo", "carnes", 55, "kg", 3),
    ("Carne picada", "carnes", 8, "kg", 2),
    ("Garbanzos", "legumbres", 25, "kg", 5),
    ("Harina", "secos", 20, "kg", 5),
    ("Aceite freidora", "secos", 20, "litros", 5),
    ("Aceite cocina", "secos", 5, "litros", 1),
    ("Vinagre", "secos", 3, "litros", 1),
    ("Garam masala", "especias", 1, "kg", 0.2),
    ("Comino", "especias", 1, "kg", 0.2),
    ("Aji molido", "especias", 1, "kg", 0.2),
    ("Chimichurri", "especias", 1, "kg", 0.2),
    ("Sal", "especias", 2, "kg", 0.5),
    ("Queso crema", "salsa_montanesa", 6, "kg", 3),
    ("Pasta de mani", "salsa_montanesa", 20, "kg", 5),
    ("Limon", "verduras", 3, "kg", 1),
    ("Repollo", "verduras", 15, "kg", 3),
    ("Cebolla", "verduras", 20, "kg", 5),
    ("Tomate", "verduras", 15, "kg", 3),
    ("Morron", "verduras", 10, "unidades", 3),
    ("Pan pita", "panificados", 30, "bolsas", 5),
    ("Papas congeladas", "congelados", 20, "bolsas", 5),
    ("Kebbes", "congelados", 50, "unidades", 10),
    ("Postres", "postres", 5, "kg", 1),
    ("Gaseosas", "bebidas", 50, "unidades", 10),
    ("Aguas", "bebidas", 40, "unidades", 10),
    ("Cervezas", "bebidas", 30, "unidades", 10),
    ("Vinos", "bebidas", 20, "unidades", 5),
    ("Baileys", "bebidas", 10, "unidades", 3),
    ("Gin Tonic", "bebidas", 10, "unidades", 3),
]

cursor.executemany(
    "INSERT INTO ingredientes (nombre, categoria, stock_actual, unidad, stock_minimo) VALUES (?, ?, ?, ?, ?)",
    ingredientes
)

conn.commit()
print("Ingredientes actualizados correctamente")
print(f"Total ingredientes: {len(ingredientes)}")

conn.close()