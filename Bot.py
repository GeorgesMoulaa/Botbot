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

def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices:
        return

    # Exemple de stratégie : tu peux ajouter ta logique ici
    for crypto in prices:
        symbol = crypto["symbol"]
        price = float(crypto["price"])

        # Ajouter ici la logique pour filtrer les opportunités
        send_telegram_message(f"Crypto: {symbol}, Prix: {price} USDT")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré")
    
    last_message_time = time.time()  # Temps initial (premier démarrage)
    
    while True:
        find_trading_opportunity()  # Vérifier les prix et envoyer des alertes
        current_time = time.time()
        
        # Vérifier si une heure s'est écoulée
        if current_time - last_message_time >= 3600:  # 3600 secondes = 1 heure
            send_telegram_message("⏰ Le bot est toujours en fonction !")
            last_message_time = current_time  # Réinitialiser l'heure du dernier message
        
        time.sleep(60)  # Vérifier toutes les 60 secondes
