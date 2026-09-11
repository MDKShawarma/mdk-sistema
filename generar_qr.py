import qrcode

# URL de tu sistema
url = "https://mdk-sistema.onrender.com/pedido"

# Crear el QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Crear la imagen
img = qr.make_image(fill_color="black", back_color="white")

# Guardar
img.save("QR_MDK_Pedidos.png")

print("✅ QR generado correctamente")
print(f"URL: {url}")
print("Archivo: QR_MDK_Pedidos.png")