from flask import Flask
import os
import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route("/")
def run_script():
    # Étape 1 : Authentification Google Sheets depuis variable d’environnement
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ZGZdBOn3nbOd7LVOG6-LSQ9jfxGlXEtxhLD7YYvWzd8/edit"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Charger la clé JSON depuis la variable d'environnement
    credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
    credentials_dict = json.loads(credentials_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_url(spreadsheet_url).worksheet("Labs-Massachusetts")

    # Étape 2 : Scraping
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://masscannabiscontrol.com/licensing-tracker/")
    time.sleep(5)

    elements = driver.find_elements(By.CLASS_NAME, "licensee")
    labs = []

    for el in elements:
        try:
            parent = el.find_element(By.XPATH, "..")
            name = el.text.strip()
            license_type = parent.find_element(By.CLASS_NAME, "license-type").text.strip()
            location = parent.find_element(By.CLASS_NAME, "license-location").text.strip()
            priority = parent.find_element(By.CLASS_NAME, "license-priority").text.strip()
            summary = parent.find_element(By.CLASS_NAME, "executive-summary").text.strip()

            if "Independent Testing Laboratory" in license_type:
                labs.append([name, license_type, location, priority, summary, "", "", "Active"])
        except Exception as e:
            print("Erreur sur un élément:", e)
            continue

    driver.quit()

    # Étape 3 : Mise à jour du Google Sheet
    sheet.resize(rows=3)
    sheet.update("A4", labs)

    return f"{len(labs)} laboratoires actifs mis à jour avec succès ✅"
