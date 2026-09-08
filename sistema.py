import sqlite3
import os
from datetime import datetime, timedelta

class MDKSistema:
    def __init__(self):
        self.conn = sqlite3.connect('mdk.db')
        self.crear_tablas()
        self.cargar_productos()
        self.cargar_gastos()
        print("Sistema MDK actualizado correctamente")
    
    def crear_tablas(self):
        cursor = self.conn.cursor()
        
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
                cliente_id INTEGER,
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
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def cargar_productos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos")
        
        if cursor.fetchone()[0] == 0:
            productos = [
                ("shawarma", "Comidas", 14000, 50, 10),
                ("Combo Shaw Papas", "Comidas", 19000, 40, 8),
                ("Combo Falafel", "Comidas", 16000, 30, 5),
                ("Combo Fatay + Papas", "Comidas", 9000, 25, 5),
                ("FALAFEL", "Comidas", 11000, 50, 10),
                ("FATAY", "Comidas", 4000, 60, 15),
                ("HUMUS", "Comidas", 8000, 30, 5),
                ("KEBBE", "Comidas", 10000, 30, 5),
                ("Nuggets/Papas", "Comidas", 14000, 25, 5),
                ("PAPAS FRITAS", "Comidas", 8000, 80, 15),
                ("Pan individual", "Comidas", 600, 100, 20),
                ("Bolsa panes", "Comidas", 6000, 40, 10),
                ("COPA HELADO", "Postres", 5000, 20, 5),
                ("DEDITOS", "Postres", 2000, 30, 5),
                ("Baklava + Baileys", "Postres", 10500, 15, 3),
                ("COCAS", "Bebidas", 4000, 100, 20),
                ("AGUAS", "Bebidas", 3500, 80, 15),
                ("Smudis", "Bebidas", 4500, 40, 10),
                ("CERVEZAS", "Bebidas con alcohol", 5000, 60, 15),
                ("BAILEYS 50ML", "Bebidas con alcohol", 6500, 20, 5),
                ("GIN TONIC", "Bebidas con alcohol", 6000, 15, 3),
                ("VINO TINTO", "Bebidas con alcohol", 8000, 20, 5),
                ("VINO ROSADO", "Bebidas con alcohol", 6000, 15, 3),
            ]
            
            cursor.executemany(
                "INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo) VALUES (?, ?, ?, ?, ?)",
                productos
            )
            self.conn.commit()
            print("Productos cargados correctamente")
    
    def cargar_gastos(self):
        cursor = self.conn.cursor()
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
            
            cursor.executemany(
                "INSERT INTO gastos_fijos (concepto, monto_mensual) VALUES (?, ?)",
                gastos
            )
            self.conn.commit()
            print("Gastos fijos cargados correctamente")
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu(self):
        while True:
            self.limpiar_pantalla()
            print("=" * 55)
            print("        MDK SHAWARMA - SISTEMA DE GESTION")
            print("=" * 55)
            print("1. Ver productos")
            print("2. Registrar venta")
            print("3. Ver ventas de hoy")
            print("4. Registrar gasto")
            print("5. Ver balance del dia")
            print("6. Agregar producto")
            print("7. Ver gastos fijos mensuales")
            print("8. Informe de la manana")
            print("9. Alertas de stock")
            print("10. Resumen semanal")
            print("11. Top productos del mes")
            print("12. Proyeccion mensual")
            print("13. Registrar cliente")
            print("14. Ver clientes")
            print("15. Ventas por metodo de pago")
            print("16. Salir")
            print("=" * 55)
            
            opcion = input("Elige una opcion (1-16): ")
            
            if opcion == "1":
                self.ver_productos()
            elif opcion == "2":
                self.registrar_venta()
            elif opcion == "3":
                self.ver_ventas_hoy()
            elif opcion == "4":
                self.registrar_gasto()
            elif opcion == "5":
                self.ver_balance()
            elif opcion == "6":
                self.agregar_producto()
            elif opcion == "7":
                self.ver_gastos_fijos()
            elif opcion == "8":
                self.informe_manana()
            elif opcion == "9":
                self.alertas_stock()
            elif opcion == "10":
                self.resumen_semanal()
            elif opcion == "11":
                self.top_mensual()
            elif opcion == "12":
                self.proyeccion_mensual()
            elif opcion == "13":
                self.registrar_cliente()
            elif opcion == "14":
                self.ver_clientes()
            elif opcion == "15":
                self.ventas_por_metodo()
            elif opcion == "16":
                print("Hasta pronto!")
                break
            else:
                input("Opcion no valida. Presiona Enter para continuar...")
    
    def ver_productos(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nombre, categoria, precio, stock FROM productos ORDER BY categoria, nombre")
        productos = cursor.fetchall()
        
        print("\nPRODUCTOS DISPONIBLES:")
        print("-" * 60)
        print(f"{'ID':<5} {'Nombre':<25} {'Categoria':<20} {'Precio':<10} {'Stock':<10}")
        print("-" * 60)
        
        for prod in productos:
            print(f"{prod[0]:<5} {prod[1]:<25} {prod[2]:<20} ${prod[3]:<9,.0f} {prod[4]:<10}")
        
        print("-" * 60)
        input("\nPresiona Enter para volver...")
    
    def registrar_venta(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\nREGISTRAR VENTA")
        cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE stock > 0 ORDER BY nombre")
        productos = cursor.fetchall()
        
        print("\nProductos disponibles:")
        for prod in productos:
            print(f"{prod[0]}. {prod[1]} - ${prod[2]:,.0f} (Stock: {prod[3]})")
        
        try:
            producto_id = int(input("\nID del producto: "))
            cantidad = int(input("Cantidad: "))
            metodo = input("Metodo de pago (efectivo/mercadopago/tarjeta/pedidosya): ")
            
            cliente_id = input("ID del cliente (Enter si no tiene): ")
            if cliente_id == "":
                cliente_id = None
            else:
                cliente_id = int(cliente_id)
            
            cursor.execute("SELECT nombre, precio, stock FROM productos WHERE id = ?", (producto_id,))
            producto = cursor.fetchone()
            
            if producto and producto[2] >= cantidad:
                total = producto[1] * cantidad
                
                cursor.execute('''
                    INSERT INTO ventas (producto_id, cantidad, total, metodo_pago, cliente_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (producto_id, cantidad, total, metodo, cliente_id))
                
                cursor.execute('''
                    UPDATE productos SET stock = stock - ? WHERE id = ?
                ''', (cantidad, producto_id))
                
                if cliente_id:
                    cursor.execute('''
                        UPDATE clientes 
                        SET total_compras = total_compras + ?,
                            cantidad_pedidos = cantidad_pedidos + 1
                        WHERE id = ?
                    ''', (total, cliente_id))
                
                self.conn.commit()
                print(f"\nVenta registrada: {producto[0]} x{cantidad}")
                print(f"Total: ${total:,.0f}")
                print(f"Metodo: {metodo}")
            else:
                print("\nStock insuficiente o producto no encontrado")
        except ValueError:
            print("\nPor favor ingresa numeros validos")
        
        input("\nPresiona Enter para continuar...")
    
    def ver_ventas_hoy(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT v.id, p.nombre, v.cantidad, v.total, v.metodo_pago, v.fecha
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            WHERE date(v.fecha) = date('now')
            ORDER BY v.fecha DESC
        ''')
        
        ventas = cursor.fetchall()
        
        print("\nVENTAS DE HOY:")
        print("-" * 70)
        
        total_dia = 0
        for venta in ventas:
            print(f"#{venta[0]} | {venta[1]} | x{venta[2]} | ${venta[3]:,.0f} | {venta[4]}")
            total_dia += venta[3]
        
        print("-" * 70)
        print(f"TOTAL: ${total_dia:,.0f}")
        print(f"Cantidad de ventas: {len(ventas)}")
        
        input("\nPresiona Enter para volver...")
    
    def registrar_gasto(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\nREGISTRAR GASTO")
        concepto = input("Concepto: ")
        
        try:
            monto = float(input("Monto: $"))
            categoria = input("Categoria (mercaderia/servicios/impuestos/otros): ")
            
            cursor.execute('''
                INSERT INTO gastos (concepto, monto, categoria)
                VALUES (?, ?, ?)
            ''', (concepto, monto, categoria))
            
            self.conn.commit()
            print(f"\nGasto registrado: {concepto} - ${monto:,.0f}")
        except ValueError:
            print("\nPor favor ingresa un monto valido")
        
        input("\nPresiona Enter para continuar...")
    
    def ver_balance(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT COALESCE(SUM(total), 0) FROM ventas
            WHERE date(fecha) = date('now')
        ''')
        ingresos = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0) FROM gastos
            WHERE date(fecha) = date('now')
        ''')
        gastos = cursor.fetchone()[0]
        
        balance = ingresos - gastos
        
        print("\nBALANCE DEL DIA:")
        print("-" * 50)
        print(f"Ingresos: ${ingresos:,.0f}")
        print(f"Gastos: ${gastos:,.0f}")
        print(f"Balance: ${balance:,.0f}")
        print("-" * 50)
        
        if balance > 0:
            print("Ganancia del dia")
        elif balance < 0:
            print("Perdida del dia")
        else:
            print("Sin movimientos")
        
        input("\nPresiona Enter para volver...")
    
    def agregar_producto(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\nAGREGAR PRODUCTO")
        nombre = input("Nombre: ")
        categoria = input("Categoria: ")
        
        try:
            precio = float(input("Precio: $"))
            stock = int(input("Stock: "))
            
            cursor.execute('''
                INSERT INTO productos (nombre, categoria, precio, stock)
                VALUES (?, ?, ?, ?)
            ''', (nombre, categoria, precio, stock))
            
            self.conn.commit()
            print(f"\nProducto '{nombre}' agregado")
        except ValueError:
            print("\nPor favor ingresa valores validos")
        
        input("\nPresiona Enter para continuar...")
    
    def ver_gastos_fijos(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        cursor.execute("SELECT concepto, monto_mensual FROM gastos_fijos ORDER BY monto_mensual DESC")
        gastos = cursor.fetchall()
        
        print("\nGASTOS FIJOS MENSUALES:")
        print("-" * 50)
        
        total = 0
        for gasto in gastos:
            print(f"{gasto[0]}: ${gasto[1]:,.0f}")
            total += gasto[1]
        
        print("-" * 50)
        print(f"TOTAL MENSUAL: ${total:,.0f}")
        print(f"TOTAL SEMANAL: ${total/4:,.0f}")
        print(f"TOTAL POR DIA (4 dias): ${total/16:,.0f}")
        
        input("\nPresiona Enter para volver...")
    
    def informe_manana(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\n" + "=" * 55)
        print("   INFORME DE LA MANANA - MDK SHAWARMA")
        print("=" * 55)
        print(f"   Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("=" * 55)
        
        cursor.execute('''
            SELECT COALESCE(SUM(total), 0), COUNT(*)
            FROM ventas
            WHERE date(fecha) = date('now', '-1 day')
        ''')
        ventas_ayer = cursor.fetchone()
        
        print(f"\nVENTAS DE AYER:")
        print(f"  Total: ${ventas_ayer[0]:,.0f}")
        print(f"  Pedidos: {ventas_ayer[1]}")
        
        cursor.execute('''
            SELECT COALESCE(SUM(total), 0), COUNT(*)
            FROM ventas
            WHERE date(fecha) = date('now')
        ''')
        ventas_hoy = cursor.fetchone()
        
        print(f"\nVENTAS DE HOY:")
        print(f"  Total: ${ventas_hoy[0]:,.0f}")
        print(f"  Pedidos: {ventas_hoy[1]}")
        
        cursor.execute('''
            SELECT p.nombre, SUM(v.cantidad) as cantidad, SUM(v.total) as total
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            WHERE date(v.fecha) = date('now')
            GROUP BY p.id
            ORDER BY total DESC
            LIMIT 5
        ''')
        top = cursor.fetchall()
        
        if top:
            print(f"\nTOP 5 PRODUCTOS DE HOY:")
            for i, prod in enumerate(top, 1):
                print(f"  {i}. {prod[0]}: {prod[1]} unidades (${prod[2]:,.0f})")
        
        cursor.execute('''
            SELECT SUM(monto_mensual) / 16
            FROM gastos_fijos
        ''')
        gasto_diario = cursor.fetchone()[0]
        
        print(f"\nGASTO FIJO DE HOY: ${gasto_diario:,.0f}")
        print(f"  Te falta vender: ${max(0, gasto_diario - ventas_hoy[0]):,.0f}")
        
        cursor.execute('''
            SELECT nombre, stock, stock_minimo
            FROM productos
            WHERE stock <= stock_minimo
        ''')
        stock_bajo = cursor.fetchall()
        
        if stock_bajo:
            print(f"\nSTOCK BAJO:")
            for prod in stock_bajo:
                print(f"  {prod[0]}: {prod[1]} unidades (minimo: {prod[2]})")
        
        print("\n" + "=" * 55)
        input("\nPresiona Enter para volver...")
    
    def alertas_stock(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT nombre, stock, stock_minimo
            FROM productos
            WHERE stock <= stock_minimo
            ORDER BY stock ASC
        ''')
        
        productos_bajos = cursor.fetchall()
        
        print("\nALERTAS DE STOCK:")
        print("-" * 50)
        
        if productos_bajos:
            for prod in productos_bajos:
                print(f"ALERTA: {prod[0]}")
                print(f"  Stock actual: {prod[1]}")
                print(f"  Stock minimo: {prod[2]}")
                print(f"  Faltan: {prod[2] - prod[1]} unidades")
                print("-" * 50)
        else:
            print("Todo el stock esta bien")
        
        input("\nPresiona Enter para volver...")
    
    def resumen_semanal(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\n" + "=" * 55)
        print("   RESUMEN SEMANAL - MDK SHAWARMA")
        print("=" * 55)
        
        cursor.execute('''
            SELECT date(fecha) as dia, COUNT(*) as pedidos, SUM(total) as total
            FROM ventas
            WHERE date(fecha) >= date('now', '-7 days')
            GROUP BY date(fecha)
            ORDER BY fecha DESC
        ''')
        
        dias = cursor.fetchall()
        
        total_semana = 0
        total_pedidos = 0
        
        print(f"\n{'Dia':<15} {'Pedidos':<10} {'Total':<15}")
        print("-" * 40)
        
        for dia in dias:
            print(f"{dia[0]:<15} {dia[1]:<10} ${dia[2]:<14,.0f}")
            total_semana += dia[2]
            total_pedidos += dia[1]
        
        print("-" * 40)
        print(f"{'TOTAL':<15} {total_pedidos:<10} ${total_semana:<14,.0f}")
        
        if dias:
            promedio_diario = total_semana / len(dias)
            print(f"\nPromedio diario: ${promedio_diario:,.0f}")
        
        cursor.execute('''
            SELECT SUM(monto_mensual) / 4
            FROM gastos_fijos
        ''')
        gasto_semanal = cursor.fetchone()[0]
        
        print(f"Gasto fijo semanal: ${gasto_semanal:,.0f}")
        print(f"Diferencia: ${total_semana - gasto_semanal:,.0f}")
        
        print("\n" + "=" * 55)
        input("\nPresiona Enter para volver...")
    
    def proyeccion_mensual(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\n" + "=" * 55)
        print("   PROYECCION MENSUAL - MDK SHAWARMA")
        print("=" * 55)
        
        cursor.execute('''
            SELECT COALESCE(SUM(total), 0), COUNT(*)
            FROM ventas
            WHERE strftime('%m', fecha) = strftime('%m', 'now')
        ''')
        ventas_mes = cursor.fetchone()
        
        cursor.execute('''
            SELECT SUM(monto_mensual)
            FROM gastos_fijos
        ''')
        gastos_fijos = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0)
            FROM gastos
            WHERE strftime('%m', fecha) = strftime('%m', 'now')
        ''')
        gastos_extra = cursor.fetchone()[0]
        
        total_gastos = gastos_fijos + gastos_extra
        
        cursor.execute('''
            SELECT CAST(julianday('now') - julianday(date('now', 'start of month')) AS INTEGER) + 1
        ''')
        dias_transcurridos = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT CAST(julianday(date('now', 'start of month', '+1 month', '-1 day')) - julianday(date('now', 'start of month')) AS INTEGER) + 1
        ''')
        dias_totales_mes = cursor.fetchone()[0]
        
        if dias_transcurridos > 0:
            promedio_diario = ventas_mes[0] / dias_transcurridos
        else:
            promedio_diario = 0
        
        proyeccion_ventas = promedio_diario * dias_totales_mes
        proyeccion_ganancia = proyeccion_ventas - total_gastos
        
        print(f"\nFECHA: {datetime.now().strftime('%d/%m/%Y')}")
        print(f"Dias transcurridos: {dias_transcurridos} de {dias_totales_mes}")
        print("-" * 55)
        
        print(f"\nVENTAS DEL MES:")
        print(f"  Total actual: ${ventas_mes[0]:,.0f}")
        print(f"  Pedidos: {ventas_mes[1]}")
        print(f"  Promedio diario: ${promedio_diario:,.0f}")
        print(f"  Proyeccion a fin de mes: ${proyeccion_ventas:,.0f}")
        
        print(f"\nGASTOS DEL MES:")
        print(f"  Gastos fijos: ${gastos_fijos:,.0f}")
        print(f"  Gastos extra: ${gastos_extra:,.0f}")
        print(f"  Total gastos: ${total_gastos:,.0f}")
        
        print(f"\nPROYECCION FINAL:")
        print(f"  Ganancia estimada: ${proyeccion_ganancia:,.0f}")
        
        if proyeccion_ganancia > 0:
            print(f"  Estado: GANANCIA")
        elif proyeccion_ganancia < 0:
            print(f"  Estado: PERDIDA")
            print(f"  Te faltan: ${abs(proyeccion_ganancia):,.0f}")
        else:
            print(f"  Estado: EMPATE")
        
        print("\n" + "=" * 55)
        input("\nPresiona Enter para volver...")
    
    def top_mensual(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\n" + "=" * 55)
        print("   TOP PRODUCTOS DEL MES - MDK SHAWARMA")
        print("=" * 55)
        
        cursor.execute('''
            SELECT p.nombre, SUM(v.cantidad) as unidades, SUM(v.total) as total
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            WHERE strftime('%m', v.fecha) = strftime('%m', 'now')
            GROUP BY p.id
            ORDER BY total DESC
            LIMIT 10
        ''')
        
        top = cursor.fetchall()
        
        if top:
            print(f"\n{'#':<5} {'Producto':<25} {'Unidades':<10} {'Total':<15}")
            print("-" * 55)
            
            for i, prod in enumerate(top, 1):
                print(f"{i:<5} {prod[0]:<25} {prod[1]:<10} ${prod[2]:<14,.0f}")
        else:
            print("\nNo hay ventas registradas este mes")
        
        print("\n" + "=" * 55)
        input("\nPresiona Enter para volver...")
    
    def registrar_cliente(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\nREGISTRAR CLIENTE")
        nombre = input("Nombre: ")
        telefono = input("Telefono: ")
        
        cursor.execute('''
            INSERT INTO clientes (nombre, telefono)
            VALUES (?, ?)
        ''', (nombre, telefono))
        
        self.conn.commit()
        print(f"\nCliente '{nombre}' registrado correctamente")
        
        input("\nPresiona Enter para volver...")
    
    def ver_clientes(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, nombre, telefono, total_compras, cantidad_pedidos
            FROM clientes
            ORDER BY total_compras DESC
        ''')
        
        clientes = cursor.fetchall()
        
        print("\nCLIENTES REGISTRADOS:")
        print("-" * 60)
        print(f"{'ID':<5} {'Nombre':<20} {'Telefono':<15} {'Compras':<15} {'Pedidos':<10}")
        print("-" * 60)
        
        for cli in clientes:
            print(f"{cli[0]:<5} {cli[1]:<20} {cli[2]:<15} ${cli[3]:<14,.0f} {cli[4]:<10}")
        
        print("-" * 60)
        print(f"Total clientes: {len(clientes)}")
        
        input("\nPresiona Enter para volver...")
    
    def ventas_por_metodo(self):
        self.limpiar_pantalla()
        cursor = self.conn.cursor()
        
        print("\n" + "=" * 55)
        print("   VENTAS POR METODO DE PAGO - HOY")
        print("=" * 55)
        
        cursor.execute('''
            SELECT metodo_pago, COUNT(*) as pedidos, SUM(total) as total
            FROM ventas
            WHERE date(fecha) = date('now')
            GROUP BY metodo_pago
            ORDER BY total DESC
        ''')
        
        metodos = cursor.fetchall()
        
        if metodos:
            print(f"\n{'Metodo':<20} {'Pedidos':<10} {'Total':<15}")
            print("-" * 45)
            
            total_general = 0
            for m in metodos:
                print(f"{m[0]:<20} {m[1]:<10} ${m[2]:<14,.0f}")
                total_general += m[2]
            
            print("-" * 45)
            print(f"{'TOTAL':<20} {'':<10} ${total_general:<14,.0f}")
        else:
            print("\nNo hay ventas registradas hoy")
        
        print("\n" + "=" * 55)
        input("\nPresiona Enter para volver...")

# Iniciar sistema
if __name__ == "__main__":
    sistema = MDKSistema()
    sistema.mostrar_menu()