from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import json
import subprocess
import re
from datetime import datetime
import functools

app = Flask(__name__)
app.secret_key = 'mdk_secret_key_2026'

CONTRASENA = 'MDK2026'

def get_db():
    conn = sqlite3.connect('mdk.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_requerido(f):
    @functools.wraps(f)
    def decorador(*args, **kwargs):
        if not session.get('autenticado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorador

def limpiar_respuesta(texto):
    texto = re.sub(r'\x1b\[[0-9;]*[KkDdCc]', '', texto)
    texto = re.sub(r'[^\x20-\x7EáéíóúÁÉÍÓÚñÑ¿¡]', '', texto)
    texto = re.sub(r'\b(\w+?)\1\b', r'\1', texto)
    texto = re.sub(r'\b(\w{3,}?)\1\b', r'\1', texto)
    texto = texto.strip()
    return texto

def preguntar_deepseek(pregunta):
    try:
        prompt = f"Respondé en español. Escribí solo la respuesta final, sin repetir sílabas ni palabras. Pregunta: {pregunta}"
        resultado = subprocess.run(
            ['ollama', 'run', 'mistral', prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=180
        )
        respuesta = resultado.stdout.strip()
        respuesta = limpiar_respuesta(respuesta)
        return respuesta[:800]
    except Exception as e:
        return f"Error: {str(e)}"

def get_emoji(nombre):
    nombre_lower = nombre.lower()
    if 'bolsa de panes' in nombre_lower:
        return '🥖'
    if 'pan individual' in nombre_lower:
        return '🫓'
    emojis = {
        'shawarma': '🌯',
        'falafel': '🧆',
        'fatay': '🥟',
        'humus': '🫘',
        'kebbe': '🥩',
        'papas': '🍟',
        'helado': '🍨',
        'deditos': '🍡',
        'baklava': '🍯',
        'coca': '🥤',
        'smudis': '🥤',
        'agua': '💧',
        'cerveza': '🍺',
        'baileys': '🥃',
        'gin': '🍸',
        'vino': '🍷',
        'pan': '🫓'
    }
    for clave, emoji in emojis.items():
        if clave in nombre_lower:
            return emoji
    return '🍽️'

def orden_importancia(nombre):
    nombre_lower = nombre.lower()
    if 'combo' in nombre_lower:
        return 5
    elif 'shawarma' in nombre_lower:
        return 0
    elif 'falafel' in nombre_lower:
        return 1
    elif 'fatay' in nombre_lower:
        return 2
    elif 'humus' in nombre_lower:
        return 3
    elif 'kebbe' in nombre_lower:
        return 4
    elif 'papas' in nombre_lower:
        return 6
    elif any(p in nombre_lower for p in ['postre', 'helado', 'deditos', 'baklava']):
        return 7
    elif any(b in nombre_lower for b in ['agua', 'coca', 'smudis', 'cerveza', 'baileys', 'gin', 'vino']):
        return 8
    else:
        return 9

def es_empleado():
    ip = request.remote_addr
    return ip != '127.0.0.1'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contrasena = request.form.get('contrasena', '')
        if contrasena == CONTRASENA:
            session['autenticado'] = True
            return redirect(url_for('inicio'))
        else:
            return render_template('login.html', error="Contraseña incorrecta")
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session['autenticado'] = False
    return redirect(url_for('login'))

@app.route('/empleado')
def empleado():
    return render_template('empleado.html')

@app.route('/')
@login_requerido
def inicio():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE date(fecha) = date('now')")
    ventas_hoy = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ventas WHERE date(fecha) = date('now')")
    pedidos_hoy = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(monto_mensual) / 16 FROM gastos_fijos")
    gasto_diario = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM productos WHERE stock <= stock_minimo")
    stock_bajo = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ingredientes WHERE stock_actual <= stock_minimo")
    ingredientes_bajos = cursor.fetchone()[0]
    conn.close()
    return render_template('inicio.html', ventas_hoy=ventas_hoy, pedidos_hoy=pedidos_hoy, gasto_diario=gasto_diario, stock_bajo=stock_bajo, total_productos=total_productos, total_clientes=total_clientes, ingredientes_bajos=ingredientes_bajos)

@app.route('/productos', methods=['GET', 'POST'])
@login_requerido
def productos():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        nuevo_precio = request.form.get('precio')
        if producto_id and nuevo_precio:
            cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (float(nuevo_precio), int(producto_id)))
            conn.commit()
    cursor.execute("SELECT * FROM productos")
    productos_raw = cursor.fetchall()
    productos = sorted(productos_raw, key=lambda p: (orden_importancia(p[1]), p[1]))
    conn.close()
    empleado = es_empleado()
    return render_template('productos.html', productos=productos, empleado=empleado)

@app.route('/agregar_producto', methods=['POST'])
@login_requerido
def agregar_producto():
    nombre = request.form.get('nombre')
    categoria = request.form.get('categoria')
    precio = request.form.get('precio')
    stock = request.form.get('stock')
    if nombre and categoria and precio and stock:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo) VALUES (?, ?, ?, ?, ?)",
            (nombre, categoria, float(precio), int(stock), 10)
        )
        conn.commit()
        conn.close()
    return redirect(url_for('productos'))

@app.route('/stock', methods=['GET', 'POST'])
@login_requerido
def stock():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        accion = request.form.get('accion')
        if accion == 'reset':
            cursor.execute("UPDATE ingredientes SET stock_actual = 0")
            conn.commit()
        else:
            ingrediente_id = request.form.get('ingrediente_id')
            cantidad = request.form.get('cantidad')
            if ingrediente_id and cantidad:
                cantidad = float(cantidad)
                if accion == 'sumar':
                    cursor.execute("UPDATE ingredientes SET stock_actual = stock_actual + ? WHERE id = ?", (cantidad, ingrediente_id))
                elif accion == 'restar':
                    cursor.execute("UPDATE ingredientes SET stock_actual = stock_actual - ? WHERE id = ?", (cantidad, ingrediente_id))
                elif accion == 'fijar':
                    cursor.execute("UPDATE ingredientes SET stock_actual = ? WHERE id = ?", (cantidad, ingrediente_id))
                conn.commit()
    cursor.execute("SELECT * FROM ingredientes ORDER BY categoria, nombre")
    ingredientes = cursor.fetchall()
    conn.close()
    empleado = es_empleado()
    return render_template('stock.html', ingredientes=ingredientes, empleado=empleado)

@app.route('/ventas', methods=['GET', 'POST'])
@login_requerido
def ventas():
    conn = get_db()
    cursor = conn.cursor()
    comanda = None

    if request.method == 'POST':
        carrito_json = request.form.get('carrito')
        cliente_id = request.form.get('cliente_id')
        metodo_pago = request.form.get('metodo_pago')

        if carrito_json and metodo_pago:
            carrito = json.loads(carrito_json)
            total_general = 0
            for item in carrito:
                producto_id = int(item['id'])
                cantidad = int(item['cantidad'])
                cursor.execute("SELECT nombre, precio, stock FROM productos WHERE id = ?", (producto_id,))
                producto = cursor.fetchone()
                if not producto or producto[2] < cantidad:
                    conn.close()
                    return "Error: stock insuficiente para " + item['nombre'], 400
                total_general += producto[1] * cantidad

            for item in carrito:
                producto_id = int(item['id'])
                cantidad = int(item['cantidad'])
                notas = item.get('notas', '')
                cursor.execute("SELECT nombre, precio FROM productos WHERE id = ?", (producto_id,))
                producto = cursor.fetchone()
                total_item = producto[1] * cantidad
                cursor.execute('''
                    INSERT INTO ventas (producto_id, cantidad, total, metodo_pago, notas, cliente_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (producto_id, cantidad, total_item, metodo_pago, notas, cliente_id if cliente_id else None))
                cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (cantidad, producto_id))

            if cliente_id:
                cursor.execute('UPDATE clientes SET total_compras = total_compras + ?, cantidad_pedidos = cantidad_pedidos + 1 WHERE id = ?', (total_general, int(cliente_id)))

            conn.commit()

            comanda = {
                'pedido_id': cursor.lastrowid,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'productos_comanda': carrito,
                'total': total_general,
                'metodo_pago': metodo_pago
            }

    cursor.execute('''
        SELECT v.id, p.nombre, v.cantidad, v.total, v.metodo_pago, v.notas, v.fecha, c.nombre as cliente_nombre
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        LEFT JOIN clientes c ON v.cliente_id = c.id
        WHERE date(v.fecha) = date('now')
        ORDER BY v.fecha DESC
    ''')
    ventas = cursor.fetchall()

    cursor.execute("SELECT id, nombre, precio FROM productos WHERE stock > 0")
    productos_raw = cursor.fetchall()
    productos_ordenados = sorted(productos_raw, key=lambda p: (orden_importancia(p[1]), p[1]))
    productos = [(p[0], p[1], p[2], get_emoji(p[1])) for p in productos_ordenados]

    cursor.execute("SELECT id, nombre FROM clientes ORDER BY nombre")
    clientes = cursor.fetchall()

    conn.close()
    empleado = es_empleado()
    return render_template('ventas.html', ventas=ventas, productos=productos, clientes=clientes, comanda=comanda, empleado=empleado)

@app.route('/gastos', methods=['GET', 'POST'])
@login_requerido
def gastos():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        concepto = request.form.get('concepto')
        monto = request.form.get('monto')
        categoria = request.form.get('categoria')
        if concepto and monto and categoria:
            cursor.execute('INSERT INTO gastos (concepto, monto, categoria) VALUES (?, ?, ?)', (concepto, float(monto), categoria))
            conn.commit()
    cursor.execute('''SELECT id, concepto, monto, categoria, fecha FROM gastos WHERE date(fecha) = date('now') ORDER BY fecha DESC''')
    gastos = cursor.fetchall()
    cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM gastos WHERE date(fecha) = date('now')")
    total_gastos = cursor.fetchone()[0]
    conn.close()
    empleado = es_empleado()
    return render_template('gastos.html', gastos=gastos, total_gastos=total_gastos, empleado=empleado)

@app.route('/gastos_fijos', methods=['GET', 'POST'])
@login_requerido
def gastos_fijos():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        accion = request.form.get('accion')
        if accion == 'agregar':
            concepto = request.form.get('concepto')
            monto = request.form.get('monto')
            if concepto and monto:
                cursor.execute("INSERT INTO gastos_fijos (concepto, monto_mensual) VALUES (?, ?)", (concepto, float(monto)))
                conn.commit()
        elif accion == 'eliminar':
            gasto_id = request.form.get('gasto_id')
            if gasto_id:
                cursor.execute("DELETE FROM gastos_fijos WHERE id = ?", (gasto_id,))
                conn.commit()
        elif accion == 'editar':
            gasto_id = request.form.get('gasto_id')
            monto = request.form.get('monto')
            if gasto_id and monto:
                cursor.execute("UPDATE gastos_fijos SET monto_mensual = ? WHERE id = ?", (float(monto), int(gasto_id)))
                conn.commit()
    cursor.execute("SELECT * FROM gastos_fijos ORDER BY monto_mensual DESC")
    gastos = cursor.fetchall()
    cursor.execute("SELECT SUM(monto_mensual) FROM gastos_fijos")
    total = cursor.fetchone()[0] or 0
    conn.close()
    return render_template('gastos_fijos.html', gastos=gastos, total=total)

@app.route('/contador')
@login_requerido
def contador():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE strftime('%m', fecha) = strftime('%m', 'now')")
    ingresos_mes = cursor.fetchone()[0]
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE date(fecha) = date('now')")
    ingresos_hoy = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(monto_mensual) FROM gastos_fijos")
    gastos_fijos_val = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM gastos WHERE strftime('%m', fecha) = strftime('%m', 'now')")
    gastos_variables = cursor.fetchone()[0]
    total_gastos = gastos_fijos_val + gastos_variables
    balance = ingresos_mes - total_gastos
    iva_estimado = ingresos_mes * 0.21
    iibb_estimado = ingresos_mes * 0.035
    cursor.execute("""
        SELECT date(fecha) as dia, SUM(total) as total
        FROM ventas
        WHERE date(fecha) >= date('now', '-7 days')
        GROUP BY date(fecha)
        ORDER BY fecha DESC
    """)
    ventas_semana = cursor.fetchall()
    conn.close()
    return render_template('contador.html',
                         ingresos_mes=ingresos_mes,
                         ingresos_hoy=ingresos_hoy,
                         gastos_fijos=gastos_fijos_val,
                         gastos_variables=gastos_variables,
                         total_gastos=total_gastos,
                         balance=balance,
                         iva_estimado=iva_estimado,
                         iibb_estimado=iibb_estimado,
                         ventas_semana=ventas_semana)

@app.route('/informe')
@login_requerido
def informe():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE date(fecha) = date('now')")
    ventas_hoy = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE date(fecha) = date('now', '-1 day')")
    ventas_ayer = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(monto_mensual) / 16 FROM gastos_fijos")
    gasto_diario = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT date(fecha) as dia, SUM(total) as total, COUNT(*) as pedidos
        FROM ventas
        WHERE date(fecha) >= date('now', '-14 days')
        GROUP BY date(fecha)
        ORDER BY dia DESC
    """)
    dias_raw = cursor.fetchall()
    
    historial = []
    for dia in dias_raw:
        fecha = dia[0]
        total = dia[1]
        pedidos = dia[2]
        
        cursor.execute("""
            SELECT p.nombre, SUM(v.cantidad) as cantidad, SUM(v.total) as total
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            WHERE date(v.fecha) = ?
            GROUP BY p.id
            ORDER BY total DESC
        """, (fecha,))
        productos = cursor.fetchall()
        
        historial.append({
            'fecha': fecha,
            'total': total,
            'pedidos': pedidos,
            'productos': [{'nombre': p[0], 'cantidad': p[1], 'total': p[2]} for p in productos]
        })
    
    conn.close()
    return render_template('informe.html', 
                         ventas_hoy=ventas_hoy, 
                         ventas_ayer=ventas_ayer, 
                         gasto_diario=gasto_diario, 
                         historial=historial)

@app.route('/clientes', methods=['GET', 'POST'])
@login_requerido
def clientes():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        if nombre and telefono:
            cursor.execute("INSERT INTO clientes (nombre, telefono) VALUES (?, ?)", (nombre, telefono))
            conn.commit()
    cursor.execute("SELECT id, nombre, telefono, total_compras, cantidad_pedidos FROM clientes ORDER BY total_compras DESC")
    clientes = cursor.fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/eliminar_cliente/<int:cliente_id>', methods=['POST'])
@login_requerido
def eliminar_cliente(cliente_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

@app.route('/cliente/<int:cliente_id>')
@login_requerido
def cliente_detalle(cliente_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, telefono, total_compras, cantidad_pedidos FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    if not cliente:
        conn.close()
        return "Cliente no encontrado", 404
    cursor.execute('''
        SELECT v.id, p.nombre, v.cantidad, v.total, v.metodo_pago, v.notas, v.fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        WHERE v.cliente_id = ?
        ORDER BY v.fecha DESC
    ''', (cliente_id,))
    compras = cursor.fetchall()
    conn.close()
    return render_template('cliente_detalle.html', cliente=cliente, compras=compras)

@app.route('/proveedores')
@login_requerido
def proveedores():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/agregar_proveedor', methods=['POST'])
@login_requerido
def agregar_proveedor():
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    productos = request.form.get('productos')
    if nombre and telefono and productos:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO proveedores (nombre, telefono, productos) VALUES (?, ?, ?)",
            (nombre, telefono, productos)
        )
        conn.commit()
        conn.close()
    return redirect(url_for('proveedores'))

@app.route('/eliminar_proveedor/<int:proveedor_id>', methods=['POST'])
@login_requerido
def eliminar_proveedor(proveedor_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id = ?", (proveedor_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('proveedores'))

@app.route('/chat', methods=['GET', 'POST'])
@login_requerido
def chat():
    respuesta = ""
    pregunta = ""
    if request.method == 'POST':
        pregunta = request.form.get('pregunta', '')
        if pregunta:
            respuesta = preguntar_deepseek(pregunta)
    return render_template('chat.html', respuesta=respuesta, pregunta=pregunta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)