import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Eliminar TODAS las bebidas
cursor.execute("DELETE FROM ingredientes WHERE categoria = 'bebidas'")

# Crear bebidas ordenadas por categoría
bebidas = [
    # AGUAS
    ("AGUA - Con gas", "AGUAS", 8, "unidades", 5),
    ("AGUA - Sin gas", "AGUAS", 8, "unidades", 5),
    
    # GASEOSAS
    ("GASEOSA - Coca Cola", "GASEOSAS", 16, "unidades", 5),
    ("GASEOSA - Coca Zero", "GASEOSAS", 13, "unidades", 5),
    ("GASEOSA - Sprite", "GASEOSAS", 4, "unidades", 3),
    ("GASEOSA - Sprite Zero", "GASEOSAS", 6, "unidades", 3),
    ("GASEOSA - Fanta", "GASEOSAS", 9, "unidades", 3),
    
    # JUGOS
    ("JUGO - Smudis Multifruta", "JUGOS", 7, "unidades", 3),
    ("JUGO - Smudis Pomelo", "JUGOS", 7, "unidades", 3),
    ("JUGO - Smudis Manzana", "JUGOS", 7, "unidades", 3),
    ("JUGO - Smudis Naranja", "JUGOS", 6, "unidades", 3),
    
    # CERVEZAS
    ("CERVEZA - Artesanal Pampa", "CERVEZAS", 5, "unidades", 3),
    ("CERVEZA - Andes IPA", "CERVEZAS", 8, "unidades", 3),
    ("CERVEZA - Andes Roja", "CERVEZAS", 5, "unidades", 3),
    ("CERVEZA - Michelob lata", "CERVEZAS", 1, "unidades", 0),
    ("CERVEZA - Corona", "CERVEZAS", 3, "unidades", 0),
    
    # VINOS
    ("VINO - Partridge", "VINOS", 1, "unidades", 0),
    ("VINO - Killka", "VINOS", 2, "unidades", 0),
    
    # TRAGOS
    ("TRAGO - Gancia lata", "TRAGOS", 1, "unidades", 0),
    ("TRAGO - Fernet lata", "TRAGOS", 1, "unidades", 0),
    ("TRAGO - Gin Tonic", "TRAGOS", 3, "unidades", 0),
    ("TRAGO - Spritz", "TRAGOS", 3, "unidades", 0),
    ("TRAGO - Rose", "TRAGOS", 1, "unidades", 0),
    ("TRAGO - Baileys", "TRAGOS", 11, "unidades", 2),
]

for bebida in bebidas:
    cursor.execute(
        "INSERT INTO ingredientes (nombre, categoria, stock_actual, unidad, stock_minimo) VALUES (?, ?, ?, ?, ?)",
        bebida
    )

conn.commit()
conn.close()

print("Bebidas organizadas por categoría")
print(f"Total: {len(bebidas)} productos")