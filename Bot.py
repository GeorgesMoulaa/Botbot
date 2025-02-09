import os
import time
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# MEXC API key and secret
API_KEY = 'mx0vgl2Xgrc1HaoPGr'
API_SECRET = '018fc618575f45eb828af5fed21b5aae'

# Telegram Bot token and chat ID
TELEGRAM_TOKEN = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'
TELEGRAM_CHAT_ID = '949838495'

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Function to send a message on Telegram
async def send_telegram_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=types.ParseMode.MARKDOWN)

# Function to analyze trade opportunities
def analyze_trade_opportunity():
    # Placeholder for trade analysis logic
    message = "Analyzing trade opportunities..."
    send_telegram_message(message)

# Main function that runs every 30 seconds
async def main():
    while True:
        analyze_trade_opportunity()
        time.sleep(30)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
