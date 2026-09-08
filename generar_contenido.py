import subprocess

print("Generando contenido para Instagram...")
print("Esperá un momento...")
print("-" * 50)

resultado = subprocess.run(
    ['ollama', 'run', 'mistral', 'Escribí 10 posts para Instagram de un negocio de shawarma. Cada post debe tener: título, descripción corta y hashtags. Escribí en español argentino.'],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    timeout=300
)

print(resultado.stdout)