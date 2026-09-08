import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Contar total antes
cursor.execute("SELECT COUNT(*) FROM clientes")
total_antes = cursor.fetchone()[0]

# Borrar los que NO tienen "cliente" en el nombre
cursor.execute("DELETE FROM clientes WHERE nombre NOT LIKE '%liente%'")

conn.commit()

# Contar total después
cursor.execute("SELECT COUNT(*) FROM clientes")
total_despues = cursor.fetchone()[0]

conn.close()

print(f"Total antes: {total_antes}")
print(f"Total después: {total_despues}")
print(f"Borrados: {total_antes - total_despues}")