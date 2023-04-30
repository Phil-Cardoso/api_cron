# Instalando python:3.8-slim-buster
FROM python:3.8-slim-buster

# Atualizando pip
RUN pip install --upgrade pip

# Criando pasta para app
WORKDIR /app

# Copiando arquivo com libs necessarias
COPY requirements.txt requirements.txt

# Instalando libs com base no arquivo
RUN pip install -r requirements.txt

# Copiando arquivos do projeto para o docker
COPY . .

# Comando para executar quando imagem for executada
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]