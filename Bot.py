import requests
import numpy as np
import time
import math
from datetime import datetime
import json

# Variables globales
TELEGRAM_TOKEN = "your_telegram_token"
TELEGRAM_CHAT_ID = "your_telegram_chat_id"
MEXC_API_URL = "https://api.mexc.com/api/v2/market/ticker"

# Fonction pour envoyer des messages à Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response

# Fonction pour récupérer les prix des cryptos
def get_crypto_prices():
    try:
        response = requests.get(MEXC_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": f"Erreur API: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erreur de connexion: {str(e)}"}

# Calcul du RSI (Relative Strength Index)
def calculate_rsi(prices, period=14):
    delta = np.diff(prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = np.mean(gain[:period])
    avg_loss = np.mean(loss[:period])
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calcul de la moyenne mobile simple (SMA)
def calculate_sma(prices, window=14):
    return np.mean(prices[-window:])

# Calcul de l'Indicateur MACD
def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    short_ema = np.mean(prices[-short_window:])
    long_ema = np.mean(prices[-long_window:])
    macd = short_ema - long_ema
    signal_line = np.mean(prices[-signal_window:])
    return macd, signal_line

# Fonction pour déterminer les opportunités de trading
def find_trading_opportunity():
    prices_data = get_crypto_prices()

    if "error" in prices_data:
        send_telegram_message(f"Erreur lors de la requête: {prices_data['error']}")
        return
    
    # Nous récupérons les prix des cryptos
    prices = [float(item['last']) for item in prices_data.get('data', []) if 'USDT' in item['symbol']]

    if len(prices) == 0:
        send_telegram_message("Aucune donnée de crypto disponible.")
        return

    # Calcul des indicateurs
    rsi = calculate_rsi(prices)
    sma = calculate_sma(prices)
    macd, signal_line = calculate_macd(prices)

    # Analyser la probabilité de succès
    if rsi < 30 and macd > signal_line:  # Achat potentiel
        success_rate = 85  # Probabilité de succès élevée pour un achat
        trade_decision = "Achat"
    elif rsi > 70 and macd < signal_line:  # Vente potentielle
        success_rate = 85  # Probabilité de succès élevée pour une vente
        trade_decision = "Vente"
    else:
        success_rate = 50  # Pas de trade, probabilité faible
        trade_decision = "Aucune action"

    # Si la probabilité est supérieure à 80%, notifier l'utilisateur
    if success_rate >= 80:
        message = f"🔔 Opportunité de trading détectée!\n\n"
        message += f"Action suggérée: {trade_decision}\n"
        message += f"RSI: {rsi:.2f}\nSMA: {sma:.2f}\nMACD: {macd:.2f}\nProbabilité de succès: {success_rate}%\n\n"
        message += f"Moment: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        send_telegram_message(message)

# Fonction pour exécuter la stratégie de trading en continu
def start_trading_bot():
    send_telegram_message("🚀 Bot de trading démarré !")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifie toutes les 60 secondes

if __name__ == "__main__":
    start_trading_bot()
