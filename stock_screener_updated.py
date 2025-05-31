
import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime, timedelta
import requests

from smart_login import get_smartapi_client

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = 'your_bot_token_here'
TELEGRAM_CHAT_ID = '1234567891'
STOCKS = ["RPOWER", "SUZLON", "BSE", "SBIN", "HDFCBANK", "RELIANCE", "INFY", "BAJFINANCE", "KOTAKBANK"]
CONTRACT_MASTER_PATH = "nse_instruments.csv"  # Correct file name

# --- Fundamental Data (mock) ---
fundamentals_data = {
    "RPOWER": {"eps_growth": -12, "debt_to_equity": 2.5, "promoter_holding": 15},
    "SUZLON": {"eps_growth": 5, "debt_to_equity": 1.8, "promoter_holding": 20},
    "BSE": {"eps_growth": 12, "debt_to_equity": 0.1, "promoter_holding": 75},
    "SBIN": {"eps_growth": 18, "debt_to_equity": 0.9, "promoter_holding": 58},
    "HDFCBANK": {"eps_growth": 20, "debt_to_equity": 0.6, "promoter_holding": 60},
    "RELIANCE": {"eps_growth": 22, "debt_to_equity": 0.5, "promoter_holding": 50},
    "INFY": {"eps_growth": 15, "debt_to_equity": 0.2, "promoter_holding": 70},
    "BAJFINANCE": {"eps_growth": 25, "debt_to_equity": 0.9, "promoter_holding": 55},
    "KOTAKBANK": {"eps_growth": 18, "debt_to_equity": 0.4, "promoter_holding": 45},
}

# --- Load token map ---
def load_symbol_token_mapping(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df["exchange"] == "NSE"]  # Filter NSE stocks
    return dict(zip(df["symbol"], df["token"]))

# --- Fetch OHLC from SmartAPI ---
def get_ohlc_data(client, symbol, token, interval="ONE_DAY", days=100):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)

    params = {
        "exchange": "NSE",
        "symboltoken": str(token),
        "interval": interval,
        "fromdate": start_time.strftime("%Y-%m-%d %H:%M"),
        "todate": end_time.strftime("%Y-%m-%d %H:%M")
    }

    try:
        response = client.getCandleData(params)
        candles = response["data"]
        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        print(f"Error fetching OHLC for {symbol}: {e}")
        return None

# --- Send file to Telegram ---
def send_telegram_file(file_path, caption="📊 Stock Screener Report"):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        response = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption
        }, files={"document": f})
    print(response.json())

# --- Main Screener ---
def run_screener():
    client = get_smartapi_client()
    symbol_token_map = load_symbol_token_mapping(CONTRACT_MASTER_PATH)
    results = []

    for stock in STOCKS:
        token = symbol_token_map.get(stock)
        if not token:
            print(f"Token not found for {stock}")
            continue

        df = get_ohlc_data(client, stock, token)
        if df is None or df.empty:
            continue

        # Technical Indicators
        df.ta.rsi(append=True)
        df.ta.ema(length=200, append=True)
        df.ta.macd(append=True)

        latest = df.iloc[-1]
        close = latest['close']
        rsi = latest['RSI_14']
        ema_200 = latest['EMA_200']
        macd = latest['MACD_12_26_9']
        signal = latest['MACDs_12_26_9']

        # Fundamental filters
        fundamentals = fundamentals_data.get(stock, {})
        if not fundamentals:
            continue

        eps_growth_ok = fundamentals.get("eps_growth", 0) > 10
        low_debt_ok = fundamentals.get("debt_to_equity", 1) < 1
        promoter_ok = fundamentals.get("promoter_holding", 100) > 50
        rsi_ok = rsi < 30
        ema_ok = close > ema_200
        macd_ok = macd > signal

        if all([eps_growth_ok, low_debt_ok, promoter_ok, rsi_ok, ema_ok, macd_ok]):
            results.append({
                "Stock": stock,
                "Close": round(close, 2),
                "RSI": round(rsi, 2),
                "Above EMA 200": ema_ok,
                "MACD Signal": round(macd - signal, 2),
                "EPS Growth (%)": fundamentals["eps_growth"],
                "Debt/Equity": fundamentals["debt_to_equity"],
                "Promoter Holding (%)": fundamentals["promoter_holding"]
            })

    # Generate Excel
    report_df = pd.DataFrame(results)
    if not report_df.empty:
        excel_path = "stock_screener_report.xlsx"
        report_df.to_excel(excel_path, index=False)
        send_telegram_file(excel_path)
    else:
        print("No stocks matched the filter criteria.")

if __name__ == "__main__":
    run_screener()
