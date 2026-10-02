"""Generates the FD Tracker launcher icons into the Android res folder.
Usage: python make_icons.py [path/to/res]"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

BASE = sys.argv[1] if len(sys.argv) > 1 else 'android/app/src/main/res'
S = 1024
C1, C2 = (79, 70, 229), (124, 58, 237)  # indigo -> violet

def font(size):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
              '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',
              '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf']:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gradient(size):
    g = Image.new('RGB', (256, 256)); px = g.load()
    for y in range(256):
        for x in range(256):
            t = (x + y) / 510
            px[x, y] = tuple(int(C1[i] + (C2[i] - C1[i]) * t) for i in range(3))
    return g.resize((size, size), Image.BICUBIC)

def art():
    k = 2; W = S * k
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R = lambda *v: [x * k for x in v]
    d.rounded_rectangle(R(178, 218, 688, 793), radius=70 * k, fill=(30, 27, 75, 70))
    d.rounded_rectangle(R(165, 195, 675, 770), radius=70 * k, fill=(255, 255, 255, 255))
    d.text((420 * k, 360 * k), 'FD', font=font(230 * k), fill=(79, 70, 229, 255), anchor='mm')
    d.rounded_rectangle(R(250, 545, 560, 585), radius=20 * k, fill=(199, 210, 254, 255))
    d.rounded_rectangle(R(250, 625, 470, 665), radius=20 * k, fill=(199, 210, 254, 255))
    cx, cy, r = 680, 690, 215
    d.ellipse(R(cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), fill=(255, 255, 255, 255))
    d.ellipse(R(cx - r, cy - r, cx + r, cy + r), fill=(245, 158, 11, 255))
    d.ellipse(R(cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26), fill=(252, 211, 77, 255))
    d.text((cx * k, (cy + 6) * k), '\u20b9', font=font(260 * k), fill=(146, 64, 14, 255), anchor='mm')
    return im.resize((S, S), Image.LANCZOS)

def fit(a, frac):
    bb = a.getbbox(); a = a.crop(bb)
    sc = frac * S / max(a.size)
    a = a.resize((round(a.width * sc), round(a.height * sc)), Image.LANCZOS)
    c = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    c.paste(a, ((S - a.width) // 2, (S - a.height) // 2), a)
    return c

def mask(shape):
    m = Image.new('L', (S * 2, S * 2), 0); d = ImageDraw.Draw(m)
    if shape == 'round': d.ellipse([0, 0, S * 2 - 1, S * 2 - 1], fill=255)
    else: d.rounded_rectangle([0, 0, S * 2 - 1, S * 2 - 1], radius=int(S * 2 * 0.22), fill=255)
    return m.resize((S, S), Image.LANCZOS)

a = art()
bg = gradient(S).convert('RGBA')
def icon(shape):
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask(shape))
    out.alpha_composite(fit(a, 0.66))
    return out
legacy, rnd, fg = icon('square'), icon('round'), fit(a, 0.54)

dens = {'mdpi': (48, 108), 'hdpi': (72, 162), 'xhdpi': (96, 216), 'xxhdpi': (144, 324), 'xxxhdpi': (192, 432)}
for n, (li, fi) in dens.items():
    d = os.path.join(BASE, 'mipmap-' + n); os.makedirs(d, exist_ok=True)
    legacy.resize((li, li), Image.LANCZOS).save(os.path.join(d, 'ic_launcher.png'))
    rnd.resize((li, li), Image.LANCZOS).save(os.path.join(d, 'ic_launcher_round.png'))
    fg.resize((fi, fi), Image.LANCZOS).save(os.path.join(d, 'ic_launcher_foreground.png'))
v = os.path.join(BASE, 'values'); os.makedirs(v, exist_ok=True)
open(os.path.join(v, 'ic_launcher_background.xml'), 'w').write(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#4F46E5</color>\n</resources>\n')
legacy.resize((512, 512), Image.LANCZOS).save(os.path.join(BASE, 'preview_icon.png'))
print('icons written to', BASE)
