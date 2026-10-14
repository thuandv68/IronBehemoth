"""Render episode graphics from a spec file.
Usage: python3 ib_gfx.py <EP>        (reads <EP>/build/gfx.txt, writes PNGs to <EP>/gfx/)
Spec lines (fields split by |, # = comment):
  title|<name>|INSIDE THE|STURMTIGER|38 CM RW 61 · "STORM TIGER"     -> <name>.png   (centered title overlay)
  chapter|<name>|01|THE GUN                                             -> chapter_<name>.png
  ov|<name>|≈ 345 KG|ONE ROUND · AS HEAVY AS FIVE GROWN MEN              -> ov_<name>.png  (number overlay, lower left)
  lt|<name>|LINE ONE|LINE TWO                                           -> lt_<name>.png  (lower third with dark box)
  card|<name>|18|STURMTIGERS EVER BUILT                                 -> card_<name>.png (full-frame dark card)
  q|<name>|QUESTION ONE|QUESTION TWO|QUESTION THREE                     -> <name>1..3.png (cumulative question list)
All text must be English (on-screen). Overlays are transparent PNGs 1920x1080."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
EP = os.path.abspath(sys.argv[1]); C = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'common', 'fonts')
G = os.path.join(EP, 'gfx'); os.makedirs(G, exist_ok=True)
W, H = 1920, 1080
BG = (11, 11, 12); OR = (224, 102, 43); IV = (237, 230, 214)
def font(n, s, w=None):
    f = ImageFont.truetype(os.path.join(C, n), s)
    if w:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
BEB = lambda s: font('BebasNeue.ttf', s); OSW = lambda s, w=500: font('Oswald.ttf', s, w)
def blank(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def box(img, xy, a):
    sh = blank(); ImageDraw.Draw(sh).rectangle(xy, fill=(0, 0, 0, a)); return Image.alpha_composite(img, sh)
def grid(d):
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(18, 19, 21))
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(18, 19, 21))

def title(name, l1, l2, l3=''):
    img = box(blank(), [0, H//2-230, W, H//2+250], 110); d = ImageDraw.Draw(img)
    d.text((W//2, H//2-120), l1, font=OSW(54, 400), fill=IV+(255,), anchor='mm')
    d.text((W//2, H//2+50), l2, font=BEB(220), fill=IV+(255,), anchor='mm')
    d.rectangle([W//2-140, H//2+165, W//2+140, H//2+171], fill=OR+(255,))
    if l3: d.text((W//2, H//2+210), l3, font=OSW(34, 500), fill=OR+(255,), anchor='mm')
    img.save(f'{G}/{name}.png')
def chapter(name, num, t):
    d0 = ImageDraw.Draw(blank()); tw = d0.textbbox((0, 0), t, font=BEB(120))[2]
    img = box(blank(), [80, H//2-110, 230+tw+60, H//2+50], 140); d = ImageDraw.Draw(img)
    d.text((110, H//2-30), num, font=BEB(90), fill=OR+(255,), anchor='lm')
    d.text((230, H//2-30), t, font=BEB(120), fill=IV+(255,), anchor='lm')
    img.save(f'{G}/chapter_{name}.png')
def ov(name, big, small):
    x, y = 110, H-250; d0 = ImageDraw.Draw(blank())
    pw = max(d0.textbbox((0, 0), big, font=BEB(120))[2], d0.textbbox((0, 0), small, font=OSW(34, 500))[2]) + 80
    img = box(blank(), [x-40, y-30, x-40+pw, y+175], 150); d = ImageDraw.Draw(img)
    d.rectangle([x-40, y-30, x-30, y+175], fill=OR+(255,))
    d.text((x, y-10), big, font=BEB(120), fill=IV+(255,)); d.text((x, y+118), small, font=OSW(34, 500), fill=OR+(255,))
    img.save(f'{G}/ov_{name}.png')
def lt(name, l1, l2):
    d0 = ImageDraw.Draw(blank())
    w = max(d0.textbbox((0, 0), l1, font=OSW(40, 600))[2], d0.textbbox((0, 0), l2, font=OSW(30, 400))[2])
    img = box(blank(), [96, H-205, 140+w+40, H-85], 165); d = ImageDraw.Draw(img)
    d.rectangle([110, H-190, 116, H-100], fill=OR+(255,))
    d.text((140, H-185), l1, font=OSW(40, 600), fill=IV+(255,)); d.text((140, H-135), l2, font=OSW(30, 400), fill=(200, 196, 186, 255))
    img.save(f'{G}/lt_{name}.png')
def card(name, big, small):
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img); grid(d)
    sz = 420 if len(big) <= 4 else (260 if len(big) <= 8 else 170)
    d.text((W//2, H//2-60), big, font=BEB(sz), fill=OR, anchor='mm')
    d.text((W//2, H//2+170), small, font=OSW(48, 500), fill=IV, anchor='mm')
    img.save(f'{G}/card_{name}.png')
def qlist(name, *Q):
    for k in range(1, len(Q)+1):
        img = box(blank(), [90, 250, 1500, 250+len(Q)*190], 150); d = ImageDraw.Draw(img)
        for i in range(k):
            y = 300+i*190
            d.text((140, y), f'0{i+1}', font=BEB(110), fill=OR+(255,)); d.text((290, y+10), Q[i], font=BEB(100), fill=IV+(255,))
        img.save(f'{G}/{name}{k}.png')

F = {'title': title, 'chapter': chapter, 'ov': ov, 'lt': lt, 'card': card, 'q': qlist}
n = 0
for ln in open(os.path.join(EP, 'build', 'gfx.txt'), encoding='utf-8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'): continue
    p = [x.strip() for x in ln.split('|')]
    F[p[0]](*p[1:]); n += 1
print('gfx specs', n, '->', G, sorted(f for f in os.listdir(G) if f.endswith('.png')))
