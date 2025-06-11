from flask import Flask
import threading
from scraper import run_script

app = Flask(__name__)

@app.route("/")
def run():
    threading.Thread(target=run_script).start()
    return "✅ Script lancé en arrière-plan", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
