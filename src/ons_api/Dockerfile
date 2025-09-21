# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Variável de ambiente do Python
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta
EXPOSE 8080

# Comando para rodar a API (FastAPI com uvicorn)
CMD ["uvicorn", "ons_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
