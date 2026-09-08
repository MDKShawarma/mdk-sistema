import subprocess

print("Generando estrategia de marketing...")
print("Esperá un momento...")
print("-" * 50)

resultado = subprocess.run(
    ['ollama', 'run', 'mistral', 'Escribí una estrategia de marketing para un negocio de shawarma. Dividila en 3 partes: WhatsApp, Instagram y YouTube. Escribí en español argentino, paso a paso.'],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    timeout=300
)

print(resultado.stdout)