import requests
import time
import json
import numpy as np
import pandas as pd
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Fonction pour envoyer un message sur Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response

# Fonction pour récupérer les prix des cryptos via l'API MEXC
def get_crypto_prices():
    try:
        MEXC_API_URL = "https://api.mexc.com/api/v2/market/ticker"  # URL MEXC
        response = requests.get(MEXC_API_URL)
        if response.status_code == 200:
            data = response.json()
            print(f"Réponse brute: {data}")  # Affiche la réponse brute pour le débogage
            return data
        else:
            return {"error": f"Erreur API: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de connexion: {str(e)}"}

# Calcul du RSI
def calculate_rsi(data, window=14):
    close_prices = np.array([item['last'] for item in data])
    delta = np.diff(close_prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = np.convolve(gain, np.ones((window,))/window, mode='valid')
    avg_loss = np.convolve(loss, np.ones((window,))/window, mode='valid')
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi[-1]  # Dernier RSI

# Calcul du MACD
def calculate_macd(data, slow=26, fast=12, signal=9):
    close_prices = np.array([item['last'] for item in data])
    fast_ema = pd.Series(close_prices).ewm(span=fast).mean()
    slow_ema = pd.Series(close_prices).ewm(span=slow).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal).mean()
    macd_value = macd[-1]
    signal_value = signal_line[-1]
    return macd_value, signal_value

# Vérification des opportunités en fonction du RSI et du MACD
def find_trading_opportunity():
    prices = get_crypto_prices()
    if not prices or "error" in prices:
        send_telegram_message(f"Erreur lors de la requête. Code statut: {prices.get('error')}")
        return

    # Stratégie avec RSI et MACD pour déterminer les opportunités
    for crypto in prices.get('data', []):
        symbol = crypto.get("symbol")
        price = float(crypto.get("last"))
        
        # Calcul des indicateurs RSI et MACD
        rsi = calculate_rsi(prices.get('data', []))  # Calcul du RSI
        macd, signal = calculate_macd(prices.get('data', []))  # Calcul du MACD

        # Condition pour une opportunité d'achat (RSI < 30 et MACD croise au-dessus du signal)
        opportunity_probability = 0

        if rsi < 30 and macd > signal:  # Survente + signal MACD bullish
            opportunity_probability = 0.85  # Exemple d'une probabilité de 85%

        # Condition pour une opportunité de vente (RSI > 70 et MACD croise en-dessous du signal)
        elif rsi > 70 and macd < signal:  # Surachat + signal MACD bearish
            opportunity_probability = 0.85  # Exemple d'une probabilité de 85%

        # Vérification si la probabilité d'opportunité est supérieure à 80%
        if opportunity_probability >= 0.80:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT | RSI: {rsi:.2f} | MACD: {macd:.2f} | Signal: {signal:.2f}")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
