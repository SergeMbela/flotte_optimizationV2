FROM node:20

WORKDIR /app

# Install Angular CLI globally
RUN npm install -g @angular/cli@18.2.21

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# The rest of the code will be mounted as a volume in docker-compose
# for hot reload to work efficiently.

EXPOSE 4200

# Start command with host 0.0.0.0 and poll for WSL filesystem changes
CMD ["ng", "serve", "--host", "0.0.0.0", "--poll", "2000"]
