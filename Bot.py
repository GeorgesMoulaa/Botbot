import requests
import time
import json
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MEXC_API_URL

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def get_crypto_prices():
    try:
        response = requests.get(f"{MEXC_API_URL}/api/v3/ticker/price")
        return response.json()
    except Exception as e:
        send_telegram_message(f"Erreur lors de la récupération des prix : {str(e)}")
        return None

def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices:
        return

    # Exemple de stratégie : détecter une crypto qui a chuté de plus de 5% en 24h
    for crypto in prices:
        symbol = crypto["symbol"]
        price = float(crypto["price"])
        # Ici tu peux ajouter une vraie logique de détection d'opportunité

        if "USDT" in symbol and price < 1:  # Condition basique pour tester
            send_telegram_message(f"⚡ Opportunité détectée : {symbol} à {price} USDT !")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
