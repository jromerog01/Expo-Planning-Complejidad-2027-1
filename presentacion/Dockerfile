# Imagen que sirve la presentación (HTML de Quarto/reveal.js) con nginx.
#
# Antes de construir, renderiza la presentación para que el HTML esté al día:
#   quarto render presentacion.qmd
#
# Construir y correr (desde esta carpeta):
#   docker compose up -d --build

FROM nginx:1.27-alpine

# Configuración del sitio (ver nginx.conf)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Archivos que necesita el HTML para verse completo.
# La presentación se copia como index.html para que abra en la raíz "/".
COPY presentacion.html  /usr/share/nginx/html/index.html
COPY presentacion_files /usr/share/nginx/html/presentacion_files
COPY img                /usr/share/nginx/html/img

# Opcional: el PDF también queda disponible en /presentacion.pdf
COPY presentacion.pdf   /usr/share/nginx/html/presentacion.pdf

EXPOSE 80
