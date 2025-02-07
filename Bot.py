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

    # Exemple de stratégie simple pour détecter les cryptos
    for crypto in prices:
        symbol = crypto["symbol"]
        price = float(crypto["price"])

        # Envoie un message pour chaque crypto détectée
        send_telegram_message(f"Crypto: {symbol}, Prix: {price} USDT")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré")
    
    last_message_time = time.time()  # Temps initial du dernier message d'état
    
    while True:
        find_trading_opportunity()  # Vérifie les prix des cryptos
        current_time = time.time()
        
        # Vérifie si une heure s'est écoulée (3600 secondes)
        if current_time - last_message_time >= 3600:
            send_telegram_message("⏰ Le bot est toujours en fonction !")  # Message d'état
            last_message_time = current_time  # Réinitialise le compteur du temps
        
        time.sleep(60)  # Attendre 60 secondes avant de refaire un check
