
# Binance Futures Sniper Bot (Colab Version)

# ✅ Step 1: Install Libraries
!pip install python-binance ta telegram python-dotenv

# ✅ Step 2: Import Libraries
import os
from binance.client import Client
from ta.trend import EMAIndicator
import telegram
import time

# ✅ Step 3: API Configuration
BINANCE_API_KEY = 'MASUKKAN_API_KEY_KAMU'
BINANCE_SECRET_KEY = 'MASUKKAN_SECRET_KEY_KAMU'
TELEGRAM_TOKEN = 'MASUKKAN_TOKEN_BOT_TELEGRAM'
TELEGRAM_CHAT_ID = 'MASUKKAN_CHAT_ID_KAMU'

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# ✅ Step 4: Kirim Sinyal Function
def send_signal(pair, direction, entry, sl, tp1, tp2, tp3, sr, acc):
    message = f"""
NEW SIGNAL UPDATE !

#{pair}     {direction.upper()}     10x
ENTRY      : {entry}
SL         : {sl}

TP1        : {tp1}
TP2        : {tp2}
TP3        : {tp3}

S/R        : {sr}
Acc        : {acc}%

Gunakan Money Management Yang Baik.
Jangan Maruk Karena Itu Akan Menghancurkanmu.
"""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# ✅ Step 5: Contoh Kirim Sinyal
send_signal(
    pair='BTCUSDT',
    direction='LONG',
    entry='65200 - 65350',
    sl='64500',
    tp1='66000',
    tp2='66800',
    tp3='67500',
    sr='64400/66000',
    acc=89.3
)
