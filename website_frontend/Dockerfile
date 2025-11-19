# Dockerfile para desplegar tu app Reflex (frontend + backend) en un solo contenedor
# Compatible con Railway, Render, DigitalOcean Apps, etc.

# Imagen base completa (más simple, incluye unzip y herramientas del sistema)
FROM python:3.11

# Configuración básica de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Instalamos Caddy como reverse proxy para unificar frontend + backend en un solo puerto
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    caddy \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor como /app
WORKDIR /app

# Puerto de salida del contenedor.
# Puerto por defecto (se sobreescribe con PORT de Railway)
ARG PORT=8000
ARG API_URL
ARG DATABASE_URL

# PORT y DATABASE_URL se pueden sobreescribir con variables de entorno de Railway
ENV PORT=${PORT} \
    API_URL=${API_URL:-http://localhost:${PORT}} \
    DATABASE_URL=${DATABASE_URL:-""}

# Caddyfile inline: sirve frontend desde /srv y hace proxy al backend de Reflex (8000)
RUN cat > Caddyfile <<EOF
:\$PORT

encode gzip

@backend_routes path /_event/* /ping /_upload /_upload/*
handle @backend_routes {
    reverse_proxy localhost:8000
}

root * /srv
route {
    try_files {path} {path}/ /404.html
    file_server
}
EOF

# Copiamos solo requirements primero para aprovechar cache de Docker
COPY requirements.txt ./

# Instalamos dependencias de Python (Reflex, Supabase, ConfigCat, etc.)
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiamos el resto del código de la app
COPY . .

# Inicializamos Reflex (genera estructura interna .web, etc.)
RUN reflex init

# Compilamos el frontend a estáticos y los movemos a /srv
# (sigue el patrón recomendado en la guía de self-hosting de Reflex)
RUN reflex export --frontend-only --no-zip && \
    mkdir -p /srv && \
    mv .web/_static/* /srv/ && \
    rm -rf .web

# Hasta que Reflex maneje bien SIGTERM
STOPSIGNAL SIGKILL

# Exponemos el puerto (Railway inyecta su propio PORT en runtime)
EXPOSE ${PORT}

# Arranque:
# 1) Caddy sirve el frontend y hace proxy al backend
# 2) Reflex levanta solo el backend en modo prod
CMD caddy start && reflex run --env prod --backend-only --loglevel debug