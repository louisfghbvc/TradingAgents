from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor


@tool
def get_news(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve news data for a given ticker symbol.
    Uses the configured news_data vendor (yfinance).
    Also relies on the LLM's internal knowledge and search grounding (if available).
    """
    print(f"📊 Fetching Vendor News (yfinance)...")
    try:
        vendor_news = route_to_vendor(
            "get_news", ticker=ticker, start_date=start_date, end_date=end_date
        )
        if vendor_news:
            return vendor_news
    except Exception as e:
        print(f"⚠️ Vendor news failed: {e}")

    return "No vendor news found. Please use your internal knowledge base or search grounding capability to analyze recent events."


@tool
def get_global_news(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "Number of days to look back"] = 7,
    limit: Annotated[int, "Maximum number of articles to return"] = 5,
) -> str:
    """
    Retrieve global financial news.
    Uses the configured news_data vendor (yfinance).
    Also relies on the LLM's internal knowledge and search grounding (if available).
    """
    print(f"📊 Fetching Global Vendor News (yfinance)...")
    try:
        vendor_news = route_to_vendor(
            "get_global_news",
            curr_date=curr_date,
            look_back_days=look_back_days,
            limit=limit,
        )
        if vendor_news:
            return vendor_news
    except Exception as e:
        print(f"⚠️ Vendor news failed: {e}")

    return "No global vendor news found. Please use your internal knowledge base or search grounding capability to analyze recent macro events."


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
    return route_to_vendor("get_insider_transactions", ticker=ticker)
