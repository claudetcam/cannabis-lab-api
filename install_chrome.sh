#!/usr/bin/env bash
set -x

# Télécharger et installer Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Création du lien symbolique attendu par Selenium
ln -s /usr/bin/google-chrome-stable /usr/bin/google-chrome

# Nettoyage
rm google-chrome-stable_current_amd64.deb
