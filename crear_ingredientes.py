import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Crear tabla de ingredientes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        stock_actual REAL,
        unidad TEXT,
        stock_minimo REAL
    )
''')

# Verificar si ya hay ingredientes
cursor.execute("SELECT COUNT(*) FROM ingredientes")
if cursor.fetchone()[0] == 0:
    ingredientes = [
        # INGREDIENTES PARA COCINAR
        ("Carne de res", "carnes", 10, "kg", 3),
        ("Carne picada", "carnes", 8, "kg", 2),
        ("Garbanzos", "legumbres", 10, "kg", 3),
        ("Harina", "secos", 20, "kg", 5),
        ("Repollo", "verduras", 8, "kg", 2),
        ("Tomate", "verduras", 10, "kg", 3),
        ("Cebolla", "verduras", 8, "kg", 2),
        ("Morron", "verduras", 5, "kg", 1),
        ("Aceite", "secos", 15, "litros", 5),
        ("Especias", "secos", 3, "kg", 1),
        ("Salsa de ajo", "salsas", 5, "litros", 1),
        ("Salsa de yogur", "salsas", 5, "litros", 1),
        
        # PRODUCTOS COMPRADOS LISTOS
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
    print("Ingredientes cargados correctamente")
else:
    print("Ya existen ingredientes cargados")

conn.close()