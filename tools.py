# tools.py
from crewai_tools import tool

@tool("news_search")
def news_tool(query: str) -> str:
    "Stub: in futuro collegheremo una vera ricerca news."
    return f"[news_stub] Nessuna integrazione ancora per: {query}"

@tool("price_snapshot")
def price_tool(ticker: str) -> str:
    "Stub: in futuro collegheremo un provider prezzi."
    return f"[price_stub] Nessun prezzo per: {ticker}"

@tool("indicators")
def ind_tool(ticker: str) -> str:
    "Stub: calcoli indicatori in arrivo."
    return f"[ind_stub] RSI/MA non calcolati per: {ticker}"

@tool("fundamentals")
def fund_tool(ticker: str) -> str:
    "Stub: fondamentali in arrivo."
    return f"[fund_stub] Nessun dato fondamentale per: {ticker}"

@tool("kb_lookup")
def kb_tool(question: str) -> str:
    "Stub: RAG/KB non ancora collegato."
    return "[kb_stub] KB vuota." 
