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

Configuration
Add your SmartAPI credentials to config.py

Add your Telegram Bot Token and Chat ID

🖥️ Usage
Run the script with: bash
python screener.py
You’ll receive a report file and Telegram alert if red flags are found.

📤 Output
nse_instruments.csv: Filtered list of stocks with technical & fundamental red flags.

📬 Telegram Alerts
Get instant alerts of shortlisted stocks directly in your Telegram group/chat.

📄 License
MIT License

🙋‍♂️ Author
MOHAMMED MUJAHID PASHA

✨ Contributions
PRs welcome! Please submit issues or improvements.


4. Scroll down to the commit section again and fill it as:
   - **Commit message**: `Add detailed README`
   - Optional extended description: `Includes features, setup, usage, and output instructions.`

5. Choose **“Commit directly to the main branch”** and click ✅ **Commit changes**

---

Once committed, GitHub will automatically render the README on your repository's main page, including all those headings.

Let me know if you'd like a `config.py` or example `.env` file next.
