import requests
import random  # Ajouter cette ligne pour résoudre l'erreur

# Fonction pour envoyer un message sur Telegram
def send_telegram_message(chat_id, message, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

# Fonction pour analyser une opportunité de trade
def analyze_trade_opportunity():
    # Exemple de calcul d'une opportunité en utilisant un score aléatoire
    score = random.randint(50, 100)  # Simulation du score entre 50 et 100
    if score >= 80:
        return {
            "crypto_name": "Bitcoin",
            "entry_price": 40000,
            "target_price": 45000,
            "score": score
        }
    else:
        return None

# Fonction principale
def main():
    chat_id = "949838495"  # Votre ID de chat
    bot_token = "8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ"  # Votre token de bot
    
    # Message de bienvenue
    welcome_message = "Le bot a démarré avec succès ! Bonjour Georges Moula, je suis prêt à chercher des opportunités !"
    send_telegram_message(chat_id, welcome_message, bot_token)
    
    while True:
        opportunity = analyze_trade_opportunity()
        
        if opportunity:
            message = f"Nouvelle opportunité détectée à {opportunity['score']}% !\n\n" \
                      f"Nom de la crypto : {opportunity['crypto_name']}\n" \
                      f"Prix d'entrée : {opportunity['entry_price']} USDT\n" \
                      f"Objectif : {opportunity['target_price']} USDT\n\n" \
                      "Bonne chance avec ce trade !\n" \
                      "Rappelez-vous : Les marchés sont volatils, faites vos propres recherches avant de trader."
            send_telegram_message(chat_id, message, bot_token)

# Lancer le bot
if __name__ == "__main__":
    main()
