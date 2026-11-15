# Genera img/tiempo.svg: el árbol de llamadas de Path, para el análisis de tiempo.
# Cada llamada con L hace a lo más a = 2^(n+1) llamadas con L/2, así que el nivel i tiene a^i llamadas
# y la suma 1 + a + ... + a^n <= 2 a^n está dominada por el último nivel.
# Uso: python3 generar-tiempo.py ../../img
import sys

OUT = sys.argv[1]

X_ETIQ, X_BARRA = 50, 190           # x de las etiquetas de L y de las barras
ALTO_BARRA = 40
# (etiqueta de L, llamadas en ese nivel, ancho de la barra, y del centro)
FILAS = [
    ("2^n", "1", 30, 140),
    ("2^{n-1}", "a", 80, 232),
    ("2^{n-2}", "a^2", 150, 324),
    ("1", "a^n", 240, 480),
]
Y_PUNTOS = 402


def fo(cx, cy, size, weight, tex, cls="fo", just="center", extra=""):
    h = round(size * 1.9, 1)
    x = {"center": cx - 260, "flex-start": cx, "flex-end": cx - 520}[just]
    return (f'<foreignObject x="{x:.1f}" y="{cy - h/2:.1f}" width="520" height="{h}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" '
            f'style="font-size:{size}px;font-weight:{weight};justify-content:{just};height:{h}px{extra}">{tex}</div></foreignObject>')


p = ['<svg xmlns="http://www.w3.org/2000/svg" class="ill" viewBox="0 0 520 736" role="img" '
     'aria-label="Árbol de llamadas de Path: el nivel i tiene a a la i llamadas, con a igual a 2 a la n más 1; domina el último nivel">']

# Encabezado: el factor de ramificación
p += ['<rect x="50" y="22" width="420" height="50" rx="16" fill="url(#g-ink)" filter="url(#ds)" />',
      fo(260, 47, 18, 650, "Cada llamada hace a lo más \\(a = 2^{n+1}\\) llamadas", "fo t-white")]

p.append(fo(X_ETIQ, 104, 15, 600, "NIVEL", "fo t-muted", "flex-start"))
p.append(fo(X_BARRA, 104, 15, 600, "LLAMADAS", "fo t-muted", "flex-start"))

# Niveles del árbol: L, y número de llamadas (barra proporcional, no a escala)
for k, (nivel, llamadas, ancho, y) in enumerate(FILAS):
    ultimo = k == len(FILAS) - 1
    p.append(fo(X_ETIQ, y, 22, 650, f"\\(L = {nivel}\\)", "fo", "flex-start"))
    if ultimo:
        p.append(f'<rect x="{X_BARRA}" y="{y - ALTO_BARRA // 2}" width="{ancho}" height="{ALTO_BARRA}" rx="12" fill="url(#g-ink)" filter="url(#ds)" />')
    else:
        p.append(f'<rect x="{X_BARRA}" y="{y - ALTO_BARRA // 2}" width="{ancho}" height="{ALTO_BARRA}" rx="12" fill="url(#g-blue)" />')
    p.append(fo(X_BARRA + ancho + 14, y, 22, 700, f"\\({llamadas}\\)", "fo", "flex-start"))
p.append(fo(X_BARRA + 14, Y_PUNTOS, 26, 700, "\\(\\vdots\\)", "fo t-muted", "flex-start"))

# Suma de los niveles y resultado
p += ['<rect class="glass" x="50" y="548" width="420" height="82" rx="20" />',
      fo(260, 574, 15, 600, "SUMA DE TODOS LOS NIVELES", "fo t-muted"),
      fo(260, 607, 24, 650, "\\(1 + a + \\cdots + a^n \\le 2a^n\\)"),
      '<rect class="glass" x="50" y="660" width="420" height="58" rx="18" stroke="#1b2430" stroke-width="2.5" />',
      fo(260, 689, 22, 650, "\\(N(2^n) \\le 2^{n(n+1)+1} = 2^{O(n^2)}\\)"),
      '</svg>']

open(f"{OUT}/tiempo.svg", "w").write("\n  ".join(p) + "\n")
print("ok")
