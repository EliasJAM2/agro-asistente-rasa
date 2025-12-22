# 1. Usamos la imagen exacta de tu computadora para evitar errores de versión
FROM rasa/rasa:3.6.21-full

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copiamos todos los archivos del proyecto (incluyendo la carpeta models)
COPY . /app

# 4. Cambiamos a root para instalar dependencias y ajustar permisos
USER root

# Instalamos requests (que mencionaste que usas)
RUN pip install --no-cache-dir requests

# Otorgamos permisos totales a la carpeta de modelos para que Rasa pueda leer el archivo .tar.gz
RUN chmod -R 777 /app/models

# 5. Volvemos al usuario estándar de Rasa por seguridad
USER 1001

# 6. COMANDO CRUCIAL: Usamos la variable $PORT que Render asigna automáticamente.
# Esto evita el error de "Port scan timeout".
ENTRYPOINT []
CMD rasa run --enable-api --cors "*" --port $PORT
