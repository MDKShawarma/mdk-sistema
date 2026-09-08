import sqlite3

conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

# Eliminar proveedor Carnicero
cursor.execute("DELETE FROM proveedores WHERE nombre = 'Carnicero'")

# Actualizar Ezequiel con todos los productos
cursor.execute("""
    UPDATE proveedores 
    SET productos = 'carne,verduras,bebidas,papas,garbanzos,queso,especias,vinagre,harina,sal'
    WHERE nombre = 'Ezequiel'
""")

conn.commit()
conn.close()

print("Proveedores actualizados correctamente")
print("Proveedores actuales:")
print("- Ezequiel: 1166204775")
print("- Sergio: 1170634208")