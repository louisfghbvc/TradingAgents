import pytest
from tradingagents.agents.utils.news_data_tools import get_news, get_global_news
from datetime import datetime, timedelta


def test_get_news_tool():
    """Test if get_news can fetch something (via DDG or yfinance)."""
    today = datetime.now().strftime("%Y-%m-%d")
    last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Test with a major stock (NVDA) that definitely has news
    result = get_news("NVDA", last_week, today)

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 100  # Should return some content
    # It should mention either Google Search or Vendor News
    assert "Google/DuckDuckGo Search Results" in result or "Vendor News" in result


def test_get_global_news_tool():
    """Test global news fetching."""
    today = datetime.now().strftime("%Y-%m-%d")

    result = get_global_news(today)

    assert result is not None
    assert len(result) > 100
