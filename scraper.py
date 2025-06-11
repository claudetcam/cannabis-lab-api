import threading
from playwright.sync_api import sync_playwright
import time

def run_script():
    print("🔧 Lancement du script de scraping...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url = "https://masscannabiscontrol.com/list-of-licensees/"
        page.goto(url)
        print("✅ Page chargée")

        # Attendre que la page se charge complètement
        page.wait_for_timeout(5000)

        # DEBUG : Sauvegarder le HTML pour analyse
        html = page.content()
        with open("page_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("📄 HTML sauvegardé dans 'page_debug.html'")

        # Essayer de cliquer sur le bouton
        try:
            page.locator("button:has-text('License Type')").click()
            print("✅ Bouton 'License Type' cliqué")
        except Exception as e:
            print("❌ Erreur lors du clic sur le bouton :", e)

        browser.close()

# Lancer le script dans un thread au démarrage
threading.Thread(target=run_script).start()
