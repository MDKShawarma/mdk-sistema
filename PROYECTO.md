"Hola Deepy, soy Sergio de MDK Shawarma. Acá te paso mi archivo PROYECTO.md para que retomes el contexto. [Pegás el texto acá]"

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

---

## ACTUALIZACIÓN 21/10/2026

### Impresora instalada
- La XPrinter XP-V320N ya está en el negocio (conectada por USB a la compu)
- Driver instalado en Windows, aparece como "XP-80C" o "XP-80 (copy 1)"

### Puente de impresión (puente_impresion.py)
- Corre en la compu del negocio, escucha en http://192.168.100.175:5001/imprimir
- La tablet le manda el texto de la comanda por HTTP
- El puente la reenvía a la impresora por USB en modo RAW
- Loguea cada impresión y errores

### Autoarranque del puente
- IMPRIMIR_SIEMPRE.bat: loop infinito, si el puente se cae lo reinicia solo
- INICIAR_OCULTO.vbs: lanza el .bat sin mostrar la ventana de CMD
- Los dos son portables (usan %~dp0 y la ruta del script)
- Para dejarlo corriendo: doble clic en INICIAR_OCULTO.vbs

### Fix importante en app.py
- es_empleado() antes usaba request.remote_addr (siempre daba True)
- Ahora usa session.get('rol') == 'empleado' (funciona bien)

### Fix en ventas.html
- Menú condicional: dueño ve 11 items, empleado ve 5 (Ventas, Productos, Stock, Gastos, Cierre de Caja)
- Botón "Volver al Panel" ahora va a "/" (antes iba a /empleado)

### Fix en service-worker.js
- Antes cacheaba "/pedido" y rompía la navegación (al tocar "Menú Empleado" te llevaba a /pedido)
- Ahora: no cachea HTML, solo assets estáticos (/static/)
- CACHE_NAME subió a mdk-pwa-v2 (fuerza la limpieza del caché viejo)
- Estrategia: red primero para navegación, caché solo para assets

### Notas para la próxima sesión
- Probar la tablet con el menú del empleado (debería andar ahora)
- Probar un pedido real desde el QR (ver si imprime automáticamente)
- Si el navegador bloquea HTTPS→HTTP, revisar si hace falta proxy o excepción 
---

## 💡 IDEAS A FUTURO (Investigación)

### 🚁 Delivery con Drones
- **Idea:** Que el cliente pase coordenadas GPS por WhatsApp, el dron salga del techo del negocio y entregue el pedido directo.
- **Estado (Octubre 2026):** No viable en Buenos Aires.
- **Por qué:**
  - Regulación ANAC: El espacio aéreo de CABA es controlado. Prohibido volar sobre multitudes. Solo hay pruebas piloto, no uso comercial masivo.
  - Logística: El GPS del celular falla en edificios altos. Los drones actuales cargan hasta 2.5 kg (un pedido familiar de shawarma pesa más). El viento (Pampero) y los cables/árboles son un riesgo.
  - Operativa: El cliente tendría que ir a un punto abierto y seguro (plaza/estacionamiento) para recibir, no a la puerta de su casa.
- **Alternativas viables a corto plazo:**
  - Pedido con GPS: Agregar un botón en el sistema web para que el cliente capture su ubicación exacta (en vez de escribir la dirección).
  - Cajas térmicas con GPS: Ponerle un AirTag a la caja para que el cliente vea en tiempo real dónde está su moto de reparto.

### 📱 Pedido con GPS
- Implementar en el template `pedido_cliente.html` un botón de "Usar mi ubicación actual" (API de Geolocalización de HTML5) para que el empleado/repartidor vea el mapa exacto sin buscar la dirección a mano.

### 📦 Cajas térmicas con GPS
- Investigar etiquetas GPS (AirTag, Samsung SmartTag, etc.) para las cajas de delivery. Costo estimado: $20.000 ARS. Permite seguimiento en tiempo real desde el sistema.
---

## 🛠️ PLAN PARA LA SEMANA QUE VIENE (PENDIENTE)

### Configurar el puente de impresión en la compu del negocio
- **Problema:** La carpeta del proyecto no está en el Escritorio de la compu del negocio. Hay que crearla y copiar los archivos.
- **Solución segura:** Usar el asistente **Qwen** (que ya está abierto en la compu del negocio) para que nos guíe paso a paso. **No abrir DeepSeek en la compu del negocio** para evitar suspensiones de cuenta.
- **Pasos:**
  1. Crear la carpeta `MDK_Sistema` en el Escritorio de la compu del negocio.
  2. Copiar `puente_impresion.py` (ya está en el negocio, en el Escritorio).
  3. Crear `INICIAR_OCULTO.vbs` e `IMPRIMIR_SIEMPRE.bat` usando Qwen (pedirle que genere el código y guardarlo).
  4. Hacer doble clic en `INICIAR_OCULTO.vbs`.
  5. Probar en el navegador que `http://192.168.100.175:5001` diga "Puente MDK activo".
  6. Hacer una venta de prueba con "Transferencia (MercadoPago)" y ver si imprime el alias `comida.arabe.mp`.

### Prompt para Qwen (copiar y pegar allá):
> "Hola Qwen. Soy Sergio, dueño de MDK Shawarma. Necesito tu ayuda para configurar un puente de impresión local en esta computadora. Te paso los pasos que me dio mi otro asistente para que me guíes paso a paso:
> 1. Crear un archivo `INICIAR_OCULTO.vbs` con el código VBS que te paso.
> 2. Crear un archivo `IMPRIMIR_SIEMPRE.bat` con el código BAT que te paso.
> 3. Ambos archivos deben ir en la carpeta `MDK_Sistema` en el Escritorio.
> 4. Hacer doble clic en `INICIAR_OCULTO.vbs` y probar en el navegador que `http://192.168.100.175:5001` diga 'Puente MDK activo'.
> Por favor, sé muy claro porque no soy técnico." 
---

## 💡 IDEAS PARA DESPUÉS DEL ARRANQUE (Octubre 2026)

### 1. Botón "Hacer Pedido" en la web (COMPLETADO)
- Se agregó el botón en el menú de la web pública de DonWeb.
- Apunta a `https://sistema.mdk-shawarma.com/pedido`.

### 2. Pedido Programado (Para más tarde)
- **Cómo funciona:** En la pantalla de pedido por QR, si el cliente elige MercadoPago, se le muestra un campo opcional para elegir la hora de retiro.
- **Advertencia:** Debe llevar un cartel que diga: *"⚠️ IMPORTANTE: El horario solicitado es una preferencia, no una garantía. Si hay mucha demanda en ese momento, tu pedido puede demorar unos minutos más."*
- **Validación:** Solo se confirma el pedido cuando el pago de MercadoPago está aprobado.

### 3. Cálculo de Demora Automático (Inteligencia de Cola)
- **Cómo funciona:** El sistema calcula el tiempo estimado de espera basándose en:
  1. Cantidad de pedidos en cola en ese momento.
  2. Tiempo estándar de preparación por producto (dato que dará el empleado que corta y arma los shawarmas).
  3. Capacidad de la cocina.
- **Qué ve el cliente:** Al confirmar el pedido, aparece un cartel con el tiempo estimado (ej: "⏳ Demora estimada: 20 minutos").
- **Pendiente:** Preguntar al empleado cuánto tarda en armar un shawarma (en minutos) para configurar la base del cálculo.

### 4. Mapa de Calor de Delivery
- Guardar el barrio/dirección que escribe el cliente en los pedidos.
- Mostrar un gráfico de los barrios con más pedidos para optimizar zonas de delivery.

### 5. Pedido con GPS y Cajas Térmicas con GPS
- (Ya anotado en la sección de ideas a futuro).

---

## ACTUALIZACIÓN 26/10/2026

### Cálculo de demora automático (IMPLEMENTADO)
- El sistema calcula la demora estimada en base a los pedidos en cola.
- Fórmula actual: 1 pedido en cola = 7 minutos.
- Se muestra al cliente en la pantalla de confirmación: "⏳ Demora estimada: ~X minutos".
- Funciona en `/nuevo_pedido` (pedidos por QR).

### Mejora pendiente para el cálculo de demora
- **Problema:** El cálculo actual no tiene en cuenta los productos del carrito (ej: papas fritas tardan más).
- **Solución propuesta:** Sumar los tiempos de preparación de cada producto en lugar de usar un tiempo fijo por pedido.
- **Tiempos acordados con Sergio:**
  - Shawarma / Falafel / Fatay / Kebbe: 7 minutos.
  - Papas fritas / Nuggets: 6 minutos.
  - Bebidas: 0 minutos.
  - Postres: 1 minuto.
- **Ejemplo:** 1 shawarma + 1 papas = 13 minutos de demora.
- **Estado:** Pendiente de programar.

---

## ACTUALIZACIÓN 27/10/2026

### Impresión térmica (XPrinter XP-V320N)
- El ticket se imprime con el puente local (`puente_impresion.py`).
- **Letra grande:** Se implementó el modo "Doble Alto y Doble Ancho" de ESC/POS para que los clientes mayores lean fácilmente.
- **Corte automático:** Funciona perfecto. Separa la comanda de COCINA de la de CLIENTE.
- **Ancho del ticket:** Se ajustó a 24 caracteres por línea (por la letra doble) para que no se corte nada.

### Fix en guardado de notas (Personalizaciones)
- **Problema:** Las opciones ("Sin repollo", "Sin tomate", etc.) no se guardaban ni se imprimían en las ventas del local.
- **Solución:** Se modificó `app.py` (función `ventas`) para que tome `item['notas']` del carrito. Ahora las notas se guardan en la base de datos y salen en el ticket.

### Redes y conexión (IMPORTANTE)
- La compu del negocio ahora está en la red `home` (IP: `192.168.0.192`).
- Cuando vaya al negocio, la red es `Shawarma` (IP esperada: `192.168.100.175`).
- **El `ventas.html` sigue apuntando a `192.168.100.175`**. Cuando esté en el negocio, va a funcionar directo.
- **Para probar en casa:** Si se necesita probar desde la red `home`, hay que cambiar la IP en el código a `192.168.0.192` (y acordarse de volverla a cambiar al ir al negocio).

---

## ACTUALIZACIÓN 28/10/2026

### ¡IMPRESORA FUNCIONANDO AL 100% EN EL NEGOCIO! 🎉
- El ticket ahora sale perfecto: letra grande, legible y con las notas (ej: "Sin repollo") bien visibles.
- El corte automático funciona (separa la comanda de COCINA de la de CLIENTE).
- Se eliminó el botón de "imprimir pantalla" (window.print) para que nunca más salga el ticket feo con los botones del sistema.

### El gran problema de hoy: El nombre de la impresora
- Windows creó varias copias de la impresora con nombres raros (XP-80, XP-80 copy 1, etc.).
- El puente de Python estaba buscando "XP-80C", pero el nombre real que funcionaba era **"MDK Ticket"**.
- **Solución:** Se cambió el archivo `puente_impresion.py` para que busque `NOMBRE_IMPRESORA = "MDK Ticket"`.
- ⚠️ **IMPORTANTE PARA EL FUTURO:** Si alguien toca las impresoras en Windows y le cambia el nombre, el puente va a dejar de funcionar. El nombre debe ser siempre `"MDK Ticket"`.

### Estado actual del sistema
- Red del negocio: `Shawarma` (IP de la compu: `192.168.100.175`).
- Puente corriendo en la compu del negocio (ventana negra abierta).
- Sistema web apuntando a la IP correcta.
- **TODO LISTO PARA EMPEZAR A TRABAJAR DE VERDAD.**

---

## ACTUALIZACIÓN 28/10/2026 (CIERRE DE CAJA Y PEDIDOS QR)

### Cierre de Caja simplificado
- **Se quitó el horario límite de las 22:30:** Ahora la empleada puede hacer el cierre cuando terminen, sin apuros.
- **Campo de MercadoPago oculto:** La empleada ya no tiene que anotar lo que hay en MercadoPago. Solo anota el efectivo contado y el sistema hace el resto automáticamente.
- **Menú de empleado:** Se verificó que al entrar como empleado (sin contraseña), la pantalla solo muestra su menú y el formulario simplificado de cierre.

### Fix crítico en `app.py` (Pedidos por QR)
- **Problema:** En la función `nuevo_pedido`, el `conn.commit()` (que guarda los datos) estaba dentro de un bloque `if` de los puntos. Si un cliente pedía y no sumaba puntos, el pedido no se guardaba en la base de datos (aunque al cliente le aparecía confirmado).
- **Solución:** Se movió el `conn.commit()` afuera de esa condición para que **todos** los pedidos se guarden siempre.
- **Fix de indentación:** Se corrigió un error de espacios en la función `cierre_caja` que impedía que el sistema levante correctamente.