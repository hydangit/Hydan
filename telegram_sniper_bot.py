
import requests
import pandas as pd
import ta
import time
import schedule
from telegram import Bot

# Telegram Setup
bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
chat_id = 'YOUR_CHAT_ID'

# Get All Binance Futures Symbols
def get_futures_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    res = requests.get(url).json()
    return [s['symbol'] for s in res['symbols']
            if s['contractType'] == 'PERPETUAL' and s['marginAsset'] == 'USDT']

# Get 1h Kline Data
def get_klines(symbol, interval="1h", limit=100):
    url = f"https://fapi.binance.com/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    return response.json()

# Analyze Symbol & Calculate Confidence
def analyze_symbol(symbol):
    try:
        data = get_klines(symbol)
        df = pd.DataFrame(data, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = df["close"].astype(float)

        df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
        df["ema"] = ta.trend.EMAIndicator(df["close"], window=20).ema_indicator()
        macd = ta.trend.MACD(df["close"])
        df["macd_diff"] = macd.macd_diff()

        latest = df.iloc[-1]
        close = latest["close"]
        rsi = latest["rsi"]
        ema = latest["ema"]
        macd_diff = latest["macd_diff"]

        confidence = 0
        direction = None

        if rsi < 30 and close > ema and macd_diff > 0:
            confidence = 85
            direction = "LONG"
        elif rsi > 70 and close < ema and macd_diff < 0:
            confidence = 83
            direction = "SHORT"

        if confidence >= 80:
            return {
                "symbol": symbol,
                "direction": direction,
                "entry": round(close, 2),
                "sl": round(close * (0.98 if direction == "LONG" else 1.02), 2),
                "tp1": round(close * (1.015 if direction == "LONG" else 0.985), 2),
                "tp2": round(close * (1.03 if direction == "LONG" else 0.97), 2),
                "tp3": round(close * (1.045 if direction == "LONG" else 0.955), 2),
                "sr": f"{round(close * 0.97, 2)}/{round(close * 1.03, 2)}",
                "acc": confidence
            }

        return None
    except:
        return None

# Format Signal Message
def format_signal(data):
    return f"""
📡 NEW SIGNAL UPDATE !

#{data['symbol']} {data['direction']} 10x
ENTRY  : {data['entry']}
SL     : {data['sl']}

TP1    : {data['tp1']}
TP2    : {data['tp2']}
TP3    : {data['tp3']}

S/R    : {data['sr']}
Acc    : {data['acc']}%

⚠️ Gunakan Money Management Yang Baik.
Jangan Maruk Karena Itu Akan Menghancurkanmu.
"""

# Scan & Send Top 5 Signals
def scan_and_send():
    symbols = get_futures_symbols()
    results = []

    for symbol in symbols:
        result = analyze_symbol(symbol)
        if result:
            results.append(result)

    top_signals = sorted(results, key=lambda x: x['acc'], reverse=True)[:5]

    for signal in top_signals:
        msg = format_signal(signal)
        bot.send_message(chat_id=chat_id, text=f"<pre>{msg}</pre>", parse_mode="HTML")

# Run every 1 hour
schedule.every(1).hours.do(scan_and_send)

while True:
    schedule.run_pending()
    time.sleep(1)
