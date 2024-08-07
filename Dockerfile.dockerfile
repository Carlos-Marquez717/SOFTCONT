# Usa una imagen base adecuada
FROM python:3.12-slim

# Define variables de entorno necesarias
ENV NIXPACKS_PATH=/opt/venv/bin
ENV PATH=$NIXPACKS_PATH:$PATH

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Configura el directorio de trabajo
WORKDIR /app

# Crea el entorno virtual y instala las dependencias
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia el resto de la aplicación al contenedor
COPY . /app/

# Configura el comando de inicio de la aplicación
CMD ["python", "app.py"]
