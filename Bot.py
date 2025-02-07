import requests  # Ajout de la bibliothèque requests
import time
import os

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MEXC_API_URL  # Assure-toi que MEXC_API_URL est bien défini dans ton fichier config

def send_telegram_message(message):
    """Envoie un message via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def get_crypto_prices():
    """Récupère les prix des cryptos via l'API MEXC."""
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
    """Recherche une opportunité de trading."""
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
    """Fonction principale qui gère la logique du bot."""
    send_telegram_message("🚀 Bot de trading démarré !")
    
    last_message_time = time.time()  # Temps du dernier message envoyé

    while True:
        current_time = time.time()
        
        # Vérifie toutes les heures pour envoyer un message de statut
        if current_time - last_message_time >= 3600:
            send_telegram_message("🚀 Bot de trading en fonctionnement")
            last_message_time = current_time
        
        find_trading_opportunity()  # Recherche des opportunités de trading
        
        time.sleep(60)  # Attendre 60 secondes avant de vérifier à nouveau les opportunités

if __name__ == "__main__":
    main()
