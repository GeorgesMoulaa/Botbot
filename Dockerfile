FROM python:3.9-slim

# Mise à jour et installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation de TA-Lib
RUN pip install TA-Lib

# Copier ton application dans le conteneur
WORKDIR /app
COPY . /app

# Installer les autres dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Démarrer ton application
CMD ["python", "Bot.py"]
