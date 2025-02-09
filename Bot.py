import os
import time
import requests
import numpy as np
import pandas as pd
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Insère tes informations API ici
MEXC_API_KEY = 'mx0vgl2Xgrc1HaoPGr'  # Ton API Key MEXC
MEXC_API_SECRET = '018fc618575f45eb828af5fed21b5aae'  # Ton Secret Key MEXC
TELEGRAM_TOKEN = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'  # Ton token Telegram
TELEGRAM_CHAT_ID = '949838495'  # Ton ID Telegram

# Initialiser le bot Telegram
bot = Bot(TELEGRAM_TOKEN)

# Fonction d'envoi d'une notification
def send_telegram_notification(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Fonction qui analyse les opportunités de trading
def analyze_trade_opportunity():
    # Exemple basique de conditions d'opportunité de trading, que tu peux ajuster
    # On peut ajouter des critères comme le RSI, Moving Average, etc.
    opportunities = []

    # Exemple fictif de données de trading
    symbols = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']  # Liste des paires à surveiller

    for symbol in symbols:
        # Ici tu devras intégrer l'API MEXC pour récupérer des données réelles
        response = requests.get(f'https://api.mexc.com/api/v2/market/ticker?symbol={symbol}')
        data = response.json()
        if 'data' in data:
            last_price = float(data['data'][0]['last'])
            if last_price > 50000:  # Exemple de condition pour identifier une opportunité
                opportunities.append(f"Opportunity found for {symbol} at {last_price}")

    return opportunities

# Fonction principale
def main():
    while True:
        opportunities = analyze_trade_opportunity()

        if opportunities:
            for opportunity in opportunities:
                send_telegram_notification(opportunity)

        time.sleep(30)  # Attente de 30 secondes avant la prochaine analyse

if __name__ == "__main__":
    main()
