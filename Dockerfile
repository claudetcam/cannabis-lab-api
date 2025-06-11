# Étape de base Playwright avec tous les navigateurs
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && playwright install --with-deps

# Copie ton app
COPY . .

# Crée dossier pour les secrets (Render les montera ici)
RUN mkdir -p /etc/secrets

# Expose port (facultatif pour local, utile pour Render)
EXPOSE 10000

# Lancer gunicorn
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:10000"]
