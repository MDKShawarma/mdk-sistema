import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Eliminar Sprite Zero de ingredientes
cursor.execute("DELETE FROM ingredientes WHERE nombre = 'SPRITE ZERO'")

# Eliminar Sprite Zero de productos
cursor.execute("DELETE FROM productos WHERE nombre = 'SPRITE ZERO'")

# Actualizar Sprite en ingredientes (sumar stock de zero)
cursor.execute("SELECT stock_actual FROM ingredientes WHERE nombre = 'SPRITE'")
sprite = cursor.fetchone()
if sprite:
    nuevo_stock = sprite[0] + 6  # sumar los 6 de Sprite Zero
    cursor.execute("UPDATE ingredientes SET stock_actual = ? WHERE nombre = 'SPRITE'", (nuevo_stock,))

conn.commit()
conn.close()

print("Sprite unificado correctamente")
print(f"Stock total de Sprite: {nuevo_stock}")