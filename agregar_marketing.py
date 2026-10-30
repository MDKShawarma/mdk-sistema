import os
import glob

# Buscamos todos los archivos HTML en la carpeta templates
archivos = glob.glob('templates/*.html')
modificados = 0

for archivo in archivos:
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificamos si el archivo tiene el menú de dueño (buscamos el link de Clientes)
    # y si NO tiene ya el link de Marketing
    if '<a href="/clientes">👥 Clientes</a>' in contenido and '<a href="/marketing">📣 Marketing IA</a>' not in contenido:
        
        # Reemplazamos la línea de Clientes por Clientes + Marketing
        nuevo_contenido = contenido.replace(
            '<a href="/clientes">👥 Clientes</a>',
            '<a href="/clientes">👥 Clientes</a>\n        <a href="/marketing">📣 Marketing IA</a>'
        )
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print(f"✅ Marketing agregado a: {archivo}")
        modificados += 1

if modificados == 0:
    print("No se encontraron archivos nuevos para modificar. (Ya deben tener el botón)")
else:
    print(f"\n¡Listo! Se modificaron {modificados} archivos.")