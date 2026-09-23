# PROYECTO MDK SHAWARMA - SISTEMA DE GESTION

Ultima actualizacion: 23/09/2026

## DESCRIPCION

Sistema web de gestion para MDK Shawarma (Maison du Kebab), negocio de comida arabe en Buenos Aires, Argentina.

## URLs DEL SISTEMA

- Sistema en DonWeb: https://sistema.mdk-shawarma.com
- Pedido clientes: https://sistema.mdk-shawarma.com/pedido
- Panel empleado: https://sistema.mdk-shawarma.com/empleado
- Web publica: https://mdk-shawarma.com
- GitHub: https://github.com/MDKShawarma/mdk-sistema

## SERVIDOR DONWEB

- IP: 149.50.154.101
- Host: vps-6399034-x.dattaweb.com
- Puerto SSH: 5028
- Usuario: root
- Sistema: Ubuntu 22.04
- Nodo: OS4
- Servicio systemd: mdk.service
- Nginx configurado con SSL (Let's Encrypt)

## CREDENCIALES

- Dueno (Sergio): contrasena MDK2026 - acceso TOTAL
- Empleado: sin contrasena en /empleado - Ventas, Productos, Stock, Gastos, Cierre de Caja
- Cliente: sin contrasena en /pedido - solo hacer pedidos
- MercadoPago Access Token: guardado en /var/www/mdk-sistema/.env

## FUNCIONES QUE YA FUNCIONAN

### Autenticacion y Roles
- Login de dueno con contrasena MDK2026
- Acceso de empleado sin contrasena
- Separacion de roles (dueno vs empleado)
- Empleado NO puede acceder al panel de dueno
- Logout

### Panel de Control (Dueno)
- Ventas del dia
- Pedidos del dia
- Gasto diario estimado
- Alertas de stock bajo
- Total de productos
- Total de clientes
- Alertas de ingredientes bajos

### Productos
- Listar productos (29 cargados)
- Editar precios
- Ordenados por importancia

### Stock
- Listar ingredientes (23 cargados)
- Sumar, restar, fijar stock
- Reset total
- Alertas de stock minimo

### Ventas
- Carrito de ventas
- Multiples productos por venta
- Notas por producto
- Seleccion de cliente
- Metodos de pago (efectivo, Mercadopago)
- Numero de pedido correlativo
- Descuento automatico de stock
- Etiqueta "PAGADO ONLINE" para pagos por QR con MercadoPago

### Gastos
- Registrar gastos del dia
- Categorias
- Total del dia

### Gastos Fijos
- Listar, agregar, editar, eliminar

### Contador
- Ingresos del mes y de hoy
- Gastos fijos y variables
- Balance
- IVA estimado 21%
- IIBB estimado 3.5%
- Ventas ultimos 7 dias

### Informe
- Ventas de hoy y ayer
- Gasto diario
- Historial de 14 dias
- Productos mas vendidos por dia

### Clientes
- Listar clientes
- Agregar cliente
- Ver detalle e historial
- Eliminar cliente
- Sistema de puntos (1 punto cada $1.000)

### Proveedores
- Listar (Ezequiel, Sergio)
- Agregar y eliminar

### Chat con IA
- Chat con Ollama + Mistral

### Cierre de Caja
- Boton "Cerrar Caja" en panel empleado
- Formulario de cierre (efectivo + MercadoPago)
- Calculo automatico de esperado segun ventas
- Calculo de diferencias
- Observaciones
- Historial para dueno (ultimos 30 cierres)
- Bloqueo obligatorio despues de las 22:30

### Pedidos de Clientes (QR)
- Pagina de pedidos sin login
- Menu completo con precios
- Carrito con cantidades
- Personalizacion: Shawarma/Falafel (sin repollo, tomate, cebolla, salsa), Coca (Normal/Zero), Agua (Con/Sin gas), Smudis (Naranja/Frutilla, Pomelo, Manzana, Multifruta)
- Formulario de cliente
- Tipo de servicio (local/para llevar)
- Metodo de pago: Efectivo o MercadoPago
- Notas/sugerencias
- Numero de pedido correlativo
- Aviso de demora si hay 10+ pedidos pendientes
- Registro automatico de cliente nuevo

### Pago Online con MercadoPago (NUEVO - 23/09/2026)
- Cliente elige "MercadoPago" al hacer el pedido
- Se guarda el pedido en tabla `pedidos_pendientes`
- Se crea una preferencia de pago en MercadoPago
- Se redirige al cliente a la pasarela de pago de MercadoPago
- El cliente puede pagar con tarjeta, saldo o efectivo (Rapipago/Pago Facil)
- Al confirmar el pago, MercadoPago redirige a /pago_exitoso
- El sistema verifica el pago con la API de MercadoPago
- Se registra la venta automaticamente
- Se descuenta stock
- Se suman puntos al cliente
- Se muestra el numero de pedido al cliente

### Alerta para Empleado (NUEVO - 23/09/2026)
- En la pantalla de ventas (/ventas), cada 10 segundos se consulta si hay pedidos nuevos pagados online
- Si hay, suena un "ding" y aparece un cartel verde grande con:
  - Numero de pedido
  - Productos
  - Total
- El empleado toca "OK, VISTO" para cerrarlo
- En la tabla de ventas, los pedidos pagados online aparecen con etiqueta verde "PAGADO ONLINE"

### PWA (App instalable)
- Manifest.json
- Service Worker
- Iconos 192x192 y 512x512
- Instalable desde Chrome
- Registro automatico

## FUNCIONES PENDIENTES

- Sistema de puntos (canje de puntos por descuentos)
- WhatsApp automatico
- Impresora de comandas
- Integracion con PedidosYa
- Marketing automatico (generacion de contenido con IA)
- Prediccion de demanda
- Alertas inteligentes

## ESTRUCTURA DEL PROYECTO

MDK_Sistema/
- app.py (archivo principal Flask)
- init_db.py (inicializacion de BD)
- requirements.txt
- mdk.db (base de datos SQLite)
- .env (variables de entorno - Access Token de MercadoPago)
- Procfile (configuracion de gunicorn)
- crear_iconos.py
- static/
  - logo.png
  - style.css
  - manifest.json
  - service-worker.js
  - icon-192.png
  - icon-512.png
  - QR_MDK_Pedidos.png (QR actualizado a DonWeb)
- templates/
  - login.html
  - inicio.html
  - empleado.html
  - productos.html
  - stock.html
  - ventas.html (con alerta de pedidos nuevos)
  - gastos.html
  - gastos_fijos.html
  - contador.html
  - informe.html
  - clientes.html
  - cliente_detalle.html (con puntos)
  - proveedores.html
  - chat.html
  - cierre_caja.html
  - pedido_cliente.html (con boton MercadoPago)
  - pago_exitoso.html (NUEVO)
  - pago_fallido.html (NUEVO)
  - pago_pendiente.html (NUEVO)

## BASE DE DATOS - TABLAS

- productos (29 cargados)
- ventas
- gastos
- gastos_fijos (10 cargados)
- clientes
- movimientos_puntos
- ingredientes (23 cargados)
- proveedores (2 cargados)
- cierres_caja
- pedidos_pendientes (NUEVO - para pagos online)

## ACCESO AL SERVIDOR

Para conectarte por PuTTY:
- Host: 149.50.154.101
- Puerto: 5028
- Usuario: root
- Contrasena: (la que paso el tecnico de DonWeb)

## DEPLOY Y GITHUB

Para subir cambios:
  cd Desktop\MDK_Sistema
  git add .
  git commit -m "Descripcion del cambio"
  git push

Despues, en PuTTY:
  cd /var/www/mdk-sistema
  git pull
  systemctl restart mdk

## SERVICIOS EN EL SERVIDOR

- mdk.service (systemd): corre gunicorn con la app Flask
- nginx: servidor web con proxy al puerto 5000
- certbot: renueva el certificado SSL automaticamente cada 90 dias

## PROBLEMAS CONOCIDOS Y SOLUCIONES

- La base de datos se borra si se cambia la estructura (init_db.py detecta y borra)
- El service worker puede servir version vieja en el celular (solucion: cambiar CACHE_NAME)
- MercadoPago no permite pagarse a uno mismo (usar cuenta de otra persona)
- El servidor se actualiza automaticamente cada 90 dias con SSL

## PROXIMOS PASOS

Inmediatos:
1. Actualizar PROYECTO.md (HECHO - 23/09/2026)
2. Probar todo en el negocio

Corto plazo:
1. Sistema de puntos (canje)
2. Integracion con PedidosYa
3. Marketing automatico

Mediano plazo:
1. Impresora de comandas
2. Prediccion de demanda
3. Alertas inteligentes

## NOTAS PARA LA IA (Deepy)

Si estas leyendo esto porque perdiste el contexto:

1. El dueno es Sergio, tiene un negocio de shawarma en Buenos Aires (MDK Shawarma)
2. Sergio NO es tecnico, explicar todo paso a paso, sin tecnicismos
3. El sistema esta funcionando en DonWeb (https://sistema.mdk-shawarma.com)
4. La contrasena del dueno es MDK2026
5. El empleado entra sin contrasena en /empleado
6. Los clientes piden por QR en /pedido
7. El sistema acepta pagos online con MercadoPago (funcionando desde 23/09/2026)
8. El codigo esta en GitHub y se sube con git push
9. El servidor se actualiza con git pull + systemctl restart mdk
10. Cuando dudes, preguntar antes de asumir

## CONTACTO

- Dueno: Sergio
- Negocio: MDK Shawarma (Maison du Kebab)
- Ubicacion: Buenos Aires, Argentina
- Web: https://mdk-shawarma.com

---

Este archivo es la memoria del proyecto. Actualizarlo cada vez que se haga un cambio importante.