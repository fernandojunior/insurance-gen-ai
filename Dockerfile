# Base image
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

COPY ./requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar arquivos da aplicação para o container
COPY ./data  /app/data/
COPY ./src /app/

# Expor a porta padrão do Streamlit (8501)
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "app.py"]
