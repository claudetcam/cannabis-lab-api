# scraper.py
import os
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.sync_api import sync_playwright

def run_script():
    print("Début du script...")

    # 1. Authentification Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_path = "/etc/secrets/credentials.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1ZGZdBOn3nbOd7LVOG6-LSQ9jfxGlXEtxhLD7YYvWzd8/edit").sheet1
    sheet.clear()
    sheet.append_row(["Nom du laboratoire", "Type", "Adresse", "Dernière mise à jour", "URL"])

    print("Google Sheet prêt, lancement du scraping...")

    # 2. Scraping avec Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.masscannabiscontrol.com/licensed-marijuana-establishments/", timeout=60000)

        print("Page chargée, traitement des filtres...")

        # Cliquez sur "License Type" et cochez "Independent Testing Laboratory"
        page.locator("button:has-text('License Type')").click()
        page.wait_for_timeout(500)
        page.get_by_label("Independent Testing Laboratory").check()
        page.wait_for_timeout(1000)

        # Cliquez sur "Apply Filters"
        page.get_by_role("button", name="Apply Filters").click()
        page.wait_for_timeout(2000)

        print("Filtre appliqué, lecture des lignes...")

        # Extraction des données
        rows = page.locator("table tbody tr")
        row_count = rows.count()

        for i in range(row_count):
            row = rows.nth(i)
            cols = row.locator("td")
            nom = cols.nth(0).inner_text().strip()
            type_lab = cols.nth(1).inner_text().strip()
            adresse = cols.nth(2).inner_text().strip()
            update = cols.nth(3).inner_text().strip()
            url = cols.nth(0).locator("a").get_attribute("href")

            sheet.append_row([nom, type_lab, adresse, update, url])
            print(f"{i+1}/{row_count} ajouté : {nom}")

        browser.close()

    print("✅ Script terminé avec succès.")
