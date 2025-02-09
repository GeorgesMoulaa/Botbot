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
    # Simuler des prix de cryptos pour tester
    prices = [
        {"symbol": "BTCUSDT", "price": 0.5},  # Prix déclencheur
        {"symbol": "ETHUSDT", "price": 1500}, # Prix non déclencheur
    ]
    return prices

def find_trading_opportunity():
    prices = get_crypto_prices()  # Utilisation des prix simulés
    if not prices:
        return
    

    # Exemple de stratégie : détecter une crypto qui répond à un critère
    for crypto in prices:
        symbol = crypto["symbol"]
        price = float(crypto["price"])

        # Condition pour déclencher une notification
        if "USDT" in symbol and price < 1:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré")
    while True:
        find_trading_opportunity()  # Tester à chaque exécution
        time.sleep(60)  # Vérifier toutes les 60 secondes

import requests

def get_crypto_prices():
    url = "https://www.mxc.com/open/api/v2/market/ticker"  # L'URL de l'API MEXC
    params = {
        "symbol": "BTCUSDT"  # Le symbole de la crypto à récupérer
    }
    
    # Envoi de la requête GET à l'API
    response = requests.get(url, params=params)

    # Vérification si la requête est réussie (code 200)
    if response.status_code == 200:
        data = response.json()  # Récupère les données JSON
        print(data)  # Affiche les données reçues
        return data
    else:
        print(f"Erreur lors de la requête. Code statut: {response.status_code}")
        return None

# Appel de la fonction
get_crypto_prices()
