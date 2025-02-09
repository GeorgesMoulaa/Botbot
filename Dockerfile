# Utiliser une image Python officielle comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Mettre à jour pip pour éviter les erreurs de version
RUN pip install --upgrade pip

# Installer les dépendances système nécessaires pour TA-Lib
RUN apt-get update && \
    apt-get install -y build-essential libatlas-base-dev

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt .

# Installer les dépendances à partir du fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port sur lequel l'application s'exécute (si nécessaire)
# EXPOSE 5000

# Commande à exécuter lors du démarrage du conteneur
CMD ["python", "Bot.py"]
