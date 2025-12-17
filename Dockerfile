# Usamos exactamente tu versión de PC
FROM rasa/rasa:3.6.21-full

WORKDIR /app

# Copiamos el proyecto
COPY . /app

USER root
# Instalamos dependencias necesarias
RUN pip install --no-cache-dir requests

# Aseguramos que el modelo sea legible
RUN chmod -R 777 /app/models

USER 1001

# Usamos el puerto que Render asigna automáticamente
CMD ["run", "--enable-api", "--cors", "*", "--port", "10000"]
