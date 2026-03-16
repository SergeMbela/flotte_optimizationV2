# Utiliser une image Python officielle légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour psycopg2 et postgis
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port sur lequel FastAPI va tourner
EXPOSE 8000

# Commande pour démarrer l'application (initialisation DB puis lancement API)
# Utilise shell form pour permettre l'exécution séquentielle
CMD python main.py --init-db && uvicorn api.main:app --host 0.0.0.0 --port 8000
