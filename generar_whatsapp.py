import subprocess

print("Generando contenido para WhatsApp...")
print("Espera un momento...")
print("-" * 50)

resultado = subprocess.run(
    ['ollama', 'run', 'mistral', 'Escribi 10 mensajes para WhatsApp para un negocio de shawarma. Cada mensaje debe tener: saludo, oferta o promocion, y despedida. Escribi en espanol argentino, breve y directo.'],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    timeout=300
)

print(resultado.stdout)