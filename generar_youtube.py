import subprocess

print("Generando contenido para YouTube...")
print("Espera un momento...")
print("-" * 50)

resultado = subprocess.run(
    ['ollama', 'run', 'mistral', 'Escribi 5 ideas de videos para YouTube para un negocio de shawarma. Cada video debe tener: titulo, descripcion y duracion sugerida. Escribi en espanol argentino.'],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    timeout=300
)

print(resultado.stdout)