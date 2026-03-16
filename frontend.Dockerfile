# Étape 1 : Build de l'application Angular
FROM node:20 AS build

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY frontend/package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code du frontend
COPY frontend/ .

# Builder l'application en mode production
RUN npm run build -- --configuration production

# Étape 2 : Serveur de production Nginx
FROM nginx:alpine

# Copier les fichiers buildés vers le répertoire Nginx
# Note : Le chemin de sortie peut dépendre de votre angular.json (souvent dist/frontend/browser)
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html

# Copier une configuration Nginx personnalisée si nécessaire (optionnel)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Lancer Nginx
CMD ["nginx", "-g", "daemon off;"]
