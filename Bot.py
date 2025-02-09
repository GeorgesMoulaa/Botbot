import requests
import time
import logging
from talib import RSI, SMA
import numpy as np

# Configuration Telegram
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Initialisation des logs pour le débogage
logging.basicConfig(level=logging.DEBUG)

# Fonction pour envoyer des messages via Telegram
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            logging.debug(f"Message envoyé : {message}")
        else:
            logging.error(f"Erreur Telegram : {response.status_code}, {response.text}")
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi du message Telegram : {e}")

# Fonction pour récupérer les prix des cryptos via l'API MEXC
def get_crypto_prices():
    try:
        MEXC_API_URL = "https://www.mexc.com/api/v2/market/ticker"
        response = requests.get(MEXC_API_URL)
        
        if response.status_code == 200:
            data = response.json()
            logging.debug(f"Prix actuel : {data}")  # Afficher les prix pour vérification
            return data
        else:
            logging.error(f"Erreur API MEXC : {response.status_code}, {response.text}")
            return {"error": f"Erreur API MEXC : {response.status_code}"}
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des prix : {e}")
        return {"error": f"Erreur de connexion : {e}"}

# Appliquer les indicateurs (RSI, SMA) pour déterminer les opportunités
def calculate_indicators(prices):
    close_prices = np.array([price['last'] for price in prices])
    
    # Calcul du RSI (Relative Strength Index) et SMA (Simple Moving Average)
    rsi = RSI(close_prices, timeperiod=14)  # 14 périodes pour le RSI
    sma = SMA(close_prices, timeperiod=50)  # 50 périodes pour la SMA
    
    return rsi[-1], sma[-1]  # Retourne les dernières valeurs du RSI et SMA

# Fonction pour détecter les opportunités de trading
def find_trading_opportunity():
    prices = get_crypto_prices()
    
    if not prices or "error" in prices:
        send_telegram_message(f"Erreur lors de la requête. Code statut: {prices.get('error')}")
        return
    
    # Appliquer les indicateurs techniques sur les données récupérées
    rsi, sma = calculate_indicators(prices['data'])
    
    # Condition de la stratégie (80% de probabilité avec des indicateurs)
    if rsi < 30 and sma < np.mean([price['last'] for price in prices['data']]):  # Par exemple RSI faible et SMA en dessous du prix moyen
        send_telegram_message(f"⚡ Opportunité détectée : RSI={rsi}, SMA={sma}")
        logging.debug(f"Opportunité trouvée avec RSI={rsi} et SMA={sma}")

if __name__ == "__main__":
    logging.debug('Bot démarré avec les configurations suivantes : ')
    logging.debug(f"Token: {TELEGRAM_TOKEN}")
    logging.debug(f"Chat ID: {TELEGRAM_CHAT_ID}")

    send_telegram_message("🚀 Bot de trading démarré !")
    
    while True:
        find_trading_opportunity()  # Vérifier les opportunités toutes les minutes
        time.sleep(60)  # Attendre 60 secondes avant de vérifier à nouveau
