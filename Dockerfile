# Imagem base
FROM python:3.11-slim

# Variável de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY . /app

# Instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Executa o bot
CMD ["python", "bot-financeiro-backend.py"]
