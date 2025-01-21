# Instruções para Docker - Aplicação Streamlit

Este repositório contém a aplicação web de um chatbot baeado em uma LLM/RAG implementada com LangChain.

![architecture](architecture.png)

## Pré-requisitos

Antes de gerar a imagem Docker, certifique-se de ter o Docker instalado no seu sistema.

- [Docker Desktop para Windows/Mac](https://www.docker.com/products/docker-desktop)
- [Docker Engine para Linux](https://docs.docker.com/engine/install/)

Versão: `Docker version 27.3.1, build ce12230` 

## Passos para Gerar e Executar a Imagem

1. **Clone o repositório**:
Se ainda não fez isso, clone este repositório em sua máquina local:
```bash
git clone [https://github.com/fernandojunior/insurance-gen-ai](https://github.com/fernandojunior/insurance-gen-ai)
cd insurance-gen-ai/
```

2. **Download de arquivos**
Faça download dos arquivos PDFs e armazene no diretório `dat/input/`

3. **Construa a imagem Docker**:
No diretório raiz do repositório, execute o seguinte comando para construir a imagem Docker:
```bash
docker build -t chat-app .
```

Esse comando criará uma imagem Docker chamada `chat-app`.

4. **Variáveis de ambiente**

Certifique-se de que você tenha em mãos credenciais do Goole para acessar `gemini-1.5-flash`. Crie um `.env` e insira o texto abaixo:

```bash
GOOGLE_API_KEY="SUA CHAVE".
```

5. **Execute a imagem Docker localmente**:

Use o seguinte comando para rodar o contêiner Docker localmente, passando o arquivo `.env` como parâmetro para carregar as variáveis de ambiente:

```bash
docker run --env-file .env -p 8501:8501 chat-app

docker run --env-file .env -p 8501:8501 -v $(pwd)/data/output/:/app/data/output -v $(pwd)/data/input:/app/data/input -v $(pwd)/data/database/:/app/data/database chat-app
```

6. **Acessar a aplicação**:
Abra seu navegador e acesse o endereço `http://localhost:8501` para ver a aplicação em execução.

## Testes

```bash
docker build -t chat-test . -f Dockerfile.dev
docker run chat-test
```

## Lint

```bash
pip install flake8-black
black src/
flake8 src/
```
