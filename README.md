# Planning: un problema PSPACE-completo

Proyecto de **Complejidad Computacional** (Facultad de Ciencias, UNAM).
Incluye el reporte escrito en LaTeX y la presentación hecha con Quarto.

```
planning/
├── reporte/                     # Reporte en LaTeX
│   ├── Reporte_Planning_PSPACE.tex
│   └── img/                     # Escudos (PDF)
└── presentacion/                # Presentación en Quarto (reveal.js)
    ├── presentacion.qmd         # Contenido de las diapositivas
    ├── custom.scss              # Tema visual (colores, tarjetas, layouts)
    ├── assets/deck.html         # Encabezado fijo + script de navegación
    ├── img/                     # Ilustraciones SVG, íconos y escudos
    ├── presentacion.pdf         # Versión PDF de la presentación
    └── herramientas/
        ├── mapa/                # Script que genera el mapa real de vuelos (img/flights.svg)
        └── pdf/                 # Script que exporta el HTML a PDF
```

---

## 1. Instalar Quarto

Quarto es la herramienta que convierte `presentacion.qmd` en una página HTML con las diapositivas.
La presentación se hizo con **Quarto 1.8**; cualquier versión 1.5 o mayor debería funcionar.

### Linux (Fedora, Ubuntu, etc.)

1. Descarga el instalador desde <https://quarto.org/docs/get-started/>.
   - Fedora: el archivo `.rpm` → `sudo dnf install ./quarto-*.rpm`
   - Ubuntu/Debian: el archivo `.deb` → `sudo apt install ./quarto-*.deb`
2. Verifica:

   ```bash
   quarto --version
   ```

### macOS

```bash
brew install --cask quarto
```

O descarga el `.pkg` de la misma página.

### Windows

Descarga el `.msi` de <https://quarto.org/docs/get-started/> e instálalo.
Después abre una terminal nueva (PowerShell) y ejecuta `quarto --version`.

> No hace falta instalar Python, R ni Jupyter: la presentación no ejecuta código.

---

## 2. Ver la presentación mientras se edita

```bash
cd presentacion
quarto preview presentacion.qmd
```

Se abre el navegador y **se recarga solo** cada vez que guardas `presentacion.qmd` o `custom.scss`.
Para detenerlo: `Ctrl + C` en la terminal.

## 3. Compilar (generar el HTML final)

```bash
cd presentacion
quarto render presentacion.qmd
```

Se generan:

- `presentacion.html` → la presentación (ábrela con doble clic o en el navegador).
- `presentacion_files/` → archivos de reveal.js que necesita el HTML.

Para mandarla a alguien, comparte **toda la carpeta `presentacion/`** (o un `.zip`), no solo el `.html`:
también necesita `img/` y `presentacion_files/`.

> ⚠️ Se necesita **internet** al abrirla: la tipografía (Inter) viene de Google Fonts
> y las fórmulas se dibujan con MathJax desde un CDN.

## 4. Exportar a PDF

Ya hay un PDF listo: `presentacion/presentacion.pdf` (19 páginas, vectorial, igual al HTML).
Si cambias la presentación, vuelve a generarlo:

**Opción A (recomendada, queda idéntico al HTML)** — necesita [Node.js](https://nodejs.org):

```bash
cd presentacion
quarto render presentacion.qmd          # primero actualizar el HTML
cd herramientas/pdf
npm install
npx playwright install chromium         # solo la primera vez
npm run pdf                             # reescribe presentacion/presentacion.pdf
```

**Opción B (manual, desde Chrome):**

1. Abre `presentacion.html` en **Chrome o Chromium**.
2. Agrega `?print-pdf` al final de la URL, por ejemplo
   `file:///.../presentacion.html?print-pdf`, y recarga.
3. `Ctrl + P` → Destino: *Guardar como PDF* → Diseño: *Horizontal* →
   Márgenes: *Ninguno* → activa *Gráficos de fondo* → Guardar.

## 5. Controles durante la exposición

| Tecla / botón | Acción |
|---|---|
| `→` / `Espacio` | Siguiente diapositiva |
| `←` | Diapositiva anterior |
| Botón con flecha (pastilla blanca) | Siguiente diapositiva |
| Menú ☰ (arriba a la derecha) o `Esc` | Vista general de todas las diapositivas |
| `F` | Pantalla completa |
| `S` | Vista del presentador (notas y cronómetro) |

---

## 6. Editar con IA (forma recomendada)

La forma más rápida y segura de modificar la presentación es pedírselo a un asistente de IA que pueda
leer y editar los archivos del proyecto, por ejemplo **Claude Code**
(<https://claude.com/claude-code>), desde la carpeta raíz `planning/`:

```bash
cd planning
claude
```

La IA ya entiende la estructura (layouts, tarjetas, LaTeX, SVG); solo describe el cambio en español.

### Ejemplos de lo que le puedes pedir

- *"En la diapositiva `#vuelos`, cambia el texto de la tarjeta blanca para explicar mejor por qué el
  viajero pasa dos veces por Madrid."*
- *"Agrega una diapositiva después de `#ejemplo` con el layout `.l-banner` que muestre las tres
  llamadas de `Path` del ejemplo de vuelos."*
- *"Pon mi nombre (Fulano de Tal, 3XXXXXXXX) en lugar de 'Nombre del integrante' en la portada
  y en la última diapositiva."*
- *"La ilustración `img/flights.svg` tiene una etiqueta encimada; acomódala."*
- *"Cambia el azul del tema por un verde, manteniendo el mismo estilo."*
- *"Compila la presentación y revisa que ninguna tarjeta se desborde."*

### Recomendaciones al usar IA

1. **Nombra la diapositiva** por su identificador (`#portada`, `#path`, `#vuelos`, …): así la IA
   va directo al lugar correcto. Los identificadores están después de cada `##` en `presentacion.qmd`.
2. **Pide un cambio a la vez** y revisa el resultado con `quarto preview` antes del siguiente.
3. **Pide que respete las convenciones**: matemáticas en LaTeX (`$...$` en el texto, `\(...\)` en
   SVG/HTML), las clases de `custom.scss` y el estilo de tarjetas existente.
4. **Revisa siempre las matemáticas y las citas**: la IA puede equivocarse en un teorema, una cota o
   una referencia. El contenido debe coincidir con el reporte (`reporte/Reporte_Planning_PSPACE.tex`).
5. **Haz una copia** de la carpeta (o usa git) antes de cambios grandes, para poder regresar.

Si prefieres editar a mano, la siguiente sección explica cómo está armado todo.

## 7. Cómo editar la presentación a mano

Cada diapositiva empieza con `##` y usa *divs* de Quarto (`:::`) para acomodar tarjetas:

````markdown
## Título de la diapositiva {#identificador}

::: {.stage .l-split}          <- elige el layout

::: {.card .media .a1}         <- tarjeta de ilustración en el hueco a1
```{=html}
{{< include img/hierarchy.svg >}}
```
:::

::: {.card .blue .a2}          <- tarjeta azul en el hueco a2
::: {.title-slot}              <- aquí aparece el título "##"
:::
[Siguiente]{.btn-arrow}        <- botón con flecha
:::

::: {.card .a3}                <- tarjeta blanca en el hueco a3
Texto normal con matemáticas: $2^n - 1$
:::

:::
````

### Piezas principales

| Clase | Qué es |
|---|---|
| `.card` | Tarjeta blanca |
| `.card.blue` | Tarjeta azul degradada |
| `.card.media` | Tarjeta para ilustración SVG |
| `.title-slot` (+ `.xl`, `.md`, `.sm`) | Lugar donde se coloca el título `##` (y su tamaño) |
| `.a1` … `.a5` | En qué hueco de la retícula va la tarjeta |
| `[texto]{.stat}`, `.stat-label`, `.stat-text` | Número grande con etiqueta y descripción |
| `[texto]{.pill}`, `[texto]{.chip}`, `[texto]{.btn-arrow}` | Pastilla, chip y botón flecha |

### Layouts disponibles (en `custom.scss`, sección 8)

| Clase | Distribución |
|---|---|
| `.l-hero` | Portada: ilustración + título + 2 tarjetas |
| `.l-stats` | Panel azul con título y tarjeta de cifras |
| `.l-split` | Ilustración + título azul + tarjeta de 3 columnas |
| `.l-deep` | Ilustración grande + título suelto + tarjeta |
| `.l-banner` (`.four`) | Banner azul + 3 (o 4) tarjetas de cifras |
| `.l-stack` (`.single`) | Título azul alto + 2 tarjetas apiladas (o 1) |
| `.l-plans` | Panel azul con 3 columnas tipo "planes" |
| `.l-mosaic` | Mosaico de 4 tarjetas |
| `.l-stories` | Título azul + 2 "historias" (ilustración + texto) |
| `.l-contact` | Ilustración + título + tarjeta de contacto |

### Matemáticas

- En el texto: LaTeX normal entre `$...$`, por ejemplo `$\textsf{Path}(S_0, S^*, 2^n)$`.
- En los SVG de `img/` y en bloques HTML: usar `\(...\)`, por ejemplo `\(S_0\)`.
- Las clases de complejidad dentro de fórmulas van con `\mathsf{PSPACE}`, igual que en el reporte.

### Mapa de la diapositiva de vuelos

`img/flights.svg` es un mapa real (datos de Natural Earth, rutas de gran círculo) generado con un
script. Solo hace falta volver a generarlo si cambian las ciudades o las rutas; para eso se necesita
[Node.js](https://nodejs.org):

```bash
cd presentacion/herramientas/mapa
npm install
npm run mapa          # reescribe ../../img/flights.svg
```

Las ciudades, rutas y etiquetas están al inicio de `generar-mapa.mjs`.

### Datos que hay que completar

En `presentacion.qmd` (portada y última diapositiva) y en `reporte/Reporte_Planning_PSPACE.tex` (portada):

- `Nombre del integrante` y `Número de cuenta`.
- Las iniciales del avatar (`[JR]{.avatar}`) si cambia quién presenta.
- En el reporte también: `NOMBRE DEL PROFESOR` y `NOMBRE DEL AYUDANTE`.

---

## 8. Compilar el reporte (LaTeX)

Se necesita una distribución de LaTeX (TeX Live en Linux, MacTeX en macOS o MiKTeX en Windows)
con los paquetes `tikz`, `algpseudocode`, `tcolorbox` y `microtype`.

```bash
cd reporte
pdflatex Reporte_Planning_PSPACE.tex
pdflatex Reporte_Planning_PSPACE.tex   # segunda vez para el índice y las referencias
```

O, si tienes `latexmk`:

```bash
latexmk -pdf Reporte_Planning_PSPACE.tex
```

---

## Problemas comunes

| Problema | Solución |
|---|---|
| `quarto: command not found` | Cierra y vuelve a abrir la terminal; si sigue, reinstala Quarto. |
| Las fórmulas salen como `$...$` o `\(...\)` | No hay internet (MathJax no cargó). |
| La letra se ve distinta (no es Inter) | No hay internet (Google Fonts no cargó). |
| Las imágenes no aparecen | Se abrió el `.html` fuera de su carpeta; deben estar juntos `img/` y `presentacion_files/`. |
| Cambié un SVG y no se ve el cambio | Vuelve a ejecutar `quarto render` (los SVG se incrustan al compilar). |
