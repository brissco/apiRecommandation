# Utiliser une image de base Python
FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /var/www/apiRecommandation

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application dans le conteneur
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput || true

# Commande par défaut pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
