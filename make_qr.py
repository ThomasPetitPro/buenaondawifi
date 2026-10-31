"""Génère le QR code Buena Onda + une affichette Halloween prête à imprimer.

Usage :  python make_qr.py [url]
         (par défaut : https://thomaspetitpro.github.io/buenaondawifi/)
Prérequis : pip install "qrcode[pil]"

Fichiers produits :
  qr-buena-onda.png          QR code seul
  affichette-buena-onda.png  affichette A6 (105 x 148 mm, 300 dpi)
  affichettes-A4.pdf         4 affichettes A6 sur une page A4, à découper
"""
import math
import random
import sys
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from qrcode.constants import ERROR_CORRECT_H

URL = sys.argv[1] if len(sys.argv) > 1 else "https://thomaspetitpro.github.io/buenaondawifi/"
HERE = Path(__file__).parent
LOGO = HERE / "logo-buena-onda.png"

# Couleurs du logo + Halloween
BROWN = (99, 38, 38)      # #632626 (texte du logo)
SUN = (249, 182, 26)      # #f9b61a (soleil)
RUST = (153, 40, 0)       # #992800
ORANGE = (255, 106, 0)
CREAM = (255, 243, 224)
NIGHT = (20, 8, 10)
NIGHT2 = (52, 18, 22)

DPI = 300
W, H = 1240, 1748  # A6 à 300 dpi


def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


TITLE = lambda s: font(["/System/Library/Fonts/Supplemental/Rockwell.ttc", "DejaVuSerif-Bold.ttf"], s)
TEXT = lambda s: font(["/System/Library/Fonts/Avenir Next.ttc", "DejaVuSans.ttf"], s)


def make_qr():
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=24, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    # Brun foncé du logo sur crème : très contrasté, donc facile à scanner
    return qr.make_image(fill_color=BROWN, back_color=CREAM).convert("RGB")


def bat(draw, cx, cy, s, color):
    """Silhouette de chauve-souris centrée en (cx, cy), envergure ~ 2*s."""
    pts = [(-1.0, -0.45), (-0.7, -0.5), (-0.4, -0.3), (-0.2, -0.2), (-0.12, -0.42),
           (-0.06, -0.25), (0.06, -0.25), (0.12, -0.42), (0.2, -0.2), (0.4, -0.3),
           (0.7, -0.5), (1.0, -0.45), (0.85, -0.15), (0.78, 0.15), (0.6, 0.02),
           (0.45, 0.25), (0.28, 0.08), (0.12, 0.2), (0, 0.4), (-0.12, 0.2),
           (-0.28, 0.08), (-0.45, 0.25), (-0.6, 0.02), (-0.78, 0.15), (-0.85, -0.15)]
    draw.polygon([(cx + x * s, cy + y * s) for x, y in pts], fill=color)


def pumpkin(draw, cx, cy, r):
    for dx in (-0.55, 0.55, -0.25, 0.25, 0):
        draw.ellipse([cx + dx * r - 0.55 * r, cy - 0.8 * r, cx + dx * r + 0.55 * r, cy + 0.8 * r],
                     fill=ORANGE if dx else (255, 130, 20), outline=RUST, width=max(2, r // 18))
    draw.rounded_rectangle([cx - 0.12 * r, cy - 1.1 * r, cx + 0.12 * r, cy - 0.7 * r],
                           radius=r // 10, fill=(70, 110, 30))
    eye = lambda x: draw.polygon([(cx + x * r - 0.2 * r, cy - 0.1 * r),
                                  (cx + x * r + 0.2 * r, cy - 0.1 * r),
                                  (cx + x * r, cy - 0.4 * r)], fill=SUN)
    eye(-0.35)
    eye(0.35)
    draw.chord([cx - 0.5 * r, cy - 0.15 * r, cx + 0.5 * r, cy + 0.55 * r], 0, 180, fill=SUN)


def centered(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)


def make_poster(qr_img):
    # Fond nuit avec lueur orange en haut et en bas
    img = Image.new("RGB", (W, H), NIGHT)
    px = img.load()
    for y in range(H):
        t = y / H
        base = tuple(int(NIGHT2[i] * (1 - t) + NIGHT[i] * t) for i in range(3))
        for x in range(W):
            g = max(0.0, 1 - math.hypot((x - W / 2) / (W * 0.75), (y - H * 0.18) / (H * 0.45)))
            g2 = max(0.0, 1 - math.hypot((x - W / 2) / (W * 0.8), (y - H * 1.05) / (H * 0.3)))
            k = 0.55 * g ** 1.5 + 0.45 * g2 ** 1.5
            px[x, y] = tuple(int(base[i] + (ORANGE[i] - base[i]) * k) for i in range(3))

    d = ImageDraw.Draw(img)
    rnd = random.Random(31)

    # Étoiles + lune
    for _ in range(90):
        x, y = rnd.randrange(W), rnd.randrange(int(H * 0.95))
        if 230 < x < W - 230 and 40 < y < H - 60:
            continue  # pas d'étoiles derrière le contenu
        r = rnd.choice((1, 1, 2, 3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 230, 190))
    moon = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(moon)
    md.ellipse([W - 250, 70, W - 90, 230], fill=255)
    md.ellipse([W - 215, 55, W - 60, 210], fill=0)  # croissant
    img.paste(Image.new("RGB", (W, H), (255, 236, 190)), (0, 0), moon)

    # Chauves-souris
    for cx, cy, s in [(150, 120, 70), (300, 230, 40), (1000, 330, 55), (110, 560, 45),
                      (1130, 640, 38), (220, 1290, 42), (1060, 1240, 60)]:
        bat(d, cx, cy, s, (10, 3, 5))

    # Médaillon crème + logo
    medal_c, medal_r = (W // 2, 330), 260
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([medal_c[0] - medal_r - 20, medal_c[1] - medal_r - 20,
                                  medal_c[0] + medal_r + 20, medal_c[1] + medal_r + 20], fill=200)
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.paste(Image.new("RGB", (W, H), ORANGE), (0, 0), glow)
    d = ImageDraw.Draw(img)
    d.ellipse([medal_c[0] - medal_r, medal_c[1] - medal_r, medal_c[0] + medal_r, medal_c[1] + medal_r],
              fill=CREAM, outline=ORANGE, width=10)
    logo = Image.open(LOGO).convert("RGBA")
    lw = int(medal_r * 1.42)
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    img.paste(logo, (medal_c[0] - logo.width // 2, medal_c[1] - logo.height // 2), logo)

    # Titres
    centered(d, 625, "WI-FI GRATUIT", TITLE(96), SUN)
    centered(d, 745, "Scanne-moi pour te connecter", TEXT(46), CREAM)

    # QR code sur carte crème
    qs = 600
    qr = qr_img.resize((qs, qs), Image.NEAREST)
    qx, qy = (W - qs) // 2, 850
    pad = 18
    d.rounded_rectangle([qx - pad - 10, qy - pad - 10, qx + qs + pad + 10, qy + qs + pad + 10],
                        radius=48, fill=ORANGE)
    d.rounded_rectangle([qx - pad, qy - pad, qx + qs + pad, qy + qs + pad], radius=40, fill=CREAM)
    img.paste(qr, (qx, qy))

    # Citrouilles de part et d'autre
    pumpkin(d, 150, 1560, 85)
    pumpkin(d, W - 150, 1560, 85)

    centered(d, 1535, "Happy Halloween !", TITLE(64), ORANGE)
    centered(d, 1625, "34 rue Saint-Sébastien · Lille", TEXT(34), (255, 220, 180))
    return img


def main():
    qr = make_qr()
    qr.save(HERE / "qr-buena-onda.png")
    poster = make_poster(qr)
    poster.save(HERE / "affichette-buena-onda.png", dpi=(DPI, DPI))

    # Planche A4 (2480 x 3508 à 300 dpi) avec 4 affichettes A6
    sheet = Image.new("RGB", (2480, 3508), "white")
    for i in range(4):
        sheet.paste(poster, (i % 2 * W, i // 2 * H))
    sheet.save(HERE / "affichettes-A4.pdf", resolution=DPI)
    print(f"URL : {URL}")
    print("OK : qr-buena-onda.png, affichette-buena-onda.png, affichettes-A4.pdf")


if __name__ == "__main__":
    main()
