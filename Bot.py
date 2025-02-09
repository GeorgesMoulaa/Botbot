import pip
import time
import requests
import numpy as np  # On importe numpy ici

# Installer numpy si non installé (uniquement pour Pythonista)
try:
    import numpy
except ImportError:
    pip.main(['install', 'numpy'])

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MEXC_API_URL

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response

def get_crypto_prices():
    try:
        response = requests.get(MEXC_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": f"Erreur API : {response.status_code}"}
    except Exception as e:
        return {"error": f"Erreur de connexion : {str(e)}"}

def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices or "error" in prices:
        send_telegram_message(f"Erreur lors de la requête. Code statut: {prices.get('error')}")
        return

    # Utilisation de numpy pour l'analyse (exemple simple avec calcul de moyenne)
    price_data = [float(crypto.get("last", 0)) for crypto in prices.get("data", []) if "USDT" in crypto.get("symbol", "")]
    if len(price_data) == 0:
        return

    # Utilisation de numpy pour calculer la moyenne des prix
    avg_price = np.mean(price_data)
    send_telegram_message(f"Prix moyen des cryptos USDT: {avg_price:.2f} USDT")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
