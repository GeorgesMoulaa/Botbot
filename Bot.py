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
    response = requests.post(url, json=payload)
    return response

def get_crypto_prices():
    try:
        response = requests.get(MEXC_API_URL)
        if response.status_code == 200:
            data = response.json()
            print("Prix actuel:", data)  # Afficher les données des prix
            return data
        else:
            return {"error": f"Erreur API: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erreur de connexion: {str(e)}"}

def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices or "error" in prices:
        send_telegram_message(f"Erreur lors de la requête. Code statut: {prices.get('error')}")
        return
    
    for crypto in prices.get('data', []):  # Utiliser 'data' pour extraire les informations
        symbol = crypto.get("symbol")
        price = float(crypto.get("last"))
        
        # Condition pour déclencher une notification
        if "USDT" in symbol and price < 1:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
