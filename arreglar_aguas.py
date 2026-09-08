import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Buscar todas las aguas
cursor.execute("SELECT id, nombre, stock_actual FROM ingredientes WHERE LOWER(nombre) LIKE '%agua%'")
aguas = cursor.fetchall()

print("Aguas encontradas:")
for a in aguas:
    print(f"ID: {a[0]} | Nombre: {a[1]} | Stock: {a[2]}")

conn.close()