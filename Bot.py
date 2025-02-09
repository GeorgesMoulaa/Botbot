import requests
import pandas as pd
import numpy as np
import time
from telegram import Bot

# Configuration API et Telegram
api_key = "mx0vgl2Xgrc1HaoPGr"
api_secret = "018fc618575f45eb828af5fed21b5aae"
telegram_token = "8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ"
chat_id = "949838495"

# Initialiser le bot Telegram
bot = Bot(token=telegram_token)

# Fonction pour obtenir des données historiques de MEXC
def get_historical_data(symbol, interval='1m', limit=100):
    url = f'https://api.mexc.com/api/v2/market/kline'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()['data']
    return pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])

# Fonction pour calculer le RSI (Relative Strength Index) avec pandas et numpy
def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Fonction pour envoyer une notification Telegram
def send_telegram_message(message):
    bot.send_message(chat_id=chat_id, text=message)

# Fonction de trading
def trade():
    symbol = 'BTC_USDT'  # Exemple avec le trading de Bitcoin
    data = get_historical_data(symbol)
    data['rsi'] = calculate_rsi(data)

    last_rsi = data['rsi'].iloc[-1]
    print(f'Last RSI: {last_rsi}')

    # Conditions de trading basées sur RSI
    if last_rsi > 70:
        send_telegram_message(f"RSI élevé : {last_rsi}. Vente recommandée.")
    elif last_rsi < 30:
        send_telegram_message(f"RSI faible : {last_rsi}. Achat recommandé.")
    else:
        send_telegram_message(f"RSI neutre : {last_rsi}. Pas de position recommandée.")

# Boucle de trading
while True:
    trade()
    time.sleep(60)  # Attendre une minute avant de vérifier à nouveau
