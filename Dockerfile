# Usa una imagen base de Python 3.10
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt para instalar las dependencias
COPY requirements.txt /app/requirements.txt

# Instala las dependencias usando pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copia los archivos y directorios de la aplicación al contenedor
COPY . /app

# Comando para ejecutar la aplicación cuando el contenedor se inicia
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]