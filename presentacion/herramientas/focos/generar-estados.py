# Genera img/estados.svg: los hechos, un estado visto como tupla de valores binarios y los 2^n estados posibles.
# Uso: python3 generar-estados.py ../../img
import sys

OUT = sys.argv[1]
N = 3
ESTADO = (1, 0, 1)   # S = {c1, c3}


def fo(cx, cy, size, weight, tex, cls="fo", just="center", extra=""):
    h = round(size * 1.9, 1)
    x = {"center": cx - 260, "flex-start": cx, "flex-end": cx - 520}[just]
    return (f'<foreignObject x="{x:.1f}" y="{cy - h/2:.1f}" width="520" height="{h}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" '
            f'style="font-size:{size}px;font-weight:{weight};justify-content:{just};height:{h}px{extra}">{tex}</div></foreignObject>')


def txt(x, y, size, weight, s, cls="", anchor="middle", fill=None):
    f = f' fill="{fill}"' if fill else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" class="{cls}"{f}>{s}</text>'


p = [f'<svg xmlns="http://www.w3.org/2000/svg" class="ill" viewBox="0 0 740 740" role="img" aria-label="Un estado se ve como una tupla de {N} valores binarios; con {N} hechos hay {2**N} estados">']

# 1. Hechos (verdaderos = azul, falsos = gris)
p += ['<rect class="glass" x="170" y="36" width="400" height="196" rx="26" />',
      txt(206, 76, 16, 600, "HECHOS", "t-muted", "start")]
for k, v in enumerate(ESTADO):
    x = 206 + k * 84
    relleno = 'fill="url(#g-blue)"' if v else 'fill="#e6eef8"'
    clase = "fo t-white" if v else "fo t-muted"
    p.append(f'<rect x="{x}" y="96" width="72" height="46" rx="12" {relleno} />')
    p.append(fo(x + 36, 119, 19, 650, f"\\(c_{k + 1}\\)", clase))
    p.append(txt(x + 36, 176, 18, 650, str(v), "t-muted"))
p.append(txt(206, 208, 14, 500, "1 = se cumple · 0 = no se cumple", "t-muted", "start"))
p.append('<path class="edge" d="M370 242 V264" />')

# 2. El estado como tupla binaria
p += ['<rect x="130" y="272" width="480" height="196" rx="28" fill="url(#g-ink)" filter="url(#ds)" />',
      fo(166, 306, 28, 700, "Estado \\(S\\)", "fo t-white", "flex-start"),
      fo(574, 306, 16, 400, "tupla binaria", "fo", "flex-end", ";color:#9fb3c9"),
      fo(370, 392, 56, 700, "\\((" + ",\\,".join(str(v) for v in ESTADO) + ")\\)", "fo t-white"),
      '<path class="edge" d="M370 480 V516" />']

# 3. Todos los estados posibles
p += ['<rect class="glass" x="70" y="526" width="600" height="190" rx="26" />',
      txt(104, 566, 15, 600, "TODOS LOS ESTADOS POSIBLES", "t-muted", "start")]
for i in range(2 ** N):
    bits = [(i >> (N - 1 - b)) & 1 for b in range(N)]
    fila, col = divmod(i, 4)
    x, y = 100 + col * 136, 590 + fila * 58
    activo = tuple(bits) == ESTADO
    if activo:
        p.append(f'<rect x="{x}" y="{y}" width="124" height="44" rx="12" fill="url(#g-ink)" />')
    else:
        p.append(f'<rect x="{x}" y="{y}" width="124" height="44" rx="12" fill="#fff" fill-opacity=".8" />')
    p.append(txt(x + 62, y + 29, 18, 650, "(" + ", ".join(map(str, bits)) + ")", "t-white" if activo else ""))
p += ['<rect class="glass" x="538" y="498" width="132" height="50" rx="16" />',
      fo(604, 523, 20, 700, f"\\(2^{N} = {2**N}\\)"),
      '</svg>']
open(f"{OUT}/estados.svg", "w").write("\n  ".join(p) + "\n")
print("ok")
