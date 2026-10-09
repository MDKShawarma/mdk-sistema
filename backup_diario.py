import shutil
import os
from datetime import datetime

# Configuracion
BASE_DATOS = '/var/www/mdk-sistema/mdk.db'
CARPETA_BACKUPS = '/var/www/mdk-sistema/backups'
DIAS_RETENER = 30

# Crear carpeta si no existe
os.makedirs(CARPETA_BACKUPS, exist_ok=True)

# Generar nombre con fecha
hoy = datetime.now().strftime('%Y-%m-%d_%H%M%S')
archivo_backup = os.path.join(CARPETA_BACKUPS, f'mdk_{hoy}.db')

# Copiar la base
shutil.copy2(BASE_DATOS, archivo_backup)
print(f"BACKUP CREADO: {archivo_backup}")

# Borrar backups viejos (mas de DIAS_RETENER)
corte = datetime.now().timestamp() - (DIAS_RETENER * 86400)
borrados = 0
for archivo in os.listdir(CARPETA_BACKUPS):
    ruta = os.path.join(CARPETA_BACKUPS, archivo)
    if os.path.getmtime(ruta) < corte:
        os.remove(ruta)
        borrados += 1

print(f"Borrados {borrados} backups viejos")
print(f"Total backups actuales: {len(os.listdir(CARPETA_BACKUPS))}")