# 1. Imagen base
FROM python:3.10-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Instalación de dependencias
COPY requirements.txt .
# ERROR CORREGIDO: Es --no-cache-dir (con 'o', no 'non')
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el código fuente
COPY . .

# 5. Puerto de Streamlit
EXPOSE 8501

# 6. Comando de arranque
# ERROR CORREGIDO: En Linux se usa "/" no "\". 
# Además, faltaban comas en la lista del CMD.
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]