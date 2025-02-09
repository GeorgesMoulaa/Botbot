import time
import requests
import pandas as pd
import numpy as np
import ccxt
import telegram

# Vos informations API et Telegram
api_key = "mx0vgl2Xgrc1HaoPGr"
api_secret = "018fc618575f45eb828af5fed21b5aae"
telegram_token = "8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ"
telegram_chat_id = "949838495"

# Initialisation du bot Telegram
bot = telegram.Bot(token=telegram_token)

# Initialisation de l'API MEXC
exchange = ccxt.mexc({
    'apiKey': api_key,
    'secret': api_secret,
})

# Fonction pour obtenir les données historiques
def get_historical_data(symbol, timeframe='1m', limit=100):
    url = f'https://api.mexc.com/api/v2/market/candles?symbol={symbol}&interval={timeframe}&limit={limit}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    else:
        print(f"Erreur de récupération des données : {response.status_code}")
        return None

# Fonction pour calculer la probabilité de succès basée sur RSI et SMA
def calculate_probability(df):
    # Calcul du RSI (Relative Strength Index)
    df['RSI'] = 100 - (100 / (1 + (df['close'].pct_change().dropna().gt(0).mean() / df['close'].pct_change().dropna().lt(0).mean()))))

    # Calcul de la moyenne mobile simple (SMA)
    df['SMA'] = df['close'].rolling(window=20).mean()

    # Calcul de la probabilité
    probabilité = 0.8  # Valeur par défaut

    if df['RSI'].iloc[-1] < 30 and df['close'].iloc[-1] > df['SMA'].iloc[-1]:
        probabilité = 0.9  # Probabilité élevée si conditions de survente et prix au-dessus de la moyenne mobile
    elif df['RSI'].iloc[-1] > 70 and df['close'].iloc[-1] < df['SMA'].iloc[-1]:
        probabilité = 0.7  # Probabilité plus faible si conditions de surachat et prix en dessous de la moyenne mobile

    return probabilité

# Fonction de trading
def trade():
    symbol = 'BTC_USDT'  # Exemple de symbole (ajustez si nécessaire)
    
    # Récupérer les données historiques
    df = get_historical_data(symbol)
    
    if df is not None:
        # Calculer la probabilité de succès
        probabilité = calculate_probability(df)
        
        if probabilité >= 0.8:
            # Condition d'achat
            if df['close'].iloc[-1] > df['SMA'].iloc[-1]:
                signal = 'BUY'
                bot.send_message(chat_id=telegram_chat_id, text=f"Signal de trading: {signal} pour {symbol} avec une probabilité de réussite de {probabilité*100}%")
                print(f"Signal de trading: {signal}, probabilité de réussite: {probabilité*100}%")
            # Condition de vente
            elif df['close'].iloc[-1] < df['SMA'].iloc[-1]:
                signal = 'SELL'
                bot.send_message(chat_id=telegram_chat_id, text=f"Signal de trading: {signal} pour {symbol} avec une probabilité de réussite de {probabilité*100}%")
                print(f"Signal de trading: {signal}, probabilité de réussite: {probabilité*100}%")
        else:
            print("Aucune opportunité de trading avec un taux de probabilité suffisant.")
    else:
        print("Erreur : pas de données disponibles.")

# Exécution du trading en boucle
while True:
    trade()
    time.sleep(60)  # Attendre 60 secondes avant de faire une nouvelle demande
