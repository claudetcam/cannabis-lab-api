from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def run_script():
    try:
        # Authentification Google Sheets
        json_keyfile = "/etc/secrets/credentials.json"
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ZGZdBOn3nbOd7LVOG6-LSQ9jfxGlXEtxhLD7YYvWzd8/edit"

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(spreadsheet_url).worksheet("Labs-Massachusetts")

        labs = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://masscannabiscontrol.com/licensing-tracker/")
            page.wait_for_timeout(5000)

            licensees = page.query_selector_all(".licensee")

            for el in licensees:
                try:
                    parent = el.evaluate_handle("el => el.closest('.license-row')")
                    name = el.inner_text().strip()
                    license_type = parent.query_selector(".license-type").inner_text().strip()
                    location = parent.query_selector(".license-location").inner_text().strip()
                    priority = parent.query_selector(".license-priority").inner_text().strip()
                    summary = parent.query_selector(".executive-summary").inner_text().strip()

                    if "Independent Testing Laboratory" in license_type:
                        labs.append([name, license_type, location, priority, summary, "", "", "Active"])
                except Exception as e:
                    print("Erreur sur un élément:", e)
                    continue

            browser.close()

        # Mise à jour Google Sheets
        sheet.resize(rows=3)
        sheet.update("A4", labs)

        print(f"{len(labs)} laboratoires actifs mis à jour avec succès ✅")  # 🐛 debug console

        return f"{len(labs)} laboratoires actifs mis à jour avec succès ✅"
    
    except Exception as e:
        print("❌ Une erreur est survenue :", e)
        return f"❌ Erreur lors de l'exécution : {e}"
