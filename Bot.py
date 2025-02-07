#import requests
import time
import os
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MEXC_API_URL

# Envoi de message sur Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# Récupération des prix crypto
def get_crypto_prices():
    try:
        url = f"{MEXC_API_URL}/api/v3/ticker/price"  # Assure-toi que l'URL est correcte
        response = requests.get(url)
        
        if response.status_code == 200:  # Vérifie si la réponse de l'API est valide
            data = response.json()
            if isinstance(data, list):
                return data
            else:
                send_telegram_message(f"Erreur : Réponse invalide de l'API")
        else:
            send_telegram_message(f"Erreur API : {response.status_code}")
    except requests.exceptions.RequestException as e:
        send_telegram_message(f"Erreur de connexion : {e}")
    except ValueError:
        send_telegram_message("Erreur de traitement de la réponse JSON")

# Vérifie les opportunités de trading
def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices:
        return

    for crypto in prices:
        symbol = crypto.get("symbol")
        price = float(crypto.get("price", 0))

        if "USDT" in symbol and price < 1:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT")

# Vérifie que le bot fonctionne chaque heure
def send_hourly_update():
    send_telegram_message("🚀 Bot de trading en fonctionnement")
    
# Fonction principale du bot
if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    
    while True:
        find_trading_opportunity()  # Vérifie les opportunités de trading
        send_hourly_update()  # Envoie une mise à jour horaire
        
        time.sleep(3600)  # Attendre une heure avant la prochaine vérification Fonction pour envoyer un message Telegram
