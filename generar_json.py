import csv
import json

def es_cliente(nombre):
    n = nombre.lower()
    return 'cliente' in n or 'clienta' in n

clientes = []

with open('contacts 2026-2.csv', 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        parts = [
            (row.get('First Name') or '').strip(),
            (row.get('Middle Name') or '').strip(),
            (row.get('Last Name') or '').strip(),
        ]
        nombre = ' '.join(p for p in parts if p)

        if not nombre or not es_cliente(nombre):
            continue

        tel = ''
        for campo in ['Phone 1 - Value', 'Phone 2 - Value', 'Phone 3 - Value']:
            v = (row.get(campo) or '').strip()
            if v:
                if ':::' in v:
                    v = v.split(':::')[0].strip()
                tel = v
                break

        if not tel:
            continue

        clientes.append({'nombre': nombre, 'telefono': tel})

with open('clientes_importar.json', 'w', encoding='utf-8') as f:
    json.dump(clientes, f, ensure_ascii=False, indent=2)

print(f"Total clientes generados: {len(clientes)}")
print("Archivo: clientes_importar.json")