import requests
import random
import time

# Fonction pour envoyer des messages via l'API Telegram
def send_telegram_message(chat_id, message, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

# Fonction pour analyser une opportunité (exemple avec un score aléatoire ici)
def analyze_trade_opportunity():
    # Remplacer cette logique par des calculs réels
    score = random.randint(50, 100)  # Simuler un score entre 50 et 100
    return score

# Fonction principale du bot
def main():
    chat_id = '949838495'  # Remplacez par votre ID de chat
    bot_token = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'  # Remplacez par votre token
    language = 'fr'
    first_name = "Georges Moula"  # Votre nom
    # Message de démarrage
    startup_message = f"Le bot a démarré avec succès ! Bonjour {first_name}, je suis prêt à chercher des opportunités !"
    print(startup_message)
    send_telegram_message(chat_id, startup_message, bot_token)

    # Boucle de surveillance
    while True:
        score = analyze_trade_opportunity()  # Analyse des opportunités de trading
        print(f"Score de l'opportunité : {score}%")

        if score >= 80:  # Si le score dépasse 80%
            # Message d'opportunité
            message = (f"Nouvelle opportunité détectée à {score}% !\n"
                       f"Nom de la crypto : [Nom Crypto]\n"
                       f"Prix d'entrée : [Prix d'entrée]\n"
                       f"Objectif : [Objectif de prix]\n")
            print("Opportunité trouvée, envoi du message.")
            send_telegram_message(chat_id, message, bot_token)
        else:
            print("Aucune opportunité détectée.")  # Si pas d'opportunité

        time.sleep(30)  # Attend 30 secondes avant la prochaine analyse

# Lancer le bot
if __name__ == "__main__":
    main()
