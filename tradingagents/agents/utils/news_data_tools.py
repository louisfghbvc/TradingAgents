from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor
from ddgs import DDGS

@tool
def get_news(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve news data for a given ticker symbol.
    Uses Google Search (via DuckDuckGo) for real-time news grounding.
    """
    results_text = ""
    
    # 1. Try DuckDuckGo first (Search Grounding)
    query = f"{ticker} stock news {start_date}..{end_date}"
    print(f"🔍 Searching Google News for: {query}")
    try:
        with DDGS() as ddgs:
            # 增加搜尋數量到 10，確保來源豐富
            results = list(ddgs.news(query, max_results=10))
        if results:
            results_text += "### Google/DuckDuckGo Search Results:\n"
            for item in results:
                # 只取有意義的欄位，確保可靠性
                # 這裡可以加入簡單的來源過濾，但 DDG News 通常已經過濾過了
                results_text += f"Title: {item.get('title')}\nSource: {item.get('source')}\nDate: {item.get('date')}\nLink: {item.get('url')}\nSummary: {item.get('body')}\n---\n"
    except Exception as e:
        print(f"⚠️ DuckDuckGo search failed: {e}")

    # 2. Fallback or Append yfinance news (Standard Vendor)
    print(f"📊 Fetching Vendor News (yfinance)...")
    try:
        vendor_news = route_to_vendor("get_news", ticker, start_date, end_date)
        if vendor_news and "No news found" not in vendor_news:
            results_text += "\n### Vendor News (yfinance):\n" + vendor_news
    except Exception as e:
        print(f"⚠️ Vendor news failed: {e}")

    if not results_text:
        return "No news found from any source."
        
    return results_text

@tool
def get_global_news(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "Number of days to look back"] = 7,
    limit: Annotated[int, "Maximum number of articles to return"] = 5,
) -> str:
    """
    Retrieve global financial news.
    Combines Google Search with Vendor data.
    """
    results_text = ""
    
    # 1. DuckDuckGo
    query = "global financial market news macro economy"
    print(f"🔍 Searching Global News: {query}")
    try:
        with DDGS() as ddgs:
            # 增加全域新聞數量到 10
            results = list(ddgs.news(query, max_results=10))
        if results:
            results_text += "### Google/DuckDuckGo Search Results:\n"
            for item in results:
                results_text += f"Title: {item.get('title')}\nSource: {item.get('source')}\nDate: {item.get('date')}\nSummary: {item.get('body')}\n---\n"
    except Exception as e:
        print(f"⚠️ DuckDuckGo search failed: {e}")

    # 2. Vendor (yfinance)
    try:
        vendor_news = route_to_vendor("get_global_news", curr_date, look_back_days, limit)
        if vendor_news:
            results_text += "\n### Vendor News (yfinance):\n" + vendor_news
    except Exception as e:
        print(f"⚠️ Vendor news failed: {e}")

    return results_text if results_text else "No global news found."

@tool
def get_insider_transactions(
    ticker: Annotated[str, "ticker symbol"],
) -> str:
    """
    Retrieve insider transaction information about a company.
    Uses the configured news_data vendor.
    Args:
        ticker (str): Ticker symbol of the company
    Returns:
        str: A report of insider transaction data
    """
    return route_to_vendor("get_insider_transactions", ticker)
