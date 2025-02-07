import requests
import time
import json
import os 
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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:  # Vérifie si la requête a réussi
            try:
                data = response.json()
                if isinstance(data, list):  # Vérifie que c'est une liste de prix
                    print("Réponse API:", data)  # Log pour debug
                    return data
                else:
                    return {"error": "Réponse invalide"}
            except ValueError:
                return {"error": "Impossible de convertir la réponse en JSON"}
        else:
            return {"error": f"Erreur API : {response.status_code} - {response.text}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de connexion : {e}"}

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
    if not os.path.exists("bot_started.txt"):  # Vérifie si le fichier existe
        send_telegram_message("🚀 Bot de trading démarré !")
        open("bot_started.txt", "w").close()  # Crée un fichier pour éviter le spam

    while True:
        find_trading_opportunity()
        time.sleep(60)
