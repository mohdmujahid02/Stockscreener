# 📈 Stock Screener

A Python-based stock screener that automates technical and fundamental analysis. It fetches real-time OHLC data using SmartAPI, applies indicators like RSI, EMA, and MACD, evaluates key fundamentals such as EPS growth, high debt, and promoter holdings, and sends a summarized Excel report via Telegram.

---

## 🔧 Features

- Fetches OHLC data using SmartAPI
- Technical indicators:
  - Relative Strength Index (RSI)
  - Exponential Moving Average (EMA)
  - MACD (Moving Average Convergence Divergence)
- Fundamental filters:
  - EPS growth analysis
  - Debt-to-equity ratio
  - Promoter holding percentage
- Excel report generation
- Telegram alerts integration

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- SmartAPI credentials
- Telegram Bot Token and Chat ID

### Installation

```bash
git clone https://github.com/yourusername/Stockscreener.git
cd Stockscreener
pip install -r requirements.txt
