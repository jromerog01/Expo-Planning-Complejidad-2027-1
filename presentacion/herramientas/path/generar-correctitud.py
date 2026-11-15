# Genera img/correctitud.svg: el paso inductivo de la correctitud de Path con números concretos.
# Path(S1, S2, 8) y un camino real de 6 pasos: se corta por la mitad en S' (3 + 3 pasos)
# y cada tramo cabe en ceil(8/2) = 4. Al revés, dos tramos de a lo más 4 se pegan en un camino de a lo más 8.
# Uso: python3 generar-correctitud.py ../../img
import sys

OUT = sys.argv[1]

X_NODO = 110                   # centro horizontal de la columna de estados
ANCHO, ALTO = 104, 42          # tamaño de S1, S' y S2
Y_S1, Y_MEDIO, Y_S2 = 150, 392, 634
X_CAMINO, X_TRAMOS = 250, 360  # x de los corchetes (camino completo / tramos)
# Estados intermedios sin nombre (cada uno es un paso del camino)
INTERMEDIOS = [(230, "pre"), (312, "pre"), (472, "post"), (554, "post")]


def fo(cx, cy, size, weight, tex, cls="fo", just="center", extra=""):
    h = round(size * 1.9, 1)
    x = {"center": cx - 260, "flex-start": cx, "flex-end": cx - 520}[just]
    return (f'<foreignObject x="{x:.1f}" y="{cy - h/2:.1f}" width="520" height="{h}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" '
            f'style="font-size:{size}px;font-weight:{weight};justify-content:{just};height:{h}px{extra}">{tex}</div></foreignObject>')


def corchete(x, y_arriba, y_abajo, color):
    return (f'<path d="M{x - 7} {y_arriba + 6} H{x} V{y_abajo - 6} H{x - 7}" fill="none" stroke="{color}" '
            f'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />')


p = ['<svg xmlns="http://www.w3.org/2000/svg" class="ill" viewBox="0 0 520 736" role="img" '
     'aria-label="Un camino de S1 a S2 de a lo más L pasos se parte en el estado S prima: cada tramo mide a lo más la mitad de L">']

# Encabezado: la llamada
p += ['<rect x="110" y="22" width="300" height="50" rx="16" fill="url(#g-ink)" filter="url(#ds)" />',
      fo(260, 47, 22, 700, "\\(\\textsf{Path}(S_1, S_2, 8)\\)", "fo t-white")]

# Cabeceras de columna
p += [f'<rect class="glass" x="{X_CAMINO - 46}" y="84" width="92" height="28" rx="14" />',
      fo(X_CAMINO, 98, 16, 650, "\\(6 \\le 8\\)"),
      f'<rect class="glass" x="{X_TRAMOS - 34}" y="84" width="68" height="28" rx="14" />',
      fo(X_TRAMOS, 98, 16, 650, "\\(\\le 4\\)")]

# Guía del punto medio hacia el corchete del camino completo
p.append(f'<path d="M{X_NODO + ANCHO // 2 + 6} {Y_MEDIO} H{X_CAMINO - 9}" fill="none" stroke="#ffffff" '
         f'stroke-opacity=".8" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round" />')

# Corchetes: camino completo y sus dos tramos
p.append(corchete(X_CAMINO, Y_S1, Y_S2, "#1b2430"))
p.append(f'<circle cx="{X_CAMINO}" cy="{Y_MEDIO}" r="7" fill="#1b2430" stroke="#fff" stroke-width="2.5" />')
for a, b in [(Y_S1, Y_MEDIO), (Y_MEDIO, Y_S2)]:
    p.append(corchete(X_TRAMOS, a, b, "#2f6fb5"))
    cy = (a + b) / 2
    p.append(f'<rect class="glass" x="{X_TRAMOS + 36}" y="{cy - 17:.1f}" width="84" height="34" rx="12" />')
    p.append(fo(X_TRAMOS + 78, cy, 17, 650, "\\(3 \\le 4\\)"))

# Flechas entre estados consecutivos (S1, intermedios, S', intermedios, S2)
secuencia = [(Y_S1, ALTO // 2)] + [(y, 9) for y, lado in INTERMEDIOS if lado == "pre"] + [(Y_MEDIO, ALTO // 2)] \
          + [(y, 9) for y, lado in INTERMEDIOS if lado == "post"] + [(Y_S2, ALTO // 2)]
for (y1, r1), (y2, r2) in zip(secuencia, secuencia[1:]):
    p.append(f'<path class="edge" d="M{X_NODO} {y1 + r1 + 3} V{y2 - r2 - 4}" />')

# Estados intermedios
for y, _ in INTERMEDIOS:
    p.append(f'<circle cx="{X_NODO}" cy="{y}" r="9" fill="#cfe3f7" stroke="#8bb9ea" stroke-width="2" />')

# S1, S' y S2
x0 = X_NODO - ANCHO // 2
for y, texto, estilo in [(Y_S1, "S_1", "extremo"), (Y_MEDIO, "S'", "medio"), (Y_S2, "S_2", "extremo")]:
    if estilo == "extremo":
        p.append(f'<rect class="glass" x="{x0}" y="{y - ALTO // 2}" width="{ANCHO}" height="{ALTO}" rx="13" stroke="#1b2430" stroke-width="2.5" />')
        clase = "fo"
    else:
        p.append(f'<rect x="{x0}" y="{y - ALTO // 2}" width="{ANCHO}" height="{ALTO}" rx="13" fill="url(#g-ink)" filter="url(#ds)" />')
        clase = "fo t-white"
    p.append(fo(X_NODO, y, 19, 650, f"\\({texto}\\)", clase))

# Nota inferior
p += ['<rect class="glass" x="30" y="672" width="460" height="50" rx="16" />',
      fo(260, 697, 17, 600, "Por HI, Path es correcto con \\(\\lceil 8/2 \\rceil = 4\\)"),
      '</svg>']

open(f"{OUT}/correctitud.svg", "w").write("\n  ".join(p) + "\n")
print("ok")
