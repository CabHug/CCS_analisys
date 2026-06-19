# 1. Imagen base oficial de Python 3.14 (versión slim para mantenerla ligera)
FROM python:3.14-slim

# 2. Configurar variables de entorno para optimizar Python en Docker
# Esto evita que Python genere archivos temporales .pyc y fuerza la salida de logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema necesarias para compilar librerías como psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar el archivo de requerimientos optimizado
COPY requirements.txt .

# 6. Instalar las librerías de Python de terceros
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiar la estructura completa del proyecto al contenedor
COPY . .

# 8. Comando para arrancar la aplicación interactiva
CMD ["python", "menu.py"]