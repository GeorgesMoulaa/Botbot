import requests
import time
import json

# Remplir vos informations Telegram
TELEGRAM_TOKEN = "VOTRE_BOT_TOKEN"
TELEGRAM_CHAT_ID = "VOTRE_CHAT_ID"

# URL de l'API MEXC pour récupérer les prix des cryptos
MEXC_API_URL = "https://www.mexc.com/api/v2/market/ticker"

# Envoie un message sur Telegram
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
            return data['data']  # Afficher les données de prix
        else:
            return {"error": f"Erreur API: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erreur de connexion: {str(e)}"}

# Calcul de la moyenne mobile simple (SMA) sur les dernières valeurs de prix
def calculate_sma(prices, period=14):
    if len(prices) < period:
        return None
    sma = sum(prices[-period:]) / period
    return sma

# Calcul du RSI (Relative Strength Index) avec une période par défaut de 14
def calculate_rsi(prices, period=14):
    if len(prices) < period:
        return None

    gains = 0
    losses = 0
    for i in range(1, period+1):
        change = prices[-i] - prices[-(i+1)]
        if change > 0:
            gains += change
        else:
            losses -= change

    avg_gain = gains / period
    avg_loss = losses / period

    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Fonction principale pour détecter des opportunités de trading
def find_trading_opportunity():
    prices_data = get_crypto_prices()
    if not prices_data or "error" in prices_data:
        send_telegram_message(f"Erreur lors de la requête. Code statut: {prices_data.get('error')}")
        return

    for crypto in prices_data:
        symbol = crypto.get("symbol")
        price = float(crypto.get("last"))
        price_list = [float(item.get("last")) for item in prices_data if item.get("symbol") == symbol]

        # Calculs d'indicateurs
        sma = calculate_sma(price_list)
        rsi = calculate_rsi(price_list)

        if sma is not None and rsi is not None:
            # Conditions d'opportunité basées sur la SMA et le RSI
            if price < sma and rsi < 30:  # RSI < 30 est souvent un signal de survente
                message = f"⚡ Opportunité : {symbol} à {price} USDT\n- RSI: {rsi:.2f} (survendu)\n- Prix sous SMA: {sma:.2f}"
                send_telegram_message(message)
            elif price > sma and rsi > 70:  # RSI > 70 est souvent un signal de surachat
                message = f"⚡ Opportunité : {symbol} à {price} USDT\n- RSI: {rsi:.2f} (suracheté)\n- Prix au-dessus SMA: {sma:.2f}"
                send_telegram_message(message)

# Démarrer le bot
if __name__ == "__main__":
    send_telegram_message("🚀 Bot de trading démarré !")
    while True:
        find_trading_opportunity()
        time.sleep(60)  # Vérifier toutes les 60 secondes
