import requests
import time
from typing import Annotated, Dict, Any

# Cache to store symbol -> id mapping to avoid repeated search calls
# e.g., "BTC" -> "bitcoin", "ETH" -> "ethereum"
SYMBOL_TO_ID_CACHE = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "AVAX": "avalanche-2",
    "DOT": "polkadot",
    "LINK": "chainlink",
    "MATIC": "matic-network",
    "SHIB": "shiba-inu",
    "LTC": "litecoin",
    "TRX": "tron",
    "BCH": "bitcoin-cash",
    "UNI": "uniswap",
    "ATOM": "cosmos",
    "XMR": "monero",
    "ETC": "ethereum-classic",
    "XLM": "stellar",
}


def _get_coingecko_id(symbol: str) -> str:
    """
    Convert a ticker symbol (e.g., 'BTC', 'BTC-USD') to CoinGecko API ID (e.g., 'bitcoin').
    """
    # Clean symbol: remove "-USD" or similar suffixes
    clean_symbol = symbol.upper().replace("-USD", "").replace("USDT", "")

    # Check cache first
    if clean_symbol in SYMBOL_TO_ID_CACHE:
        return SYMBOL_TO_ID_CACHE[clean_symbol]

    # If not in cache, search via API
    try:
        url = "https://api.coingecko.com/api/v3/search"
        params = {"query": clean_symbol}
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            coins = data.get("coins", [])
            if coins:
                # Find the best match (exact symbol match preferred)
                for coin in coins:
                    if coin["symbol"].upper() == clean_symbol:
                        found_id = coin["id"]
                        SYMBOL_TO_ID_CACHE[clean_symbol] = found_id
                        return found_id
                # Fallback to the first result if no exact symbol match
                return coins[0]["id"]
    except Exception as e:
        print(f"Error searching CoinGecko ID for {symbol}: {e}")

    return clean_symbol.lower()  # Fallback to lowercase symbol


def get_crypto_data(
    symbol: Annotated[str, "The crypto symbol, e.g. BTC, ETH-USD"],
) -> str:
    """
    Fetch detailed crypto market data, community stats, and developer stats from CoinGecko.
    """
    coin_id = _get_coingecko_id(symbol)

    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "true",
            "developer_data": "true",
            "sparkline": "false",
        }

        # Add a small delay to respect rate limits (Free tier: ~10-30 req/min)
        time.sleep(1.5)

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 404:
            return f"Error: CoinGecko could not find data for ID '{coin_id}' (derived from {symbol})."

        if response.status_code != 200:
            return f"Error fetching data from CoinGecko: HTTP {response.status_code}"

        data = response.json()

        # Extract Market Data
        md = data.get("market_data", {})
        price = md.get("current_price", {}).get("usd", "N/A")
        ath = md.get("ath", {}).get("usd", "N/A")
        atl = md.get("atl", {}).get("usd", "N/A")
        market_cap = md.get("market_cap", {}).get("usd", "N/A")
        total_volume = md.get("total_volume", {}).get("usd", "N/A")
        high_24h = md.get("high_24h", {}).get("usd", "N/A")
        low_24h = md.get("low_24h", {}).get("usd", "N/A")
        price_change_24h = md.get("price_change_percentage_24h", "N/A")
        circulating_supply = md.get("circulating_supply", "N/A")
        total_supply = md.get("total_supply", "N/A")

        # Extract Community/Dev Data
        cd = data.get("community_data", {})
        dd = data.get("developer_data", {})
        reddit_subs = cd.get("reddit_subscribers", "N/A")
        twitter_followers = cd.get(
            "twitter_followers", "N/A"
        )  # Often deprecated in public API, but check
        forks = dd.get("forks", "N/A")
        stars = dd.get("stars", "N/A")
        commit_activity = dd.get("commit_count_4_weeks", "N/A")

        # Extract Description (First paragraph)
        description = data.get("description", {}).get("en", "").split("\n")[0]
        if len(description) > 500:
            description = description[:500] + "..."

        # Build Report
        report = []
        report.append(f"# CoinGecko Report for {data.get('name')} ({symbol})")
        report.append(f"**ID**: {coin_id}")
        report.append(f"**Description**: {description}\n")

        report.append("## 💰 Market Data (USD)")
        report.append(f"- **Current Price**: ${price}")
        report.append(f"- **24h High/Low**: ${high_24h} / ${low_24h}")
        report.append(f"- **Price Change (24h)**: {price_change_24h}%")
        report.append(f"- **Market Cap**: ${market_cap}")
        report.append(f"- **Volume (24h)**: ${total_volume}")
        report.append(f"- **All-Time High (ATH)**: ${ath}")
        report.append(f"- **All-Time Low (ATL)**: ${atl}")
        report.append(f"- **Circulating Supply**: {circulating_supply}")
        report.append(f"- **Total Supply**: {total_supply}\n")

        report.append("## 👥 Community & Developer Stats")
        report.append(f"- **Reddit Subscribers**: {reddit_subs}")
        report.append(f"- **GitHub Stars**: {stars}")
        report.append(f"- **GitHub Forks**: {forks}")
        report.append(f"- **4-Week Commit Count**: {commit_activity}")

        sentiment_up = data.get("sentiment_votes_up_percentage")
        sentiment_down = data.get("sentiment_votes_down_percentage")
        if sentiment_up and sentiment_down:
            report.append(
                f"- **CoinGecko User Sentiment**: 👍 {sentiment_up}% / 👎 {sentiment_down}%"
            )

        return "\n".join(report)

    except Exception as e:
        return f"Exception while fetching CoinGecko data: {str(e)}"


if __name__ == "__main__":
    print(get_crypto_data("BTC"))
