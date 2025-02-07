import requests
import time
import json
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MEXC_API_URL

# Fonction pour envoyer un message Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# Fonction pour obtenir les prix des cryptomonnaies
def get_crypto_prices():
    try:
        url = f"{MEXC_API_URL}/api/v3/ticker/price"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data
            else:
                return {"error": "Réponse invalide de l'API"}
        else:
            return {"error": f"Erreur API : {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de connexion : {e}"}

# Fonction principale pour analyser les opportunités
def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices or "error" in prices:
        send_telegram_message(f"⚠️ Erreur : {prices.get('error', 'Aucune donnée reçue')}")
        return

    for crypto in prices:
        symbol = crypto.get("symbol")
        price = float(crypto.get("price", 0))

        # Condition d'opportunité (ici USDT < 1 par exemple)
        if "USDT" in symbol and price < 1:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT")

# Fonction pour vérifier que le bot fonctionne toutes les heures
def check_bot_status():
    send_telegram_message("🚀 Bot de trading en fonctionnement")

# Lancer les vérifications toutes les heures
if __name__ == "__main__":
    while True:
        find_trading_opportunity()  # Vérifier les opportunités de trading
        check_bot_status()  # Vérifier le bon fonctionnement du bot
        time.sleep(3600)  # Attendre 1 heure (3600 secondes)
