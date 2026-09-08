import sqlite3
import os
import glob

# Buscar archivos .vcf en el escritorio y subcarpetas
escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
vcf_files = glob.glob(os.path.join(escritorio, "**", "*.vcf"), recursive=True)

if not vcf_files:
    print("No encontré archivos .vcf en el escritorio")
    print("Buscá en: " + escritorio)
    exit()

print("Archivos encontrados:")
for i, f in enumerate(vcf_files, 1):
    print(f"{i}. {f}")

# Usar el primero
archivo = vcf_files[0]
print(f"\nImportando desde: {archivo}")

# Leer el archivo
with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
    contenido = f.read()

# Dividir por contactos
contactos = contenido.split("BEGIN:VCARD")
print(f"Contactos encontrados: {len(contactos)-1}")

# Conectar a la base de datos
conn = sqlite3.connect('mdk.db')
cursor = conn.cursor()

importados = 0
omitidos = 0

for contacto in contactos:
    if "FN:" not in contacto:
        continue
    
    # Extraer nombre
    nombre = ""
    for linea in contacto.split("\n"):
        if linea.startswith("FN:"):
            nombre = linea[3:].strip()
            break
    
    # Extraer teléfono
    telefono = ""
    for linea in contacto.split("\n"):
        if linea.startswith("TEL"):
            # Limpiar el número
            tel = linea.split(":")[-1].strip()
            tel = tel.replace("+54", "").replace(" ", "").replace("-", "")
            if tel:
                telefono = tel
                break
    
    if nombre and telefono:
        # Verificar si ya existe
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

print(f"\n✅ Importación completa:")
print(f"   - Contactos importados: {importados}")
print(f"   - Contactos ya existentes: {omitidos}")