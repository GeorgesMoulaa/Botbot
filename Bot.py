import requests
import time
import talib  # Bibliothèque pour les indicateurs techniques
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MEXC_API_URL

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

# Fonction pour obtenir les prix des cryptos depuis l'API MEXC
def get_crypto_prices():
    try:
        response = requests.get(MEXC_API_URL)
        if response.status_code == 200:
            data = response.json()  # Conversion de la réponse en JSON
            return data
        else:
            return {"error": f"Erreur API: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erreur de connexion: {str(e)}"}

# Fonction pour calculer les indicateurs techniques
def calculate_indicators(prices):
    # Calcul du RSI avec un délai de 14 jours
    rsi = talib.RSI(prices, timeperiod=14)
    
    # Calcul des moyennes mobiles sur 50 et 200 jours
    ma50 = talib.SMA(prices, timeperiod=50)
    ma200 = talib.SMA(prices, timeperiod=200)
    
    # Calcul du MACD
    macd, macd_signal, _ = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    
    # Calcul de l'ADX (pour la force de la tendance)
    adx = talib.ADX(prices, timeperiod=14)
    
    # Calcul de l'ATR (Average True Range) pour mesurer la volatilité
    atr = talib.ATR(prices, timeperiod=14)
    
    # Calcul du Stochastic Oscillator
    slowk, slowd = talib.STOCH(prices, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    
    return rsi, ma50, ma200, macd, macd_signal, adx, atr, slowk, slowd

# Fonction pour analyser les opportunités de trading
def find_trading_opportunity():
    prices_data = get_crypto_prices()  # Récupération des prix
    if not prices_data or "error" in prices_data:
        send_telegram_message(f"Erreur lors de la requête. Code statut: {prices_data.get('error')}")
        return
    
    # Boucle sur chaque crypto pour évaluer les opportunités
    for crypto in prices_data.get('data', []):
        symbol = crypto.get("symbol")
        price = float(crypto.get("last"))
        
        # Récupération des prix historiques
        historical_prices = [float(crypto.get("last")) for crypto in prices_data.get('data', [])]  # Récupère les derniers prix
        
        # Calcul des indicateurs techniques
        rsi, ma50, ma200, macd, macd_signal, adx, atr, slowk, slowd = calculate_indicators(historical_prices)
        
        # Stratégie de trading : condition de succès basée sur les indicateurs
        # Exemple : Signal d'achat si RSI < 30, MACD croise au-dessus du signal, et tendance haussière avec MA50 > MA200.
        if rsi[-1] < 30 and macd[-1] > macd_signal[-1] and ma50[-1] > ma200[-1] and adx[-1] > 25:
            send_telegram_message(f"⚡ Opportunité : {symbol} à {price} USDT. RSI={rsi[-1]}, MACD={macd[-1]}, MA50>{ma200[-1]}, ADX={adx[-1]}")
        elif slowk[-1] < 20 and slowd[-1] < 20:
            send_telegram_message(f"🚨 Vente ou surveiller : {symbol} à {price} USDT. Stochastic oversold. SlowK={slowk[-1]}, SlowD={slowd[-1]}")
        else:
            send_telegram_message(f"Pas d'opportunité de trading pour {symbol} actuellement.")

# Démarrage du bot
if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    while True:
        find_trading_opportunity()  # Vérifier les opportunités
        time.sleep(60)  # Attendre 60 secondes avant la prochaine vérification
