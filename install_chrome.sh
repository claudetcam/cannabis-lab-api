#!/usr/bin/env bash
set -x

# Installer les dépendances
apt-get update && apt-get install -y wget curl unzip gnupg2

# Télécharger Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Installer Chrome
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Créer un lien symbolique à l’emplacement attendu par Selenium
mkdir -p /opt/google/chrome
ln -s /usr/bin/google-chrome /opt/google/chrome/google-chrome

# Nettoyage
rm google-chrome-stable_current_amd64.deb
