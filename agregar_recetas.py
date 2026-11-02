import os
import glob

archivos = glob.glob('templates/*.html')
modificados = 0

for archivo in archivos:
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Si tiene el menú de dueño y no tiene el link de recetas
    if '<a href="/marketing">📣 Marketing IA</a>' in contenido and '<a href="/recetas">📝 Recetas</a>' not in contenido:
        
        # Agregamos el link de recetas justo antes del de Marketing
        nuevo_contenido = contenido.replace(
            '<a href="/marketing">📣 Marketing IA</a>',
            '<a href="/recetas">📝 Recetas</a>\n        <a href="/marketing">📣 Marketing IA</a>'
        )
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print(f"✅ Recetas agregado a: {archivo}")
        modificados += 1

if modificados == 0:
    print("No se encontraron archivos para modificar.")
else:
    print(f"\n¡Listo! Se modificaron {modificados} archivos.")