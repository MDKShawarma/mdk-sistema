import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Eliminar duplicados de AGUAS (dejar uno solo)
cursor.execute("DELETE FROM ingredientes WHERE nombre = 'AGUAS' AND id NOT IN (SELECT MIN(id) FROM ingredientes WHERE nombre = 'AGUAS')")

# Eliminar Fanta duplicado (dejar el que está en mayúsculas)
cursor.execute("DELETE FROM ingredientes WHERE nombre = 'Fanta'")

# Eliminar Sprite duplicado (dejar el que está en mayúsculas)
cursor.execute("DELETE FROM ingredientes WHERE nombre = 'Sprite'")

# Eliminar Sprite Zero (ya lo unificamos)
cursor.execute("DELETE FROM ingredientes WHERE nombre = 'Sprite Zero'")

# Eliminar Sprite Zero de productos
cursor.execute("DELETE FROM productos WHERE nombre = 'SPRITE ZERO'")

# Sumar stock de Sprite Zero al Sprite principal
cursor.execute("SELECT stock_actual FROM ingredientes WHERE nombre = 'SPRITE'")
sprite = cursor.fetchone()
if sprite:
    cursor.execute("UPDATE ingredientes SET stock_actual = ? WHERE nombre = 'SPRITE'", (sprite[0] + 6,))

conn.commit()
conn.close()

print("Stock arreglado correctamente")
print("- AGUAS sin duplicados")
print("- FANTA sin duplicados")
print("- SPRITE unificado")