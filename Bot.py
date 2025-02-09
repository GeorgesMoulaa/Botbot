import requests
import time
import pandas as pd
import talib
import numpy as np
from binance.client import Client
from binance.enums import *

# Variables d'API
MEXC_API_KEY = 'mx0vgl2Xgrc1HaoPGr'
MEXC_API_SECRET = '018fc618575f45eb828af5fed21b5aae'
TELEGRAM_TOKEN = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'
TELEGRAM_CHAT_ID = '949838495'

# Fonction pour envoyer un message sur Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Fonction pour obtenir les données de marché de MEXC
def get_crypto_prices():
    url = f'https://www.mexc.com/api/v2/market/tickers'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()['data']

# Fonction pour analyser une crypto et vérifier la stratégie des 80%
def analyze_crypto(crypto):
    symbol = crypto['symbol']
    price = float(crypto['last'])

    # Vérifier les indicateurs avec des conditions de trading
    # Exemple pour RSI (Relative Strength Index)
    historical_data = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")
    close_prices = [float(candle[4]) for candle in historical_data]  # On prend le prix de clôture
    
    # Calculer RSI avec TALIB
    rsi = talib.RSI(np.array(close_prices), timeperiod=14)[-1]
    
    # Stratégie 80% : Si RSI est inférieur à 30, c'est un signal d'achat
    if rsi < 30:
        send_telegram_message(f"🚀 Opportunité : {symbol} à {price} USDT. RSI bas détecté : {rsi}")
        return True
    return False

# Fonction principale pour rechercher des opportunités
def find_trading_opportunity():
    prices = get_crypto_prices()
    
    for crypto in prices:
        if 'USDT' in crypto['symbol']:  # Filtrer les cryptos avec USDT
            if analyze_crypto(crypto):
                print(f"Notification envoyée pour {crypto['symbol']}")

# Fonction principale
if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
