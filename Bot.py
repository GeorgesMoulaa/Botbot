import requests  # Ajout de la bibliothèque requests
import time
import os

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

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
        url = f"{MEXC_API_URL}/api/v3/ticker/price"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):  # Vérifie si la réponse est bien une liste
                return data
            else:
                return {"error": "Réponse invalide"}
        else:
            return {"error": f"Erreur API : {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de connexion : {e}"}

def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices:
        return

    for crypto in prices:
        symbol = crypto["symbol"]
        price = float(crypto["price"])

        # Condition d'exemple pour détecter une opportunité
        if "USDT" in symbol and price < 1:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT")

def main():
    send_telegram_message("🚀 Bot de trading démarré !")

    while True:
        find_trading_opportunity()
        send_telegram_message("🚀 Bot de trading en fonctionnement")
        time.sleep(3600)  # Envoie un message toutes les heures

if __name__ == "__main__":
    main()
