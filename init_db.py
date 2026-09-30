import sqlite3
import os

def inicializar_base_datos():
    """Crea o actualiza la base de datos SIN BORRAR NUNCA los datos existentes"""

    # ============================
    # CREAR CONEXION
    # ============================
    conn = sqlite3.connect('mdk.db')
    cursor = conn.cursor()

    # ============================
    # CREAR TABLAS SI NO EXISTEN
    # ============================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            stock_minimo INTEGER DEFAULT 10
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            total REAL,
            metodo_pago TEXT,
            notas TEXT,
            cliente_id INTEGER,
            tipo_origen TEXT DEFAULT 'empleado',
            numero_pedido INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concepto TEXT,
            monto REAL,
            categoria TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos_fijos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concepto TEXT,
            monto_mensual REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            total_compras REAL DEFAULT 0,
            cantidad_pedidos INTEGER DEFAULT 0,
            puntos INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos_puntos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            puntos INTEGER,
            tipo TEXT,
            motivo TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            stock_actual REAL DEFAULT 0,
            unidad TEXT,
            stock_minimo REAL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            productos TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos_pendientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referencia TEXT UNIQUE,
            nombre TEXT,
            telefono TEXT,
            carrito TEXT,
            total REAL,
            estado TEXT DEFAULT 'pendiente',
            payment_id TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cierres_caja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE UNIQUE,
            efectivo_esperado REAL DEFAULT 0,
            efectivo_contado REAL DEFAULT 0,
            mercadopago_esperado REAL DEFAULT 0,
            mercadopago_contado REAL DEFAULT 0,
            diferencia_efectivo REAL DEFAULT 0,
            diferencia_mercadopago REAL DEFAULT 0,
            total_esperado REAL DEFAULT 0,
            total_contado REAL DEFAULT 0,
            diferencia_total REAL DEFAULT 0,
            observaciones TEXT,
            fecha_cierre TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # ============================
    # AGREGAR COLUMNAS QUE FALTEN (SIN BORRAR NADA)
    # ============================
    def agregar_columna_si_falta(tabla, columna, definicion):
        try:
            cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = [col[1] for col in cursor.fetchall()]
            if columna not in columnas:
                cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {definicion}")
                conn.commit()
                print(f"OK: Columna '{columna}' agregada a {tabla}")
        except Exception as e:
            print(f"AVISO: No se pudo agregar '{columna}' a {tabla}: {e}")

    # ventas: columnas nuevas que fuimos agregando
    agregar_columna_si_falta('ventas', 'tipo_origen', "TEXT DEFAULT 'empleado'")
    agregar_columna_si_falta('ventas', 'numero_pedido', 'INTEGER')
    agregar_columna_si_falta('ventas', 'cliente_id', 'INTEGER')
    agregar_columna_si_falta('ventas', 'impreso', 'INTEGER DEFAULT 0')

    # clientes: columnas nuevas
    agregar_columna_si_falta('clientes', 'puntos', 'INTEGER DEFAULT 0')

    # ============================
    # CARGAR PRODUCTOS SI ESTA VACIO
    # ============================
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("shawarma", "Comidas", 14000, 50, 10),
            ("FALAFEL", "Comidas", 11000, 50, 10),
            ("FATAY", "Comidas", 4000, 60, 15),
            ("HUMUS", "Comidas", 8000, 30, 5),
            ("KEBBE", "Comidas", 10000, 30, 5),
            ("Combo Shaw Papas", "Comidas", 19000, 40, 8),
            ("Combo Falafel", "Comidas", 16000, 30, 5),
            ("Combo Fatay + Papas", "Comidas", 9000, 25, 5),
            ("PAPAS FRITAS", "Comidas", 8000, 80, 15),
            ("Nuggets/Papas", "Comidas", 14000, 25, 5),
            ("Pan individual", "Comidas", 600, 100, 20),
            ("Bolsa panes", "Comidas", 6000, 40, 10),
            ("COPA HELADO", "Postres", 5000, 20, 5),
            ("DEDITOS", "Postres", 2000, 30, 5),
            ("Baklava + Baileys", "Postres", 10500, 15, 3),
            ("GASEOSA - Coca Cola", "Bebidas", 4000, 16, 5),
            ("GASEOSA - Coca Zero", "Bebidas", 4000, 13, 5),
            ("GASEOSA - Sprite", "Bebidas", 4000, 4, 3),
            ("GASEOSA - Sprite Zero", "Bebidas", 4000, 6, 3),
            ("GASEOSA - Fanta", "Bebidas", 4000, 9, 3),
            ("JUGO - Smudis", "Bebidas", 4500, 27, 5),
            ("AGUA - Con gas", "Bebidas", 3500, 8, 5),
            ("AGUA - Sin gas", "Bebidas", 3500, 8, 5),
            ("CERVEZA - Artesanal Pampa", "Bebidas con alcohol", 5000, 5, 3),
            ("CERVEZA - Andes IPA", "Bebidas con alcohol", 5000, 8, 3),
            ("CERVEZA - Andes Roja", "Bebidas con alcohol", 5000, 5, 3),
            ("FERNET COLA", "Bebidas con alcohol", 5000, 10, 2),
            ("VINO - Partridge", "Bebidas con alcohol", 6000, 1, 0),
            ("VINO - Killka", "Bebidas con alcohol", 8000, 2, 0),
        ]
        for prod in productos:
            cursor.execute('''
                INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo)
                VALUES (?, ?, ?, ?, ?)
            ''', prod)
        conn.commit()
        print(f"OK: {len(productos)} productos cargados")

    # ============================
    # CARGAR GASTOS FIJOS SI ESTA VACIO
    # ============================
    cursor.execute("SELECT COUNT(*) FROM gastos_fijos")
    if cursor.fetchone()[0] == 0:
        gastos = [
            ("Alquiler", 600000),
            ("Agua", 30000),
            ("Luz", 200000),
            ("Seguridad e higiene", 56358),
            ("Publicidad", 1862),
            ("Internet", 15700),
            ("+Vida", 39360),
            ("Contador", 65000),
            ("Lautaro monotributo", 52000),
            ("Empleados (2)", 1920000)
        ]
        for g in gastos:
            cursor.execute("INSERT INTO gastos_fijos (concepto, monto_mensual) VALUES (?, ?)", g)
        conn.commit()
        print(f"OK: {len(gastos)} gastos fijos cargados")

    # ============================
    # CARGAR PROVEEDORES SI ESTA VACIO
    # ============================
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    if cursor.fetchone()[0] == 0:
        proveedores = [
            ("Ezequiel", "1166204775", "carne,verduras,bebidas,papas,garbanzos,queso,especias,vinagre,harina,sal"),
            ("Sergio", "1170634208", "pan,kebbes,postres,pasta_mani,garam_masala,aceite_freidora"),
        ]
        for p in proveedores:
            cursor.execute("INSERT INTO proveedores (nombre, telefono, productos) VALUES (?, ?, ?)", p)
        conn.commit()
        print(f"OK: {len(proveedores)} proveedores cargados")

    # ============================
    # CARGAR INGREDIENTES SI ESTA VACIO
    # ============================
    cursor.execute("SELECT COUNT(*) FROM ingredientes")
    if cursor.fetchone()[0] == 0:
        ingredientes = [
            ("Bola de lomo", "carnes", 55, "kg", 3),
            ("Carne picada", "carnes", 8, "kg", 2),
            ("Garbanzos", "legumbres", 25, "kg", 5),
            ("Harina", "secos", 20, "kg", 5),
            ("Aceite freidora", "secos", 20, "litros", 5),
            ("Aceite cocina", "secos", 5, "litros", 1),
            ("Vinagre", "secos", 3, "litros", 1),
            ("Garam masala", "especias", 1, "kg", 0.2),
            ("Comino", "especias", 1, "kg", 0.2),
            ("Aji molido", "especias", 1, "kg", 0.2),
            ("Chimichurri", "especias", 1, "kg", 0.2),
            ("Sal", "especias", 2, "kg", 0.5),
            ("Queso crema", "salsa_montanesa", 6, "kg", 3),
            ("Pasta de mani", "salsa_montanesa", 20, "kg", 5),
            ("Limon", "verduras", 3, "kg", 1),
            ("Repollo", "verduras", 15, "kg", 3),
            ("Cebolla", "verduras", 20, "kg", 5),
            ("Tomate", "verduras", 15, "kg", 3),
            ("Morron", "verduras", 10, "unidades", 3),
            ("Pan pita", "panificados", 30, "bolsas", 5),
            ("Papas congeladas", "congelados", 20, "bolsas", 5),
            ("Kebbes", "congelados", 50, "unidades", 10),
            ("Postres", "postres", 5, "kg", 1),
        ]
        for ing in ingredientes:
            cursor.execute('''
                INSERT INTO ingredientes (nombre, categoria, stock_actual, unidad, stock_minimo)
                VALUES (?, ?, ?, ?, ?)
            ''', ing)
        conn.commit()
        print(f"OK: {len(ingredientes)} ingredientes cargados")

    # ============================
    # CERRAR
    # ============================
    conn.close()
    print("Base de datos lista (sin borrar datos)")


if __name__ == '__main__':
    inicializar_base_datos()