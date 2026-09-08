import sqlite3
import re

# Archivo específico de contactos
archivo = r"C:\Users\w10\Desktop\PROYECTO MDK IA\contacts 2026-2.csv"

print(f"Importando desde: {archivo}")

# Leer el archivo
with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
    lineas = f.readlines()

# Conectar a la base de datos
conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

importados = 0
omitidos = 0
total_clientes = 0

for linea in lineas[1:]:  # saltar la primera línea
    if "Cliente" in linea or "cliente" in linea or "Clienta" in linea:
        total_clientes += 1
        partes = linea.split(",")
        
        # Buscar nombre (primeras columnas con texto)
        nombre = ""
        for parte in partes[:5]:
            parte = parte.strip()
            if parte and "myContacts" not in parte and "Mobile" not in parte and "Home" not in parte:
                nombre = parte
                break
        
        # Buscar teléfono
        telefono = ""
        for i, parte in enumerate(partes):
            if "Mobile" in parte or "Phone" in parte or "Móvil" in parte or "Celular" in parte:
                if i+1 < len(partes):
                    tel = partes[i+1].strip()
                    tel = re.sub(r'[^0-9+]', '', tel)
                    if tel and len(tel) > 6:
                        telefono = tel
                        break
        
        if nombre and telefono:
            cursor.execute("SELECT id FROM clientes WHERE telefono = ?", (telefono,))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                    (nombre, telefono)
                )
                importados += 1
            else:
                omitidos += 1

conn.commit()
conn.close()

print(f"\n✅ Resultado:")
print(f"   - Contactos con 'Cliente' encontrados: {total_clientes}")
print(f"   - Importados: {importados}")
print(f"   - Ya existentes: {omitidos}")