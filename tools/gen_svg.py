"""Generates blueprint-style axonometric SVG drawings used as image slots
until the client supplies real photography."""
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img')
os.makedirs(OUT, exist_ok=True)
C30, S30 = math.cos(math.radians(30)), 0.5

BG = {'blue': ('#10304F', '#163E64'), 'ink': ('#0B1A2B', '#12283F'), 'steel': ('#2B3E52', '#344A61')}
LINE = '#CFE0F0'
AMBER = '#F2A900'


class Draw:
    def __init__(self, w=1200, h=900, bg='blue', s=38, cx=None, cy=None):
        self.w, self.h, self.s = w, h, s
        self.cx = cx if cx is not None else w / 2
        self.cy = cy if cy is not None else h * 0.62
        self.bg = BG[bg]
        self.items = []

    def p(self, x, y, z):
        return (self.cx + (x - z) * C30 * self.s, self.cy + (x + z) * S30 * self.s - y * self.s)

    def poly(self, pts, fill, stroke=LINE, sw=1.6, op=1, dash=None):
        d = ' '.join(f'{a:.1f},{b:.1f}' for a, b in (self.p(*q) for q in pts))
        da = f' stroke-dasharray="{dash}"' if dash else ''
        self.items.append(f'<polygon points="{d}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{da}/>')

    def line(self, a, b, stroke=LINE, sw=1.4, dash=None, op=1):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        self.items.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{op}"{da}/>')

    def box(self, x, y, z, w, h, d, tone=('#2E5E8A', '#24507A', '#3B70A0'), stroke=LINE, op=1):
        x0, x1, z0, z1, y0, y1 = x, x + w, z, z + d, y, y + h
        self.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], tone[2], stroke, op=op)   # top
        self.poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], tone[0], stroke, op=op)   # front (z+)
        self.poly([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], tone[1], stroke, op=op)   # right (x+)

    def windows_front(self, x, y, z, w, h, cols, rows, pad=0.25, fill='#9EC3E6'):
        cw, rh = (w - pad * (cols + 1)) / cols, (h - pad * (rows + 1)) / rows
        for r in range(rows):
            for c in range(cols):
                x0 = x + pad + c * (cw + pad); y0 = y + pad + r * (rh + pad)
                self.poly([(x0, y0, z), (x0 + cw, y0, z), (x0 + cw, y0 + rh, z), (x0, y0 + rh, z)], fill, LINE, 1, op=.55)

    def windows_right(self, x, y, z, d, h, cols, rows, pad=0.25, fill='#7FA9CF'):
        cw, rh = (d - pad * (cols + 1)) / cols, (h - pad * (rows + 1)) / rows
        for r in range(rows):
            for c in range(cols):
                z0 = z + pad + c * (cw + pad); y0 = y + pad + r * (rh + pad)
                self.poly([(x, y0, z0), (x, y0, z0 + cw), (x, y0 + rh, z0 + cw), (x, y0 + rh, z0)], fill, LINE, 1, op=.5)

    def ground(self, size=14):
        for i in range(-size, size + 1, 2):
            self.line((i, 0, -size), (i, 0, size), op=.18, sw=1)
            self.line((-size, 0, i), (size, 0, i), op=.18, sw=1)

    def dim(self, a, b, label, off=(0, 0, 1.2)):
        a2 = tuple(a[i] + off[i] for i in range(3)); b2 = tuple(b[i] + off[i] for i in range(3))
        self.line(a, a2, AMBER, 1, op=.8); self.line(b, b2, AMBER, 1, op=.8)
        self.line(a2, b2, AMBER, 1.4)
        (mx, my) = self.p(*[(a2[i] + b2[i]) / 2 for i in range(3)])
        if label: self.items.append(f'<text x="{mx:.0f}" y="{my + 26:.0f}" fill="{AMBER}" font-family="Arial, sans-serif" font-size="20" font-weight="700" text-anchor="middle">{label}</text>')

    def svg(self, title):
        g0, g1 = self.bg
        grid = (f'<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">'
                f'<path d="M40 0H0V40" fill="none" stroke="{LINE}" stroke-opacity=".09"/></pattern>'
                f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g0}"/></linearGradient></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{title}">'
                f'<title>{title}</title>{grid}<rect width="100%" height="100%" fill="url(#bg)"/><rect width="100%" height="100%" fill="url(#g)"/>'
                + ''.join(self.items) + '</svg>')


def save(name, draw, title):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(draw.svg(title))


CONC = ('#B9C3CB', '#97A3AD', '#D3DBE1')
PLAST = ('#DCE3E8', '#B7C2CB', '#EEF2F5')
ROOF = ('#3B4752', '#2C3640', '#4A5764')
AMB = (AMBER, '#C98A00', '#FFC233')
TREE = ('#3E7A4F', '#2F6140', '#4F9461')


def house(variant='blue', scaffold=False, title='Residential construction drawing'):
    d = Draw(bg=variant, s=44, cy=600)
    d.ground()
    d.box(-5, 0, -3, 10, 0.4, 7, CONC)
    d.box(-4.6, 0.4, -2.6, 6, 2.8, 6, PLAST)
    d.windows_front(-4.6, 0.6, 3.4, 6, 2.4, 3, 1)
    d.box(1.4, 0.4, -2.6, 3.2, 5.6, 6, PLAST)
    d.windows_right(4.6, 0.6, -2.6, 6, 2.4, 2, 1)
    d.windows_right(4.6, 3.4, -2.6, 6, 2.4, 2, 1)
    d.windows_front(1.4, 3.4, 3.4, 3.2, 2.4, 1, 1)
    # flat roof slabs
    d.box(-5, 3.2, -3, 6.6, 0.3, 6.8, ROOF)
    d.box(1.1, 6.0, -3, 3.8, 0.3, 6.8, ROOF)
    d.box(-2.6, 0.4, 3.4, 2.2, 0.15, 1.6, AMB)
    for (x, z) in [(-6.5, 5), (6.2, 4.5), (6.5, -2)]:
        d.box(x, 0, z, 0.9, 1.2, 0.9, TREE)
    if scaffold:
        for i in range(6):
            x = -5 + i * 2
            d.line((x, 0, 4.2), (x, 6.6, 4.2), AMBER, 2)
        for j in range(5):
            y = j * 1.6
            d.line((-5, y, 4.2), (5, y, 4.2), AMBER, 2)
        d.line((-5, 0, 4.2), (5, 6.4, 4.2), AMBER, 1.2, op=.7)
    d.dim((-5, 0, 4), (5, 0, 4), None, off=(0, 0, 2.2))
    save(('renovation' if scaffold else 'residential') + f'-{variant}.svg', d, title)


def commercial(variant='blue', title='Commercial building drawing'):
    d = Draw(bg=variant, s=34, cy=690)
    d.ground(16)
    d.box(-6, 0, -4, 12, 0.5, 8, CONC)
    for f in range(5):
        y = 0.5 + f * 2.2
        tone = PLAST if f == 0 else ('#3D6E99', '#2F5C84', '#D3DBE1')
        d.box(-5.6, y, -3.6, 11.2, 2.0, 7.2, tone)
        if f:
            d.windows_front(-5.6, y, 3.6, 11.2, 2.0, 6, 1, 0.2, '#A9CBEA')
            d.windows_right(5.6, y, -3.6, 7.2, 2.0, 4, 1, 0.2, '#86AFD3')
        d.box(-6, y + 2.0, -4, 12, 0.2, 8, CONC)
    d.box(-2, 0.5, 3.6, 4, 0.2, 1.6, AMB)
    d.box(-3, 11.7, -1, 3, 1, 2.4, ROOF)
    d.dim((-6, 0, 4), (6, 0, 4), None, off=(0, 0, 2.4))
    save(f'commercial-{variant}.svg', d, title)


def industrial(variant='steel', title='Industrial warehouse drawing'):
    d = Draw(bg=variant, s=36, cy=620)
    d.ground(16)
    d.box(-8, 0, -4, 16, 0.4, 9, CONC)
    d.box(-7.6, 0.4, -3.6, 15.2, 4.0, 8.2, PLAST)
    for i in range(4):
        x = -7.6 + i * 3.8
        d.poly([(x, 4.4, -3.6), (x + 3.8, 4.4, -3.6), (x + 3.8, 4.4, 4.6), (x, 4.4, 4.6)], ROOF[2])
        d.poly([(x, 4.4, 4.6), (x + 3.8, 4.4, 4.6), (x + 3.8, 6.0, 4.6)], ROOF[0])
        d.poly([(x + 3.8, 4.4, -3.6), (x + 3.8, 4.4, 4.6), (x + 3.8, 6.0, 4.6), (x + 3.8, 6.0, -3.6)], '#9EC3E6', op=.5)
    for i in range(3):
        x = -6.4 + i * 4.8
        d.poly([(x, 0.4, 4.6), (x + 3, 0.4, 4.6), (x + 3, 3.4, 4.6), (x, 3.4, 4.6)], AMB[0], op=.9)
    save(f'industrial-{variant}.svg', d, title)


def civil(variant='ink', title='Civil works drawing'):
    d = Draw(bg=variant, s=36, cy=520)
    d.ground(16)
    # road
    d.poly([(-14, 0.01, -2), (14, 0.01, -2), (14, 0.01, 2), (-14, 0.01, 2)], '#38485A')
    for i in range(-13, 14, 3):
        d.poly([(i, 0.02, -0.1), (i + 1.5, 0.02, -0.1), (i + 1.5, 0.02, 0.1), (i, 0.02, 0.1)], '#F5F7F8', op=.9)
    # culvert / bridge deck crossing
    d.box(-2, 0, 2.6, 4, 0.8, 5, CONC)
    d.box(-2.4, 0.8, 2.4, 4.8, 0.3, 5.4, CONC)
    d.poly([(-1.2, 0, 7.6), (1.2, 0, 7.6), (1.2, 0.6, 7.6), (-1.2, 0.6, 7.6)], '#0B1A2B')
    # drain line
    d.box(-14, -0.0, 2.2, 12, 0.2, 0.4, CONC)
    d.box(2, 0, 2.2, 12, 0.2, 0.4, CONC)
    # barriers
    for i in range(-12, 13, 4):
        d.box(i, 0, -3, 1.2, 0.6, 0.5, AMB)
    d.dim((-2, 0, 8), (2, 0, 8), None, off=(0, 0, 1.4))
    save(f'civil-{variant}.svg', d, title)


def interior(variant='blue', title='Interior fit-out drawing'):
    d = Draw(bg=variant, s=50, cy=640)
    # floor + two walls (cutaway room)
    d.poly([(-5, 0, -4), (5, 0, -4), (5, 0, 4), (-5, 0, 4)], '#D3DBE1')
    for i in range(-5, 6):
        d.line((i, 0.01, -4), (i, 0.01, 4), '#97A3AD', 1, op=.6)
    d.poly([(-5, 0, -4), (5, 0, -4), (5, 5, -4), (-5, 5, -4)], '#EEF2F5')
    d.poly([(-5, 0, -4), (-5, 0, 4), (-5, 5, 4), (-5, 5, -4)], '#DCE3E8')
    d.poly([(0, 1.2, -4), (3.6, 1.2, -4), (3.6, 4, -4), (0, 4, -4)], '#9EC3E6', op=.8)
    d.box(-4.6, 0, -3.6, 4, 0.9, 1.4, ROOF)           # counter
    d.box(-4.6, 0.9, -3.6, 4, 0.1, 1.4, AMB)
    d.box(0.5, 0, 0, 3, 0.75, 1.8, ('#7C5A3A', '#664A30', '#8E6A47'))  # table
    d.box(-4.6, 2.6, -3.9, 4, 1, 0.3, PLAST)
    save(f'interior-{variant}.svg', d, title)


def person(name='team-placeholder.svg'):
    w, h = 800, 1000
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Team member photo placeholder">'
           f'<title>Team member photo placeholder</title><rect width="100%" height="100%" fill="#E5E8E6"/>'
           f'<circle cx="400" cy="380" r="150" fill="#C3CBCF"/><path d="M130 1000c20-250 140-380 270-380s250 130 270 380z" fill="#C3CBCF"/>'
           f'<path d="M250 330c0-90 70-150 150-150s150 60 150 150c-60-30-240-30-300 0z" fill="{AMBER}"/>'
           f'<rect x="240" y="320" width="320" height="26" rx="4" fill="#C98A00"/></svg>')
    open(os.path.join(OUT, name), 'w').write(svg)


def og():
    d = Draw(1200, 630, 'blue', s=26, cx=820, cy=470)
    d.ground(12)
    for f in range(4):
        y = 0.4 + f * 1.8
        d.box(-4, y, -3, 8, 1.6, 6, PLAST if f == 0 else ('#3D6E99', '#2F5C84', '#D3DBE1'))
        d.box(-4.3, y + 1.6, -3.3, 8.6, 0.2, 6.6, CONC)
    d.items.append('<text x="70" y="270" fill="#fff" font-family="Arial Black, Arial, sans-serif" font-size="72" font-weight="900">R.B.N.</text>'
                   '<text x="70" y="350" fill="#fff" font-family="Arial Black, Arial, sans-serif" font-size="56" font-weight="900">Construction</text>'
                   f'<rect x="70" y="380" width="120" height="8" fill="{AMBER}"/>'
                   '<text x="70" y="440" fill="#C3D3E2" font-family="Arial, sans-serif" font-size="28">Polonnaruwa, Sri Lanka</text>')
    save('og-image.svg', d, 'R.B.N. Construction')


house('blue'); house('ink'); house('steel', scaffold=True, title='Renovation works drawing'); house('blue', scaffold=True, title='Renovation works drawing')
commercial('blue'); commercial('ink'); commercial('steel')
industrial('steel'); industrial('ink')
civil('ink'); civil('blue')
interior('blue'); interior('steel')
person(); og()
print(sorted(os.listdir(OUT)))
