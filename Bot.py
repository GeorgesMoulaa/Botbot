import requests
import time
import numpy as np
import pandas as pd

# Fonction pour envoyer un message via Telegram
def send_telegram_message(chat_id, message, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, data=data)
    response_json = response.json()
    
    # Log du message envoyé
    print(f"Message à envoyer : {message}")
    
    if response_json.get('ok'):
        print("Le message a été envoyé avec succès.")
    else:
        print(f"Erreur d'envoi : {response_json.get('description')}")
    
    return response_json

# Fonction pour démarrer le bot et envoyer un message de démarrage
def start_bot():
    message = "Le bot a démarré avec succès !"
    send_telegram_message(chat_id, message, bot_token)

# Fonction pour obtenir les données de MEXC
def get_mexc_data():
    url = 'https://www.mexc.com/api/v2/market/ticker'
    response = requests.get(url)
    data = response.json()
    return data['data']

# Calcul de la stratégie basée sur des indicateurs (exemple avec Moving Average)
def calculate_trade_probability(data):
    df = pd.DataFrame(data)
    df['price'] = df['last']  # Prix actuel
    df['MA5'] = df['price'].rolling(window=5).mean()  # Moyenne mobile 5 jours
    df['MA20'] = df['price'].rolling(window=20).mean()  # Moyenne mobile 20 jours
    
    # Exemple de stratégie : si MA5 croise MA20 à la hausse, alors on considère une opportunité
    if df['MA5'].iloc[-1] > df['MA20'].iloc[-1]:
        return 85  # Probabilité de succès de 85%
    else:
        return 60  # Pas d'opportunité

# Analyser les opportunités dans le top 1000
def analyze_trade_opportunity():
    data = get_mexc_data()  # Récupérer les données des cryptos
    opportunities = []
    
    for crypto in data[:1000]:  # Top 1000 cryptos
        name = crypto['symbol']
        price = float(crypto['last'])
        
        # Calculer la probabilité du trade pour cette crypto
        probability = calculate_trade_probability([crypto])  # Exemple simplifié
        print(f"Vérification de {name}: Probabilité = {probability}%")
        
        if probability > 80:  # Si la probabilité est > 80%, on envoie le trade
            opportunity = {
                'name': name,
                'price': price,
                'probability': probability,
                'entry': price,
                'target': price * 1.05,  # Objectif de 5% de gain
                'stop_loss': price * 0.98  # Stop loss à -2%
            }
            opportunities.append(opportunity)
    
    return opportunities

# Fonction principale
def main():
    start_bot()  # Démarrer le bot et envoyer un message de démarrage

    while True:
        opportunities = analyze_trade_opportunity()
        
        if opportunities:
            for opportunity in opportunities:
                message = (
                    f"Opportunité de trade détectée pour {opportunity['name']} :\n"
                    f"- Prix actuel : {opportunity['price']}\n"
                    f"- Prix d'entrée : {opportunity['entry']}\n"
                    f"- Objectif de profit (5%) : {opportunity['target']}\n"
                    f"- Stop loss (-2%) : {opportunity['stop_loss']}\n"
                    f"Probabilité de succès : {opportunity['probability']}%"
                )
                send_telegram_message(chat_id, message, bot_token)  # Envoyer le message Telegram
                print(f"Opportunité envoyée: {message}")
        
        time.sleep(30)  # Attendre 30 secondes avant de vérifier à nouveau

# ID de chat et token du bot
chat_id = '949838495'  # Remplacez par votre ID de chat
bot_token = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'  # Remplacez par votre token

# Démarrer le bot
main()
