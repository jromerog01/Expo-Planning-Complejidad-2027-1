# Genera img/path.svg: cómo Path parte el camino de S1 a S2 por la mitad en cada nivel (L, L/2, L/4, ...).
# Se dibuja un camino de 8 pasos (L = 8) con 9 estados; los puntos medios son:
#   L -> S' (posición 4);  L/2 -> posiciones 2 y 6;  L/4 -> posiciones 1, 3, 5 y 7.
# Uso: python3 generar-path.py ../../img
import sys

OUT = sys.argv[1]

PASOS = 8                      # pasos del camino dibujado
X_NODO = 110                   # centro horizontal de la columna de estados
Y0, DY = 140, 60               # y del primer estado y separación entre estados
ANCHO, ALTO = 104, 42          # tamaño de S1, S' y S2

# Un nivel por cada tamaño de tramo: (etiqueta, x de los corchetes, color, [(inicio, fin, punto medio), ...])
NIVELES = [
    ("L", 250, "#1b2430", [(0, 8, 4)]),
    ("L/2", 330, "#2f6fb5", [(0, 4, 2), (4, 8, 6)]),
    ("L/4", 410, "#8bb9ea", [(0, 2, 1), (2, 4, 3), (4, 6, 5), (6, 8, 7)]),
]


def y(i):
    return Y0 + DY * i


def fo(cx, cy, size, weight, tex, cls="fo", just="center", extra=""):
    h = round(size * 1.9, 1)
    x = {"center": cx - 260, "flex-start": cx, "flex-end": cx - 520}[just]
    return (f'<foreignObject x="{x:.1f}" y="{cy - h/2:.1f}" width="520" height="{h}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" '
            f'style="font-size:{size}px;font-weight:{weight};justify-content:{just};height:{h}px{extra}">{tex}</div></foreignObject>')


# A qué nivel pertenece cada estado como punto medio
nivel_de = {}
for etiqueta, _, _, segs in NIVELES:
    for _, _, m in segs:
        nivel_de[m] = etiqueta

# Radio vertical de cada estado (para que las flechas no lo toquen)
def radio(i):
    if i in (0, PASOS, PASOS // 2):
        return ALTO // 2
    return 11 if nivel_de.get(i) == "L/2" else 9


p = ['<svg xmlns="http://www.w3.org/2000/svg" class="ill" viewBox="0 0 520 736" role="img" '
     'aria-label="Path parte el camino de S1 a S2 por la mitad en cada nivel: L, L/2, L/4, hasta L = 1">']

# Encabezado: la llamada
p += ['<rect x="110" y="22" width="300" height="50" rx="16" fill="url(#g-ink)" filter="url(#ds)" />',
      fo(260, 47, 22, 700, "\\(\\textsf{Path}(S_1, S_2, L)\\)", "fo t-white")]

# Cabeceras de columna (una por nivel)
for etiqueta, x, _, _ in NIVELES:
    p.append(f'<rect class="glass" x="{x - 32}" y="84" width="64" height="28" rx="14" />')
    p.append(fo(x, 98, 16, 650, f"\\({etiqueta}\\)"))

# Guías tenues: de cada punto medio (estado) a su corchete
for _, x, _, segs in NIVELES:
    for _, _, m in segs:
        p.append(f'<path d="M{X_NODO + ANCHO // 2 + 6} {y(m)} H{x - 9}" fill="none" stroke="#ffffff" '
                 f'stroke-opacity=".8" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round" />')

# Corchetes de cada nivel y su punto medio
for _, x, color, segs in NIVELES:
    for a, b, m in segs:
        p.append(f'<path d="M{x - 7} {y(a) + 6} H{x} V{y(b) - 6} H{x - 7}" fill="none" stroke="{color}" '
                 f'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />')
        p.append(f'<circle cx="{x}" cy="{y(m)}" r="7" fill="{color}" stroke="#fff" stroke-width="2.5" />')

# Flechas entre estados consecutivos
for i in range(PASOS):
    p.append(f'<path class="edge" d="M{X_NODO} {y(i) + radio(i) + 3} V{y(i + 1) - radio(i + 1) - 4}" />')

# Estados
x0 = X_NODO - ANCHO // 2
for i in range(PASOS + 1):
    if i in (0, PASOS):                                   # S1 y S2
        p.append(f'<rect class="glass" x="{x0}" y="{y(i) - ALTO // 2}" width="{ANCHO}" height="{ALTO}" rx="13" stroke="#1b2430" stroke-width="2.5" />')
        p.append(fo(X_NODO, y(i), 19, 650, "\\(S_1\\)" if i == 0 else "\\(S_2\\)"))
    elif i == PASOS // 2:                                 # S'
        p.append(f'<rect x="{x0}" y="{y(i) - ALTO // 2}" width="{ANCHO}" height="{ALTO}" rx="13" fill="url(#g-ink)" filter="url(#ds)" />')
        p.append(fo(X_NODO, y(i), 19, 650, "\\(S'\\)", "fo t-white"))
    elif nivel_de.get(i) == "L/2":                        # puntos medios de las mitades
        p.append(f'<circle cx="{X_NODO}" cy="{y(i)}" r="11" fill="url(#g-blue)" stroke="#fff" stroke-width="2.5" />')
        p.append(fo(X_NODO - 20, y(i), 17, 650, "\\(S''\\)", "fo t-muted", "flex-end"))
    else:                                                 # puntos medios de los cuartos
        p.append(f'<circle cx="{X_NODO}" cy="{y(i)}" r="9" fill="#cfe3f7" stroke="#8bb9ea" stroke-width="2" />')

# Nota inferior
p += ['<rect class="glass" x="30" y="672" width="460" height="50" rx="16" />',
      fo(260, 697, 17, 600, "Cada tramo se parte igual, hasta \\(L = 1\\)"),
      '</svg>']

open(f"{OUT}/path.svg", "w").write("\n  ".join(p) + "\n")
print("ok")
