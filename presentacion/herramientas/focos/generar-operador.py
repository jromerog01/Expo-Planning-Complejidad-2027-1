# Genera img/operador-ejemplo.svg: cómo el botón 2 transforma un estado de los focos en otro (diagrama vertical).
# Estado inicial -> Botón 2 (prerrequisito, agrega, elimina) -> estado nuevo.
# Uso: python3 generar-operador.py ../../img
import sys

OUT = sys.argv[1]


def txt(x, y, size, weight, s, cls="", anchor="middle", fill=None):
    f = f' fill="{fill}"' if fill else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" class="{cls}"{f}>{s}</text>'


def foco(cx, cy, r, on):
    s = [f'<rect x="{cx - r*0.42:.1f}" y="{cy + r*0.78:.1f}" width="{r*0.84:.1f}" height="{r*0.62:.1f}" rx="2.5" fill="#1f4a7d" fill-opacity="{0.9 if on else 0.28}" />']
    if on:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="#8bb9ea" fill-opacity=".38" />')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g-blue)" />')
        s.append(f'<circle cx="{cx - r*0.32:.1f}" cy="{cy - r*0.34:.1f}" r="{r*0.24:.1f}" fill="#fff" fill-opacity=".8" />')
    else:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="#cdd9e7" stroke-width="1.5" />')
    return "".join(s)


def estado(y, titulo, valores):
    s = [f'<rect class="glass" x="30" y="{y}" width="460" height="170" rx="26" />',
         txt(260, y + 38, 20, 650, titulo, "t-muted")]
    for k, on in enumerate(valores):
        cx = 107 + k * 153
        s.append(foco(cx, y + 90, 25, on))
        s.append(txt(cx, y + 142, 17, 600, f"foco {k + 1}", "t-muted"))
        s.append(txt(cx, y + 163, 16, 650, "encendido" if on else "apagado", "t-accent" if on else "t-muted"))
    return s


def fila(y, letra, color, etiqueta, texto, palomita=False):
    s = [f'<rect x="38" y="{y}" width="444" height="62" rx="14" fill="#ffffff" fill-opacity=".08" />',
         f'<circle cx="74" cy="{y + 31}" r="17" fill="{color}" fill-opacity=".2" />',
         txt(74, y + 38, 19, 700, letra, fill=color),
         txt(106, y + 26, 15, 500, etiqueta, anchor="start", fill="#9fb3c9"),
         txt(106, y + 50, 21, 650, texto, "t-white", "start")]
    if palomita:
        s += [f'<circle cx="452" cy="{y + 31}" r="14" fill="#1f7a4d" />',
              f'<path d="m445 {y + 31} 5 5 9-9.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" />']
    return s


p = ['<svg xmlns="http://www.w3.org/2000/svg" class="ill" viewBox="0 0 520 742" role="img" aria-label="El botón 2 convierte el estado con solo el foco 1 encendido en el estado con solo el foco 2 encendido">']
p += estado(20, "Estado inicial", [True, False, False])
p += ['<path class="edge" d="M260 194 V234" />']
p += ['<rect x="20" y="242" width="480" height="270" rx="30" fill="url(#g-ink)" filter="url(#ds)" />',
      txt(52, 286, 27, 700, "Botón 2", "t-white", "start")]
p += fila(300, "P", "#8fc0f2", "prerrequisito", "foco 1 encendido", True)
p += fila(368, "A", "#7fd6a6", "agrega", "foco 2 encendido")
p += fila(436, "D", "#f2a29a", "elimina", "foco 1 encendido")
p += ['<path class="edge" d="M260 524 V550" />']
p += estado(552, "Estado nuevo", [False, True, False])
p.append("</svg>")
open(f"{OUT}/operador-ejemplo.svg", "w").write("\n  ".join(p) + "\n")
print("ok")
