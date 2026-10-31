"""Génère le QR code orange Buena Onda à partir de l'URL GitHub Pages.

Usage :  python make_qr.py https://TON-PSEUDO.github.io/buena-onda-wifi/
Prérequis : pip install "qrcode[pil]"
"""
import sys
import qrcode
from qrcode.constants import ERROR_CORRECT_H

if len(sys.argv) != 2:
    sys.exit("Usage : python make_qr.py <url>")

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=24, border=4)
qr.add_data(sys.argv[1])
qr.make(fit=True)
# Orange foncé sur fond crème : reste très contrasté, donc facile à scanner
img = qr.make_image(fill_color="#c24a00", back_color="#fff3e0")
img.save("qr-buena-onda.png")
print("QR code enregistré : qr-buena-onda.png")
