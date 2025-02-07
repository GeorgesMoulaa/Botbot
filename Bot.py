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
        # Simuler des prix
        prices = [
            {"symbol": "BTCUSDT", "price": 0.5},  # Prix déclencheur
            {"symbol": "ETHUSDT", "price": 1500}, # Prix non déclencheur
        ]
        return prices
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de connexion : {e}"}

def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices:
        return

    # Exemple de stratégie : détecter une crypto qui répond à la condition
    for crypto in prices:
        symbol = crypto["symbol"]
        price = float(crypto["price"])

        # Si la crypto est USDT et son prix est inférieur à 1
        if "USDT" in symbol and price < 1:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
