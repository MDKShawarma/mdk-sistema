# 🌯 MDK SHAWARMA - Sistema de Gestión
**Última actualización: 09/10/2026**

Sistema completo de gestión para el local: ventas, stock, clientes, pagos online,
puntos de fidelidad, informes y contabilidad. Funciona 24/7 en DonWeb.

 URL: https://sistema.mdk-shawarma.com
🔑 Login dueño: MDK2026

---

## 🏗️ ARQUITECTURA

| Capa | Detalle |
|------|---------|
| Lenguaje | Python + Flask |
| Base de datos | SQLite (mdk.db) - BLINDADA |
| Servidor | VPS DonWeb (149.50.154.101), puerto SSH 5028 |
| Carpeta servidor | /var/www/mdk-sistema |
| Servicio | systemctl restart mdk |
| Carpeta local | C:\Users\w10\Desktop\MDK_Sistema |
| Transporte | GitHub (git push / git pull) |
| HTTPS | Let's Encrypt activo |

---

## 🔄 FLUJO DE TRABAJO DIARIO (CMD + PuTTY)

1. Editar archivos en la compu (Bloc de Notas o el editor que prefieras)
2. En CMD:
   git add .
   git commit -m "descripcion del cambio"
   git push
3. En PuTTY:
   cd /var/www/mdk-sistema
   git pull
   systemctl restart mdk
4. Probar en el navegador

---

## ✅ FUNCIONES QUE YA FUNCIONAN

### Ventas y local
- Pantalla de ventas con carrito, personalización de productos (sin repollo, sin tomate, etc.)
- Descuento automático de stock al vender
- Comanda en 2 copias (COCINA + CLIENTE) con línea de corte
- Impresión desde navegador (window.print) mientras llega la impresora nueva
- Alerta sonora y visual de pedidos QR (verde = pagado, naranja = a cobrar)
- Cierre de caja obligatorio para el empleado a las 22:30

### Pagos online
- Pedidos por QR desde el celular (PWA instalable)
- Pago con MercadoPago integrado y verificado
- Registro automático del pedido al aprobarse el pago
- Etiqueta "PAGADO ONLINE" en el listado de ventas

### Clientes y fidelidad
- 534 clientes cargados (528 recuperados del JSON + nuevos)
- Alta automática de clientes por teléfono (QR y ventas)
- Historial de compras y de puntos por cliente
- Puntos: 1 punto por cada $1.000 pagados
- CANJE DE PUNTOS (instalado 08/10):
  - 100 puntos = $1.000 de descuento
  - Canje en bloques cerrados de 100 puntos
  - Sin mínimo de compra
  - El descuento nunca supera el total de la compra
  - Se registra en el historial como "resta" con el motivo del canje
  - Pendiente: prueba en vivo con una venta real

### Gestión
- Productos con precios editables y orden por importancia
- Stock de ingredientes con mínimos y alertas
- Gastos variables y gastos fijos (con edición)
- Contador: balance del mes, IVA e IIBB estimados, ventas de la semana
- Informe día a día con botón BORRAR DÍA (solo dueño, con confirmación)
- Proveedores con datos de contacto
- Chat con IA local (Ollama)

---

## 🛡️ BLINDAJE DE LA BASE DE DATOS (06/10/2026)

- init_db.py YA NO BORRA la base de datos nunca más
- Si falta una columna nueva, la agrega con ALTER TABLE y conserva todo
- Verificación: grep "os.remove" /var/www/mdk-sistema/init_db.py
  (debe mostrar NADA; si muestra algo, el blindaje se perdió)

---

## 👥 RECUPERACIÓN DE CLIENTES (06/10/2026)

- El 28/09 la base se recreó sola (antes del blindaje) y quedaron 8 clientes
- Se recuperaron 528 clientes desde clientes_importar.json
- Script importar_clientes.py normaliza teléfonos (saca +54, 9, espacios)
  para no duplicar clientes
- Total actual: 534 clientes

---

## 🖨️ IMPRESIÓN - ESTADO ACTUAL

| Etapa | Estado |
|-------|--------|
| RawBT (Android) | ABANDONADO: bloqueado por pantalla de licencia |
| Thermer | ABANDONADO: no detectaba la impresora en la tablet |
| Impresora nueva | XPrinter XP-V320N (LAN, corte automático) - COMPRADA, sin entregar |
| Plan al llegar | Servidor de impresión local en la PC del local; la tablet/envío manda el texto por HTTP y sale impreso con corte automático |
| Mientras tanto | Impresión de comanda desde el navegador (botón IMPRIMIR) |

---

## 🔑 DATOS IMPORTANTES

- SSH: root@149.50.154.101 puerto 5028 (contraseña cambiada el 06/10/2026 desde el panel de DonWeb; está anotada en la agenda de Sergio)
- Panel DonWeb: opción "Software y Accesos" para ver/cambiar la contraseña; NUNCA tocar los botones "Recrear" ni "Vaciar"
- Backup DonWeb: Premium Diario (permite restaurar el servidor completo si hace falta)
- MercadoPago: credenciales en el archivo .env del servidor (no subir a GitHub)
- clients de respaldo: clientes_importar.json (528 clientes, también en GitHub)

---

## 📁 ARCHIVOS CLAVE

| Archivo | Función |
|---------|---------|
| app.py | Todas las rutas del sistema |
| init_db.py | Crea tablas y columnas sin borrar datos (blindado) |
| importar_clientes.py | Recuperación de clientes desde JSON |
| clientes_importar.json | Respaldo de 528 clientes |
| templates/ | Pantallas HTML |
| static/ | Logo, estilos y service-worker (PWA) |

---

## 📌 PENDIENTES (PRÓXIMOS PASOS)

1. 🧪 Probar el canje de puntos con una venta real
2. 🖨️ Configurar la XPrinter XP-V320N cuando llegue (servidor de impresión local)
3. 📱 WhatsApp automático (confirmación de pedidos)
4. 🛵 Integración con PedidosYa
5. 📣 Marketing automático (redes)
6. 💾 Backup diario automático de mdk.db dentro del servidor

---

## 📅 HISTORIAL RESUMIDO

- Ago 2026: sistema base (productos, stock, ventas, gastos, contador, informes)
- Sep 2026: QR + MercadoPago, PWA, HTTPS, alertas, comandas, puntos
- 28/09/2026: incidente de base de datos recreada (se pierden clientes)
- 06/10/2026: blindaje de init_db + recuperación de 528 clientes + contraseña SSH nueva
- 08/10/2026: canje de puntos instalado
- 09/10/2026: botón borrar día en Informe