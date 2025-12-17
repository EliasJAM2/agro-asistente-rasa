# Dockerfile
# Usa la imagen base oficial de Rasa con todas las dependencias
FROM rasa/rasa:3.6.13-full

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido de tu proyecto al contenedor
COPY . /app

# Instala cualquier dependencia adicional que necesite tu modelo (como requests)
USER root
RUN pip install requests
USER 1001

# Comando para iniciar Rasa Core
# Se expone el puerto 5005 y se habilita la API para que el frontend pueda conectarse

CMD ["rasa", "run", "--enable-api", "--port", "5005", "--credentials", "credentials.yml"]
