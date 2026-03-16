#!/bin/bash

# start.sh - Script pour lancer le projet Fleet Optimization

MODE=${1:-dev}

if [ "$MODE" == "dev" ]; then
    echo "Lancement en mode DÉVELOPPEMENT (Hot Reload sur le port 4200)..."
    docker compose --profile dev up --build
elif [ "$MODE" == "prod" ]; then
    echo "Lancement en mode PRODUCTION (Nginx sur le port 80)..."
    docker compose --profile prod up --build -d
    echo "Frontend disponible sur http://localhost/"
else
    echo "Usage: ./start.sh [dev|prod]"
    exit 1
fi
