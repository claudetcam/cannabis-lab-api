#!/usr/bin/env bash

# Installer les dépendances
apt-get update
apt-get install -y wget gnupg unzip

# Ajouter la clé et le dépôt de Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Installer Google Chrome
apt-get update
apt-get install -y google-chrome-stable

# Créer le dossier et le lien attendu par Selenium
mkdir -p /opt/google/chrome
ln -s /usr/bin/google-chrome /opt/google/chrome/google-chrome
