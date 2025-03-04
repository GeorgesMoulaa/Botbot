import requests
import time
import os

# Fonction pour envoyer des messages via l'API Telegram
def send_telegram_message(chat_id, message, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

# Fonction pour récupérer les prix actuels des cryptos à partir de l'API MEXC
def get_market_data(symbol):
    url = f"https://api.mexc.com/api/v2/market/ticker?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    if data['success']:
        return float(data['data']['last'])
    else:
        return None

# Fonction pour calculer des indicateurs et déterminer si une opportunité existe (exemple simple)
def analyze_trade_opportunity():
    score = random.randint(50, 100)  # Simule un score entre 50 et 100
    if score >= 80:  # Seulement si l'opportunité est supérieure à 80%
        crypto_name = "Bitcoin"
        entry_price = get_market_data("BTC_USDT")
        target_price = entry_price * 1.1  # Exemple d'objectif (10% plus élevé)
        return score, crypto_name, entry_price, target_price
    return None

# Fonction pour vérifier si le message de bienvenue a déjà été envoyé
def check_if_welcome_sent():
    if os.path.exists("welcome_sent.txt"):
        with open("welcome_sent.txt", "r") as file:
            return file.read() == "true"
    return False

# Fonction pour marquer que le message de bienvenue a été envoyé
def mark_welcome_sent():
    with open("welcome_sent.txt", "w") as file:
        file.write("true")

# Fonction principale du bot
def main():
    chat_id = '949838495'  # Remplacez par votre ID de chat
    bot_token = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'  # Remplacez par votre token
    first_name = "Georges Moula"  # Votre nom
    
    # Vérifie si le message de bienvenue a été envoyé
    if not check_if_welcome_sent():
        # Envoi du message de bienvenue
        startup_message = f"Le bot a démarré avec succès ! Bonjour {first_name}, je suis prêt à chercher des opportunités !"
        send_telegram_message(chat_id, startup_message, bot_token)
        # Marque que le message a été envoyé
        mark_welcome_sent()
    
    while True:
        opportunity = analyze_trade_opportunity()  # Analyse des opportunités
        if opportunity:
            score, crypto_name, entry_price, target_price = opportunity
            message = (f"Nouvelle opportunité détectée à {score}% !\n\n"
                       f"Nom de la crypto : {crypto_name}\n"
                       f"Prix d'entrée : {entry_price} USDT\n"
                       f"Objectif : {target_price} USDT\n\n"
                       f"Bonne chance avec ce trade !\n\n"
                       f"Rappelez-vous : Les marchés sont volatils, faites vos propres recherches avant de trader.")
            send_telegram_message(chat_id, message, bot_token)
        else:
            print("Aucune opportunité détectée.")  # Si pas d'opportunité

        time.sleep(30)  # Attend 30 secondes avant la prochaine analyse

# Lancer le bot
if __name__ == "__main__":
    main()
