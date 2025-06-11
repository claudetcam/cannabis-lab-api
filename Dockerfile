# Étape de base Playwright avec tous les navigateurs
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie ton app
COPY . .

# Ajoute les credentials secrets dans le container (via Render)
RUN mkdir -p /etc/secrets

# Expose port (facultatif)
EXPOSE 10000

# Lancer gunicorn
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:10000"]
