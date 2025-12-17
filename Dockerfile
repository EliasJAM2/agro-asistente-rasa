# Usa la imagen base oficial de Rasa
FROM rasa/rasa:3.6.15-full

# Establece el directorio de trabajo
WORKDIR /app

# Copia todo el proyecto (esto incluye la carpeta models)
COPY . /app

# Permisos de root para instalar dependencias
USER root
RUN pip install --no-cache-dir requests

# Volvemos al usuario de Rasa
USER 1001

# Usamos CMD en lugar de ENTRYPOINT para que Render pueda manejar mejor los argumentos
# El puerto se define con la variable $PORT que Render asigna automáticamente
CMD ["run", "--enable-api", "--cors", "*", "--port", "10000"]
