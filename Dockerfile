FROM python:3.9-slim

# Mise à jour du système et installation des dépendances nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer TA-Lib
RUN pip install TA-Lib

# Copier votre application
WORKDIR /app
COPY . /app

# Installer les autres dépendances Python
RUN pip install -r requirements.txt

CMD ["python", "Bot.py"]
