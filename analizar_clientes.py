import csv

def es_cliente(nombre):
    n = nombre.lower()
    return 'cliente' in n or 'clienta' in n

total = 0
con_telefono = 0
clientes = []

with open('contacts 2026-2.csv', 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += 1
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
        
        if tel:
            con_telefono += 1
            clientes.append((nombre, tel))

print(f"Total filas en CSV: {total}")
print(f"Clientes con 'cliente'/'clienta' y telefono: {con_telefono}")
print()
print("Primeros 30:")
for n, t in clientes[:30]:
    print(f"  - {n} | {t}")