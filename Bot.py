import time
import requests
import pandas as pd
import numpy as np
from telegram import Bot

# Configuration de votre bot Telegram
TELEGRAM_TOKEN = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'  # Token Telegram
CHAT_ID = '949838495'  # ID du chat Telegram

# Configuration de l'API MEXC
MEXC_API_KEY = 'mx0vgl2Xgrc1HaoPGr'  # API Key MEXC
MEXC_API_SECRET = '018fc618575f45eb828af5fed21b5aae'  # API Secret MEXC

# Fonction pour envoyer un message sur Telegram
def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Fonction pour récupérer les données du marché MEXC
def get_market_data():
    url = "https://api.mexc.com/api/v2/market/ticker"
    response = requests.get(url)
    data = response.json()
    return data

# Calcul de l'indicateur RSI
def calculate_rsi(data, window=14):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Calcul de l'indicateur MACD
def calculate_macd(data, fast=12, slow=26, signal=9):
    fast_ema = data['close'].ewm(span=fast, min_periods=fast).mean()
    slow_ema = data['close'].ewm(span=slow, min_periods=slow).mean()
    macd = fast_ema - slow_ema
    macd_signal = macd.ewm(span=signal, min_periods=signal).mean()
    
    return macd, macd_signal

# Calcul de l'indicateur EMA
def calculate_ema(data, span=50):
    ema = data['close'].ewm(span=span, adjust=False).mean()
    return ema

# Fonction pour analyser les opportunités de trading
def analyze_trade_opportunity():
    market_data = get_market_data()
    
    opportunities = []

    for crypto in market_data['data']:
        symbol = crypto['symbol']
        url = f'https://api.mexc.com/api/v2/market/kline?symbol={symbol}&interval=1m&limit=100'
        response = requests.get(url)
        data = response.json()['data']

        # Convertir les données en DataFrame
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['close'] = df['close'].astype(float)

        # Calcul des indicateurs
        rsi = calculate_rsi(df)
        macd, macd_signal = calculate_macd(df)
        ema = calculate_ema(df)

        # Dernier RSI, MACD et EMA
        latest_rsi = rsi.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_macd_signal = macd_signal.iloc[-1]
        latest_ema = ema.iloc[-1]

        # Vérification des conditions pour une opportunité (stratégie simple)
        if latest_rsi < 30 and latest_macd > latest_macd_signal and df['close'].iloc[-1] > latest_ema:
            opportunities.append(f"Opportunité : {symbol} - RSI : {latest_rsi:.2f}, MACD : {latest_macd:.2f}, EMA : {latest_ema:.2f}. Acheter maintenant !")
        
        elif latest_rsi > 70 and latest_macd < latest_macd_signal and df['close'].iloc[-1] < latest_ema:
            opportunities.append(f"Opportunité : {symbol} - RSI : {latest_rsi:.2f}, MACD : {latest_macd:.2f}, EMA : {latest_ema:.2f}. Vendre maintenant !")
    
    return opportunities

# Fonction principale pour exécuter le bot
def main():
    while True:
        opportunities = analyze_trade_opportunity()
        if opportunities:
            for opportunity in opportunities:
                send_telegram_message(opportunity)
        time.sleep(30)  # Attendre 30 secondes avant de chercher à nouveau

# Lancer le bot
if __name__ == '__main__':
    main()
