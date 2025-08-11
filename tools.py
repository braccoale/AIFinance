"""
Utility module defining the tools used by the CrewAI agents.

Each tool is exposed as a `langchain.tools.Tool` instance wrapping a
simple Python function.  In this skeleton all tools return static
strings.  Replace the bodies of these functions with your own logic
that fetches real data (e.g. from financial APIs, RSS feeds, or your
knowledge base).

The descriptions attached to each Tool should briefly explain when
agents ought to use it.  When adding new tools, be concise but
informative – the agent relies on these descriptions to choose the
appropriate tool.
"""

from __future__ import annotations

from typing import List

from langchain.tools import Tool

def market_data(ticker: str, interval: str = "1d", lookback: int = 180) -> str:
    """Return OHLCV candle data for a ticker as a JSON string.

    Args:
        ticker: The stock symbol (e.g. "AAPL").
        interval: Candle interval (e.g. "1d", "1h").
        lookback: Number of periods to look back.

    Returns:
        A JSON string representing the requested candle data.  In this
        skeleton implementation a placeholder message is returned.
    """
    # TODO: connect to a real market data provider (e.g. Yahoo Finance,
    # Polygon.io, Alpha Vantage) and return structured candle data.
    return (
        f"Stub candles for {ticker} interval={interval} lookback={lookback}. "
        "Replace this with real OHLCV data."
    )

def news_feed(query: str, window_days: int = 3) -> str:
    """Fetch recent news articles matching a query.

    Args:
        query: Search terms (tickers, company names, etc.).
        window_days: How many days back to search.

    Returns:
        A brief summary of news headlines.  This skeleton returns a
        placeholder.  Use a news API (e.g. NewsAPI, RSS feeds) in your
        implementation.
    """
    # TODO: implement a real news aggregator and summarizer.  You
    # could integrate with an RSS feed or a commercial API.  Make
    # sure to respect API rate limits and licensing requirements.
    return (
        f"Stub news summary for query '{query}' over the last {window_days} "
        "days."
    )

def indicators(candles_json: str, which: List[str]) -> str:
    """Compute technical indicators from candle data.

    Args:
        candles_json: JSON representation of candle data (OHLCV).
        which: A list of indicator names (e.g. ["RSI", "MACD"]).

    Returns:
        A textual summary of indicator values.  This skeleton
        implementation returns a placeholder message.  Replace with
        calls to a technical analysis library such as pandas_ta.
    """
    # TODO: parse the JSON, compute requested indicators, and format
    # the results in a way that's useful for the agent.
    return (
        f"Stub indicators {which} for the provided candle data. "
        "Replace this with real computations."
    )

def fundamentals(ticker: str) -> str:
    """Retrieve fundamental financial metrics for a company.

    Args:
        ticker: The stock symbol.

    Returns:
        A summary of EPS, revenue growth, guidance and key ratios.  In
        this skeleton a placeholder is returned.  Replace with calls
        to a fundamental data provider or your own analytics.
    """
    # TODO: integrate with a fundamental data API (e.g. FMP,
    # Alpha Vantage) or a custom model to compute valuations.
    return (
        f"Stub fundamentals for {ticker}. "
        "Replace this with earnings, revenue, guidance and ratios."
    )

def kb_query(question: str, ticker: str = "") -> str:
    """Query the knowledge base (RAG) for context.

    Args:
        question: The natural language question posed by an agent.
        ticker: Optional ticker to scope the search.

    Returns:
        A relevant passage or summary from your knowledge base.  In
        this skeleton it returns a placeholder message.  Implement
        using LlamaIndex or another retrieval system.
    """
    # TODO: use LlamaIndex (llama_index) or another RAG engine to
    # retrieve passages from transcripts, 10‑K/10‑Q filings, or your
    # own notes.  Provide citations or metadata to aid the agent.
    return (
        f"Stub KB answer for question '{question}' (ticker={ticker}). "
        "Replace with retrieval augmented generation output."
    )

# Wrap the Python functions as LangChain tools.  These objects
# carry metadata so CrewAI knows when to use them.
price_tool = Tool(
    name="market_data",
    func=market_data,
    description=(
        "Return OHLCV candle data as JSON.  Use this to fetch price and volume"
        " history for a given ticker and interval."
    ),
)

news_tool = Tool(
    name="news_feed",
    func=news_feed,
    description=(
        "Fetch and summarise recent news articles about one or more tickers "
        "over a window of days."
    ),
)

ind_tool = Tool(
    name="indicators",
    func=indicators,
    description=(
        "Compute technical indicators (e.g. RSI, moving averages, breakouts) "
        "from OHLCV candle data."
    ),
)

fund_tool = Tool(
    name="fundamentals",
    func=fundamentals,
    description=(
        "Retrieve fundamental financial metrics (EPS, revenue growth, valuation) "
        "for a given company."
    ),
)

kb_tool = Tool(
    name="kb_query",
    func=kb_query,
    description=(
        "Query the knowledge base (RAG) for additional context, such as transcripts,"
        " filings or your own notes."
    ),
)

__all__ = [
    "price_tool",
    "news_tool",
    "ind_tool",
    "fund_tool",
    "kb_tool",
    "market_data",
    "news_feed",
    "indicators",
    "fundamentals",
    "kb_query",
]