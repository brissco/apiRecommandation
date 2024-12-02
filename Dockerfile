# Utiliser une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /var/www/apiRecommandation

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application dans le conteneur
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Collecter les fichiers statiques (optionnel)
RUN python manage.py collectstatic --noinput || true

# Commande par défaut pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
