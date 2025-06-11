from flask import Flask
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

app = Flask(__name__)

@app.route("/")
def run_script():
    # Étape 1 : Authentification Google Sheets
    json_keyfile = "/etc/secrets/credentials.json"
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ZGZdBOn3nbOd7LVOG6-LSQ9jfxGlXEtxhLD7YYvWzd8/edit"

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_url(spreadsheet_url).worksheet("Labs-Massachusetts")

    # Étape 2 : Configuration Chromium headless pour Render
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
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

    # Étape 3 : Mise à jour Google Sheet
    sheet.resize(rows=3)
    sheet.update("A4", labs)

    return f"{len(labs)} laboratoires actifs mis à jour avec succès ✅"
