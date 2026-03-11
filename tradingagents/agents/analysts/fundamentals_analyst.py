from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.fundamental_data_tools import (
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
)
from tradingagents.dataflows.coin_gecko import get_crypto_data
from tradingagents.dataflows.config import get_config


def create_fundamentals_analyst(llm):
    def fundamentals_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_fundamentals,
            get_balance_sheet,
            get_cashflow,
            get_income_statement,
            get_crypto_data,  # Added crypto tool
        ]

        system_message = (
            "You are a researcher tasked with analyzing fundamental information about an asset (stock or cryptocurrency). "
            "If the asset is a **Crypto** (e.g., BTC-USD, ETH-USD): Use the `get_crypto_data` tool to fetch market cap, volume, supply, and community stats. Do NOT use financial statement tools. "
            "If the asset is a **Stock** (e.g., AAPL, 2330.TW): Write a comprehensive report including financial documents, company profile, basic financials, and financial history. "
            "Make sure to include as much detail as possible. Provide detailed analysis and insights. "
            + " Make sure to append a Markdown table at the end of the report to organize key points in the report."
            + " Use the available tools: `get_fundamentals` for general analysis. For Stocks only, use `get_balance_sheet`, `get_cashflow`, and `get_income_statement`.",
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(
            tool_names=", ".join(
                [
                    tool.name if hasattr(tool, "name") else tool.__name__
                    for tool in tools
                ]
            )
        )
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "fundamentals_report": report,
        }

    return fundamentals_analyst_node
