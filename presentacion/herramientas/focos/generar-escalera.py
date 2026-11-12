# Genera img/planning-escalera.svg: una escalera de acciones válidas que sube del estado inicial al estado final.
# Mismo lenguaje visual que la portada (tarjetas de vidrio, flechas azules, insertos con palomita).
# Incluye dos errores posibles: una acción no válida (requisitos sin cumplir) y un estado atascado.
# Uso: python3 generar-escalera.py ../../img
import sys

OUT = sys.argv[1]


def fo(x, y, size, weight, tex, cls="fo", just="flex-start", extra=""):
    h = round(size * 1.9, 1)
    return (f'<foreignObject x="{x}" y="{y}" width="520" height="{h}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" '
            f'style="font-size:{size}px;font-weight:{weight};justify-content:{just};height:{h}px{extra}">{tex}</div></foreignObject>')


def palomita(cx, cy, r=12):
    return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1f7a4d" />',
            f'<path d="m{cx - 6} {cy} 4.5 4.5 8-8.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" />']


# Posiciones verticales de cada pieza (la escalera ocupa todo el alto)
Y_S0, Y_P1, Y_P2, Y_SF, Y_ATASCO, Y_NOVALIDA = 448, 322, 196, 40, 136, 406

p = ['<svg xmlns="http://www.w3.org/2000/svg" class="ill" viewBox="0 0 640 570" role="img" aria-label="Escalera de acciones válidas que sube del estado inicial al estado final, con una acción no válida y un estado atascado">']

# Flechas (van debajo de las tarjetas)
p += [f'<path class="edge" d="M118 {Y_S0 - 2} C118 {Y_S0 - 48} 138 {Y_P1 + 36} 166 {Y_P1 + 27}" />',
      f'<path class="edge" d="M246 {Y_P1 - 2} C246 {Y_P1 - 52} 270 {Y_P2 + 30} 326 {Y_P2 + 25}" />',
      f'<path class="edge" d="M406 {Y_P2 - 2} C406 {Y_P2 - 56} 428 {Y_SF + 56} 446 {Y_SF + 42}" />',
      # rama hacia el estado atascado
      f'<path class="edge" d="M214 {Y_P1 - 4} C214 {Y_P1 - 52} 172 {Y_ATASCO + 108} 140 {Y_ATASCO + 74}" />',
      # acción no válida: línea punteada que se corta
      f'<path d="M198 {Y_S0 + 44} C270 {Y_S0 + 62} 330 {Y_NOVALIDA + 64} 380 {Y_NOVALIDA + 40}" fill="none" stroke="#b0413e" stroke-width="2.6" stroke-dasharray="3 7" stroke-linecap="round" />']

# Estado inicial
p += [f'<rect class="glass" x="28" y="{Y_S0}" width="170" height="72" rx="18" />',
      f'<circle cx="62" cy="{Y_S0 + 36}" r="17" class="accent" />',
      fo(56, Y_S0 + 21, 16, 700, "\\(S\\)", "fo t-white"),
      f'<text x="90" y="{Y_S0 + 30}" font-size="14" class="t-muted">estado inicial</text>',
      fo(90, Y_S0 + 27.5, 21, 650, "\\(S_0\\)")]

# Acciones válidas
for x, y, op in [(170, Y_P1, "O_{i_1}"), (330, Y_P2, "O_{i_2}")]:
    p.append(f'<rect class="glass" x="{x}" y="{y}" width="150" height="50" rx="16" />')
    p += palomita(x + 26, y + 25)
    p.append(f'<text x="{x + 50}" y="{y + 21}" font-size="13" class="t-muted">acción válida</text>')
    p.append(fo(x + 50, y + 18, 18, 650, f"\\({op}\\)"))

# Estado final
p += [f'<rect x="450" y="{Y_SF}" width="170" height="72" rx="20" fill="url(#g-ink)" filter="url(#ds)" />',
      f'<text x="474" y="{Y_SF + 28}" font-size="14" fill="#9fb3c9">estado final</text>',
      fo(474, Y_SF + 27, 24, 650, "\\(S^*\\)", "fo t-white")]
p += palomita(592, Y_SF + 36, 14)

# Estado atascado: ninguna acción es válida desde ahí
p += [f'<rect class="glass" x="24" y="{Y_ATASCO}" width="236" height="72" rx="16" />',
      f'<circle cx="56" cy="{Y_ATASCO + 36}" r="15" fill="#c27a1d" />',
      f'<rect x="48" y="{Y_ATASCO + 33}" width="16" height="6" rx="3" fill="#fff" />',
      f'<text x="82" y="{Y_ATASCO + 30}" font-size="15" font-weight="650">estado atascado</text>',
      fo(82, Y_ATASCO + 34, 14, 500, "ninguna acción es válida", "fo t-muted")]

# Acción no válida
p += [f'<rect class="glass" x="380" y="{Y_NOVALIDA}" width="226" height="64" rx="16" />',
      f'<circle cx="410" cy="{Y_NOVALIDA + 32}" r="13" fill="#b0413e" />',
      f'<path d="m404 {Y_NOVALIDA + 26} 12 12m0 -12 -12 12" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round" />',
      f'<text x="434" y="{Y_NOVALIDA + 26}" font-size="14" font-weight="650">acción no válida</text>',
      fo(434, Y_NOVALIDA + 23, 14, 500, "requisitos sin cumplir", "fo t-muted"),
      '</svg>']
open(f"{OUT}/planning-escalera.svg", "w").write("\n  ".join(p) + "\n")
print("ok")
