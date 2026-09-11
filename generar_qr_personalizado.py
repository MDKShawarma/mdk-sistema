from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

# URL de tu sistema
url = "https://mdk-sistema.onrender.com/pedido"

# Verificar que existe el logo
logo_path = "logo_mdk.png"
if not os.path.exists(logo_path):
    print(f"❌ ERROR: No se encuentra el archivo {logo_path}")
    exit()

# ============================
# 1. CREAR EL QR
# ============================
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,
    border=2,
)
qr.add_data(url)
qr.make(fit=True)

# Colores: dorado sobre negro
qr_img = qr.make_image(fill_color="#d4a017", back_color="#000000").convert("RGB")

# ============================
# 2. AGREGAR LOGO EN EL CENTRO
# ============================
logo = Image.open(logo_path).convert("RGB")

# Redimensionar el logo (30% del tamaño del QR, más grande)
qr_width, qr_height = qr_img.size
logo_size = int(qr_width * 0.30)
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Posición centrada
pos_x = (qr_width - logo_size) // 2
pos_y = (qr_height - logo_size) // 2

# Pegar el logo directamente (sin círculo)
qr_img.paste(logo, (pos_x, pos_y))

# ============================
# 3. CREAR IMAGEN FINAL CON CARTELES
# ============================
ancho_final = qr_width + 100
alto_final = qr_height + 300

imagen_final = Image.new("RGB", (ancho_final, alto_final), "#000000")
draw = ImageDraw.Draw(imagen_final)

# Cargar fuentes
try:
    fuente_titulo = ImageFont.truetype("arialbd.ttf", 55)
    fuente_subtitulo = ImageFont.truetype("arial.ttf", 32)
    fuente_instruccion = ImageFont.truetype("arialbd.ttf", 38)
except:
    fuente_titulo = ImageFont.load_default()
    fuente_subtitulo = ImageFont.load_default()
    fuente_instruccion = ImageFont.load_default()

# Título arriba: MDK SHAWARMA
titulo = "MDK SHAWARMA"
bbox_titulo = draw.textbbox((0, 0), titulo, font=fuente_titulo)
ancho_titulo = bbox_titulo[2] - bbox_titulo[0]
draw.text(((ancho_final - ancho_titulo) // 2, 30), titulo, fill="#d4a017", font=fuente_titulo)

# Subtítulo: Maison du Kebab
subtitulo = "Maison du Kebab"
bbox_sub = draw.textbbox((0, 0), subtitulo, font=fuente_subtitulo)
ancho_sub = bbox_sub[2] - bbox_sub[0]
draw.text(((ancho_final - ancho_sub) // 2, 95), subtitulo, fill="#d4a017", font=fuente_subtitulo)

# Pegar el QR en el centro
pos_qr_x = (ancho_final - qr_width) // 2
pos_qr_y = 150
imagen_final.paste(qr_img, (pos_qr_x, pos_qr_y))

# Cartel abajo
cartel = "ESCANEÁ PARA PEDIR"
bbox_cartel = draw.textbbox((0, 0), cartel, font=fuente_instruccion)
ancho_cartel = bbox_cartel[2] - bbox_cartel[0]
y_cartel = pos_qr_y + qr_height + 30
draw.text(((ancho_final - ancho_cartel) // 2, y_cartel), cartel, fill="#d4a017", font=fuente_instruccion)

# ============================
# 4. GUARDAR
# ============================
nombre_archivo = "QR_MDK_Personalizado.png"
imagen_final.save(nombre_archivo)

print("✅ QR personalizado generado correctamente")
print(f"Archivo: {nombre_archivo}")
print(f"URL: {url}")
print(f"Tamaño: {imagen_final.size}")