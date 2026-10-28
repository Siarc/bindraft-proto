#!/usr/bin/env python3
"""Generates share image, logo and favicons. Run: python3 _src/assets.py"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "_src", "fonts")
PAPER, INK, COPPER, GREY, RULE = "#F2F0EB", "#0E0D0C", "#B5652B", "#625E57", "#CFCAC0"
A = os.path.join(ROOT, "assets"); os.makedirs(A, exist_ok=True)

def font(name, size): return ImageFont.truetype(os.path.join(F, name), size)

# OG 1200x630
W, H = 1200, 630
im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
pad = 72
mono = font("geistmono.ttf", 22)
d.text((pad, pad - 6), "SOFTWARE STUDIO · UTTARA, DHAKA", font=mono, fill=GREY)
d.text((W - pad, pad - 6), "WEB · MOBILE · AI AGENTS", font=mono, fill=GREY, anchor="ra")
wm = font("geist600.ttf", 188)
d.text((pad - 8, 150), "BindRaft", font=wm, fill=INK)
x1 = d.textbbox((pad - 8, 150), "BindRaft", font=wm)[2]
by = d.textbbox((pad - 8, 150), "BindRaft", font=wm)[3]
d.rectangle([x1 + 10, by - 34, x1 + 40, by - 4], fill=COPPER)
d.line([(pad, 440), (W - pad, 440)], fill=INK, width=2)
t = font("geist500.ttf", 44)
d.text((pad, 470), "We build the software", font=t, fill=INK)
x2 = d.textbbox((pad, 470), "We build the software ", font=t)[2]
d.text((x2, 470), "businesses run on.", font=t, fill=GREY)
d.text((pad, 548), "bindraft.com", font=mono, fill=COPPER)
im.save(os.path.join(A, "og.png"), optimize=True)

# Logo / icons: ink square, copper block
def icon(size):
    i = Image.new("RGB", (size, size), INK); g = ImageDraw.Draw(i)
    s = size / 32
    g.rectangle([20 * s, 20 * s, 26 * s - 1, 26 * s - 1], fill=COPPER)
    return i
icon(180).save(os.path.join(ROOT, "apple-touch-icon.png"))
icon(512).save(os.path.join(A, "logo.png"))
icon(64).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
open(os.path.join(ROOT, "favicon.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#0E0D0C"/>'
    '<rect x="20" y="20" width="6" height="6" fill="#B5652B"/></svg>\n')
print("assets written")
