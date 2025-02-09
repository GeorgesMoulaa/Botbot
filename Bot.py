import requests
import time

# Fonction pour envoyer un message via Telegram
def send_telegram_message(chat_id, message, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    
    # Log du message envoyé
    print(f"Message à envoyer : {message}")
    
    response = requests.post(url, data=data)
    response_json = response.json()
    
    print(f"Réponse Telegram : {response_json}")
    
    if response_json.get('ok'):
        print("Le message a été envoyé avec succès.")
    else:
        print(f"Erreur d'envoi : {response_json.get('description')}")
    
    return response_json

# Fonction pour démarrer le bot et envoyer un message de démarrage
def start_bot():
    message = "Le bot a démarré avec succès !"
    send_telegram_message(chat_id, message, bot_token)

# Fonction qui simule l'analyse d'une opportunité de trading
def analyze_trade_opportunity():
    # Simuler l'analyse de la probabilité d'un trade
    trade_probability = 85  # Probabilité simulée (à remplacer par votre propre logique d'analyse)

    # Si la probabilité d'un trade est supérieure à 80 %, envoie un message avec les détails
    if trade_probability > 80:
        message = f"Nouvelle opportunité de trade détectée avec une probabilité de succès de {trade_probability}%.\n\n" \
                  "Voici ce que vous devez faire :\n" \
                  "- Entrez sur le marché au prix actuel.\n" \
                  "- Fixez un stop loss à 2% en dessous du prix d'entrée.\n" \
                  "- Visez un objectif de profit de 5%.\n" \
                  "- Surveillez la tendance et ajustez en fonction des indicateurs."
        send_telegram_message(chat_id, message, bot_token)
        print(f"Nouvelle opportunité envoyée: {message}")
    else:
        print(f"Aucune opportunité détectée avec une probabilité supérieure à 80%.")

# Fonction principale
def main():
    start_bot()  # Démarrer le bot et envoyer un message de démarrage

    while True:
        analyze_trade_opportunity()  # Analyser une opportunité de trade
        time.sleep(30)  # Attendre 30 secondes avant de vérifier à nouveau

# ID de chat et token du bot
chat_id = '949838495'  # Remplacez par votre ID de chat
bot_token = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'  # Remplacez par votre token

# Démarrer le bot
main()
