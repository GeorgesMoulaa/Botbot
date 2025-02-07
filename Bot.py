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
        url = f"{MEXC_API_URL}/api/v3/ticker/price"
        response = requests.get(url)
        
        if response.status_code == 200:  # Vérifie si la réponse est OK
            try:
                data = response.json()
                if isinstance(data, list):  # Vérifie si 'data' est une liste
                    print("Réponse API:", data)  # Affiche les données de l'API pour déboguer
                    return data
                else:
                    return {"error": "Réponse invalide"}
            except ValueError:
                return {"error": "Impossible de convertir la réponse"}
        else:
            return {"error": f"Erreur API : {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de connexion : {e}"}

def find_trading_opportunity():
    prices = get_crypto_prices()
    
    if not prices:
        send_telegram_message("Erreur: Impossible de récupérer les prix.")
        return
    
    # Vérifie le format des données
    print(prices)  # Affiche la structure de 'prices'

    for crypto in prices:
        # Vérifie si 'crypto' est un dictionnaire avant d'essayer d'y accéder
        if isinstance(crypto, dict):
            symbol = crypto.get("symbol", "")
            price = float(crypto.get("price", 0))
            if "USDT" in symbol and price < 1:
                send_telegram_message(f"⚡ Opportunité détectée : {symbol} à {price}")
        else:
            print("Données mal formatées:", crypto)

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
