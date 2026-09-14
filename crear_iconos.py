"""
Script para crear íconos cuadrados para la PWA
Toma el logo.png rectangular y crea icon-192.png y icon-512.png cuadrados
"""

from PIL import Image

def crear_icono_cuadrado(ruta_logo, ruta_salida, tamano, color_fondo=(26, 26, 26)):
    """
    Crea un ícono cuadrado con el logo centrado y fondo del color elegido
    
    Args:
        ruta_logo: Ruta del logo original
        ruta_salida: Ruta donde guardar el ícono
        tamano: Tamaño del ícono (192 o 512)
        color_fondo: Color RGB del fondo (default: #1a1a1a negro MDK)
    """
    
    # Abrir el logo
    logo = Image.open(ruta_logo).convert('RGBA')
    
    # Calcular proporciones
    ancho_logo, alto_logo = logo.size
    proporcion = ancho_logo / alto_logo
    
    # Calcular tamaño del logo dentro del cuadrado
    # Dejamos un 10% de margen alrededor
    margen = 0.10
    tamano_util = int(tamano * (1 - margen * 2))
    
    if proporcion > 1:
        # Logo horizontal
        nuevo_ancho = tamano_util
        nuevo_alto = int(tamano_util / proporcion)
    else:
        # Logo vertical o cuadrado
        nuevo_alto = tamano_util
        nuevo_ancho = int(tamano_util * proporcion)
    
    # Redimensionar el logo
    logo_redimensionado = logo.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    
    # Crear el lienzo cuadrado con el color de fondo
    icono = Image.new('RGBA', (tamano, tamano), color_fondo + (255,))
    
    # Calcular posición para centrar el logo
    pos_x = (tamano - nuevo_ancho) // 2
    pos_y = (tamano - nuevo_alto) // 2
    
    # Pegar el logo en el centro
    icono.paste(logo_redimensionado, (pos_x, pos_y), logo_redimensionado)
    
    # Guardar el ícono
    icono.save(ruta_salida, 'PNG')
    print(f"✅ Creado: {ruta_salida} ({tamano}x{tamano})")


if __name__ == '__main__':
    print("🎨 Creando íconos para la PWA de MDK...")
    print("=" * 50)
    
    # Crear ícono 192x192
    crear_icono_cuadrado(
        'static/logo.png',
        'static/icon-192.png',
        192,
        color_fondo=(26, 26, 26)  # #1a1a1a (negro MDK)
    )
    
    # Crear ícono 512x512
    crear_icono_cuadrado(
        'static/logo.png',
        'static/icon-512.png',
        512,
        color_fondo=(26, 26, 26)  # #1a1a1a (negro MDK)
    )
    
    print("=" * 50)
    print("🎉 ¡Íconos creados correctamente!")
    print("📁 Archivos en: static/")