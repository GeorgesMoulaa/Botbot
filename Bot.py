import os
import requests
import pandas as pd
import numpy as np
import time
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor

# MEXC API Keys
MEXC_API_KEY = 'mx0vgl2Xgrc1HaoPGr'
MEXC_SECRET_KEY = '018fc618575f45eb828af5fed21b5aae'

# Telegram bot details
TELEGRAM_TOKEN = '8183061202:AAEGqmjBUB6owUjGs6KoJxxnbMfl-ueXDFQ'
TELEGRAM_CHAT_ID = '949838495'

# Initialize the bot for Telegram
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Function to get historical data from MEXC API
def get_historical_data(symbol, interval='1m'):
    url = f'https://www.mexc.com/api/v2/market/kline'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 100  # Fetch 100 data points (adjustable)
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'data' in data:
        return pd.DataFrame(data['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    else:
        return pd.DataFrame()

# Define a simple strategy based on RSI and moving average
def analyze_trade_opportunity(symbol):
    df = get_historical_data(symbol)
    if df.empty:
        return None  # No data received

    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['rsi'] = pd.Series(np.random.randn(len(df)))  # Placeholder RSI (replace with actual RSI calc)
    df['sma'] = df['close'].rolling(window=10).mean()  # 10-period SMA

    # Define conditions for the trade (example: RSI < 30 and price above SMA)
    buy_condition = (df['rsi'].iloc[-1] < 30) and (df['close'].iloc[-1] > df['sma'].iloc[-1])
    if buy_condition:
        return f"Buy opportunity detected for {symbol}: RSI < 30 and price above SMA"
    return None

# Function to send messages to Telegram
async def send_telegram_message(chat_id, text):
    try:
        await bot.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Error sending message: {e}")

# Main loop to check trading opportunities every 30 seconds
async def main():
    while True:
        symbol = 'BTC_USDT'  # Example trading pair
        opportunity = analyze_trade_opportunity(symbol)
        if opportunity:
            await send_telegram_message(TELEGRAM_CHAT_ID, opportunity)
        await asyncio.sleep(30)  # Wait 30 seconds before checking again

# Start the bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp)
