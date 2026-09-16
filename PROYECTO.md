# PROYECTO MDK SHAWARMA - SISTEMA DE GESTION

Ultima actualizacion: 16/09/2026

## DESCRIPCION

Sistema web de gestion para MDK Shawarma (Maison du Kebab), negocio de comida arabe en Buenos Aires, Argentina.

## URLs DEL SISTEMA

- Sistema en Render: https://mdk-sistema.onrender.com
- Pedido clientes: https://mdk-sistema.onrender.com/pedido
- Panel empleado: https://mdk-sistema.onrender.com/empleado
- Web publica: https://mdk-shawarma.com
- GitHub: https://github.com/MDKShawarma/mdk-sistema

## CREDENCIALES

- Dueno (Sergio): contrasena MDK2026 - acceso TOTAL
- Empleado: sin contrasena en /empleado - Ventas, Productos, Stock, Gastos, Cierre de Caja
- Cliente: sin contrasena en /pedido - solo hacer pedidos

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
- Listar clientes (332 cargados)
- Agregar cliente
- Ver detalle e historial
- Eliminar cliente

### Proveedores
- Listar (Ezequiel, Sergio)
- Agregar y eliminar

### Chat con IA
- Chat con Ollama + Mistral

### Cierre de Caja (NUEVO)
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
- Metodo de pago
- Notas/sugerencias
- Numero de pedido correlativo
- Aviso de demora si hay 10+ pedidos pendientes
- Registro automatico de cliente nuevo

### PWA (App instalable)
- Manifest.json
- Service Worker
- Iconos 192x192 y 512x512
- Instalable desde Chrome
- Registro automatico

## FUNCIONES PENDIENTES

- Sistema de puntos (fidelidad)
- WhatsApp automatico
- Impresora de comandas

## ESTRUCTURA DEL PROYECTO

MDK_Sistema/
- app.py (archivo principal Flask)
- init_db.py (inicializacion de BD)
- requirements.txt
- mdk.db (base de datos SQLite)
- crear_iconos.py
- static/
  - logo.png
  - style.css
  - manifest.json
  - service-worker.js
  - icon-192.png
  - icon-512.png
- templates/
  - login.html
  - inicio.html
  - empleado.html
  - productos.html
  - stock.html
  - ventas.html
  - gastos.html
  - gastos_fijos.html
  - contador.html
  - informe.html
  - clientes.html
  - cliente_detalle.html
  - proveedores.html
  - chat.html
  - cierre_caja.html
  - pedido_cliente.html

## BASE DE DATOS - TABLAS

- productos (29 cargados)
- ventas
- gastos
- gastos_fijos (10 cargados)
- clientes (332 cargados)
- ingredientes (23 cargados)
- proveedores (2 cargados)
- cierres_caja (NUEVO)

IMPORTANTE: En Render la BD se borra en cada deploy. Los datos iniciales se cargan solos pero las ventas y clientes se pierden.

## DEPLOY Y GITHUB

Para subir cambios:
  cd Desktop\MDK_Sistema
  git add .
  git commit -m "Descripcion del cambio"
  git push

Render hace deploy automatico en 1-2 minutos.

## CONFIGURACION LOCAL

Requisitos:
- Python 3.9+
- Flask
- Pillow
- Ollama + Mistral (para chat IA)

Instalacion:
  cd Desktop\MDK_Sistema
  pip install flask pillow
  python app.py

URLs locales:
- Compu: http://localhost:5000
- Celular: http://192.168.1.54:5000 (misma WiFi)

## HISTORIAL DE CAMBIOS

### 2026-09-08 a 2026-09-14
- Sistema base creado (Flask + SQLite)
- Productos, ventas, stock, gastos, informes
- Clientes (332 cargados)
- Chat con IA
- Sistema en Render
- PWA (manifest, service worker, iconos)
- Web publica en DonWeb
- QR de pedidos para clientes
- Personalizacion de Smudis

### 2026-09-15
- Roles separados: dueno vs empleado
- Empleado no puede ver panel de dueno
- Cierre de caja obligatorio despues de las 22:30
- Formulario de cierre (efectivo + MercadoPago)
- Historial de cierres para dueno

### 2026-09-16
- Creacion del archivo PROYECTO.md (este archivo)

## PROBLEMAS CONOCIDOS Y SOLUCIONES

- Render se duerme cada 15 min: normal en plan gratis, tarda 30-50s en despertar
- Base de datos se borra en deploy: migrar a DonWeb Cloud o compu local
- Chrome no muestra cartel PWA: Chrome exige HTTPS y engagement. Buscar en 3 puntitos
- Antivirus marca .bat como virus: falso positivo. Usar acceso directo a CMD

## PROXIMOS PASOS

Inmediatos:
1. Probar cierre de caja completo
2. Verificar bloqueo despues de las 22:30

Corto plazo:
1. Sistema de puntos (fidelidad)
2. WhatsApp automatico
3. Comprar compu nueva (Lenovo ThinkPad T14 Gen 1, $550.000)

Mediano plazo:
1. Migrar a DonWeb Cloud Server ($4.500/mes)
2. Impresora de comandas
3. Integracion con PedidosYa

## NOTAS PARA LA IA (Deepy)

Si estas leyendo esto porque perdiste el contexto:

1. El dueno es Sergio, tiene un negocio de shawarma en Buenos Aires (MDK Shawarma)
2. Sergio NO es tecnico, explicar todo paso a paso, sin tecnicismos
3. El sistema ya esta funcionando en Render
4. La contrasena del dueno es MDK2026
5. El empleado entra sin contrasena en /empleado
6. Los clientes piden por QR en /pedido
7. Hicimos el cierre de caja pero falta probarlo bien
8. El codigo esta en GitHub y se sube con git push
9. Usar comandos de CMD para todo
10. Cuando dudes, preguntar antes de asumir

## CONTACTO

- Dueno: Sergio
- Negocio: MDK Shawarma (Maison du Kebab)
- Ubicacion: Buenos Aires, Argentina
- Web: https://mdk-shawarma.com

---

Este archivo es la memoria del proyecto. Actualizarlo cada vez que se haga un cambio importante.