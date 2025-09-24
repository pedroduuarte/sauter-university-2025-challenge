# Dockerfile
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Diretório da aplicação
WORKDIR /app

# Copiar apenas requirements para otimizar cache
COPY requirements.txt .

# Instalar dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Expor porta do FastAPI
EXPOSE 8080

# Comando de execução do Cloud Run
CMD ["sh", "-c", "uvicorn src.ons_api.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
