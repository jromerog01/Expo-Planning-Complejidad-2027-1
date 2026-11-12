# Genera img/focos3.svg e img/focos4.svg: focos y botones del contador (Teorema 9.6 del reporte).
# Botón i (operador O_i): requiere los focos 1..i-1 encendidos; enciende el foco i y apaga los anteriores.
# Uso: python3 generar-focos.py ../../img
import sys

OUT = sys.argv[1]
COLORES = ["#e1eefb", "#cfe3f7", "#8bb9ea", "#6fa6e3"]   # un tono por botón


def plan(n):
    """Devuelve [(botón, estado)] para el plan mínimo; el estado es un conjunto de focos encendidos."""
    estado, pasos = set(), []
    while len(estado) < n:
        i = next(k for k in range(1, n + 1) if k not in estado)   # primer foco apagado
        assert all(j in estado for j in range(1, i)), "botón no aplicable"
        estado = {j for j in estado if j > i} | {i}
        pasos.append((i, set(estado)))
    return pasos


def fo(cx, cy, size, weight, tex, cls="fo", just="center", extra=""):
    h = round(size * 1.9, 1)
    x = {"center": cx - 260, "flex-start": cx, "flex-end": cx - 520}[just]
    return (f'<foreignObject x="{x:.1f}" y="{cy - h/2:.1f}" width="520" height="{h}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" '
            f'style="font-size:{size}px;font-weight:{weight};justify-content:{just};height:{h}px{extra}">{tex}</div></foreignObject>')


def txt(x, y, size, weight, s, cls="", anchor="middle"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" class="{cls}">{s}</text>'


def foco(cx, cy, r, on):
    s = [f'<rect x="{cx - r*0.42:.1f}" y="{cy + r*0.78:.1f}" width="{r*0.84:.1f}" height="{r*0.62:.1f}" rx="2.5" fill="#1f4a7d" fill-opacity="{0.9 if on else 0.28}" />']
    if on:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="#8bb9ea" fill-opacity=".38" />')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g-blue)" />')
        s.append(f'<circle cx="{cx - r*0.32:.1f}" cy="{cy - r*0.34:.1f}" r="{r*0.24:.1f}" fill="#fff" fill-opacity=".8" />')
    else:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="#cdd9e7" stroke-width="1.5" />')
    return "".join(s)


def botones(n, w, gap, x0, y=28, h=58):
    s = []
    for i in range(1, n + 1):
        x = x0 + (i - 1) * (w + gap)
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{COLORES[i-1]}" stroke="#fff" stroke-width="2.5" filter="url(#ds-sm)" />')
        s.append(txt(x + w / 2, y + 37, 19, 700, f"Botón {i}", "ink"))
    return s


def tabla(n, filas, ox, ancho, y0, paso, r, col_pill, ancho_pill, xs_focos, primer_paso):
    """Un panel con encabezado y una fila por paso: número de paso, botón presionado y focos."""
    s = [f'<rect class="glass" x="{ox}" y="108" width="{ancho}" height="{y0 + (len(filas) - 1) * paso + 28 - 108}" rx="22" />']
    s.append(txt(ox + 24, 140, 13, 600, "paso", "t-muted"))
    s.append(txt(ox + col_pill + ancho_pill / 2, 140, 13, 600, "botón", "t-muted"))
    for k, x in enumerate(xs_focos, 1):
        s.append(txt(ox + x, 140, 13, 600, f"foco {k}" if n == 3 else f"F{k}", "t-muted"))
    for i, (boton, estado) in enumerate(filas):
        cy = y0 + i * paso
        s.append(txt(ox + 24, cy + 5, 15, 600, primer_paso + i, "t-muted"))
        if boton is None:
            s.append(f'<rect x="{ox + col_pill}" y="{cy - 15}" width="{ancho_pill}" height="30" rx="15" fill="#fff" fill-opacity=".55" />')
            s.append(txt(ox + col_pill + ancho_pill / 2, cy + 5, 14, 600, "inicio", "t-muted"))
        else:
            s.append(f'<rect x="{ox + col_pill}" y="{cy - 15}" width="{ancho_pill}" height="30" rx="15" fill="{COLORES[boton-1]}" stroke="#fff" stroke-width="1.5" />')
            s.append(txt(ox + col_pill + ancho_pill / 2, cy + 5, 14, 700, f"Botón {boton}", "ink"))
        for k, x in enumerate(xs_focos, 1):
            s.append(foco(ox + x, cy - 3, r, k in estado))
    return s


def svg(n):
    pasos = [(None, set())] + plan(n)
    cabeza = f'<svg xmlns="http://www.w3.org/2000/svg" class="ill" viewBox="0 0 {W} 620" role="img" aria-label="{n} focos y {n} botones: cada fila muestra el botón presionado y los focos encendidos">'
    partes = [cabeza]
    if n == 3:
        partes += botones(3, 150, 20, 35)
        partes += tabla(3, pasos, 30, 500, 176, 46, 16, 70, 110, [290, 365, 440], 0)
        centro, ancho_pastilla = 280, 270
    else:
        partes += botones(4, 122, 14, 35)
        partes += tabla(4, pasos[:8], 20, 272, 176, 46, 12, 44, 78, [146, 180, 214, 248], 0)
        partes += tabla(4, pasos[8:], 308, 272, 176, 46, 12, 44, 78, [146, 180, 214, 248], 8)
        centro, ancho_pastilla = 300, 290
    partes.append(f'<rect x="{centro - ancho_pastilla/2}" y="548" width="{ancho_pastilla}" height="54" rx="16" fill="url(#g-ink)" filter="url(#ds)" />')
    partes.append(fo(centro, 575, 18, 650, f"\\({2**n - 1} = {2**(n-1) - 1} + 1 + {2**(n-1) - 1}\\) pasos", cls="fo t-white"))
    partes.append("</svg>")
    return "\n  ".join(partes) + "\n"


W = 560
open(f"{OUT}/focos3.svg", "w").write(svg(3))
W = 600
open(f"{OUT}/focos4.svg", "w").write(svg(4))
print("ok")
