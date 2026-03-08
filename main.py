from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a custom config
config = DEFAULT_CONFIG.copy()
# 使用本地 Gemini (免費版)
config["deep_think_llm"] = "gemini-3.0-pro"
config["quick_think_llm"] = "gemini-3.0-flash"
config["max_debate_rounds"] = 1

config["data_vendors"] = {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "yfinance",
    "news_data": "yfinance",
}

# Initialize
ta = TradingAgentsGraph(debug=True, config=config)

# Run for TODAY (NVDA)
# 抓取昨天的日期作為交易日 (或是今天的日期)
today = datetime.now().strftime("%Y-%m-%d")
# 如果是週末，yfinance 可能會抓不到當天的即時價，但新聞還是可以搜
print(f"🚀 Running Trading Agent for NVDA on {today}...")

_, decision = ta.propagate("NVDA", today)
print("\n--- FINAL DECISION ---\n")
print(decision)
