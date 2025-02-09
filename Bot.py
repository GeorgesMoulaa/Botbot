import os
import requests
import time
import telegram

# Configurations Telegram
TELEGRAM_TOKEN = "8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ"
TELEGRAM_CHAT_ID = "949838495"  # Remplace par ton ID de chat Telegram

# Initialisation du bot Telegram
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Fonction pour envoyer un message à Telegram
def send_telegram_notification(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("Message envoyé : ", message)
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")

# Fonction pour analyser les opportunités
def analyze_trade_opportunity():
    print("Analyse des opportunités de trading en cours...")
    opportunities = []

    symbols = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']  # Liste de symboles à vérifier

    for symbol in symbols:
        try:
            response = requests.get(f'https://api.mexc.com/api/v2/market/ticker?symbol={symbol}')
            data = response.json()

            if 'data' in data:
                last_price = float(data['data'][0]['last'])
                print(f"Prix actuel pour {symbol}: {last_price}")  # Afficher dans le log

                if last_price > 50000:  # Condition exemple pour une opportunité
                    opportunities.append(f"Opportunity found for {symbol} at {last_price}")
            else:
                print(f"Aucune donnée pour {symbol}")
        
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {symbol} : {e}")
    
    return opportunities

# Fonction principale
def main():
    send_telegram_notification("Bot démarré avec succès")  # Test démarrage
    while True:
        print("Vérification des opportunités...")
        opportunities = analyze_trade_opportunity()

        if opportunities:
            for opportunity in opportunities:
                send_telegram_notification(opportunity)
        
        time.sleep(30)

if __name__ == "__main__":
    main()
