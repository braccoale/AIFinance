
from crewai import Agent

from .tools import (
    price_tool,
    news_tool,
    ind_tool,
    fund_tool,
    kb_tool,
)

__all__ = [
    "analyst_news",
    "analyst_tech",
    "analyst_fund",
    "portfolio_mgr",
]

# News & Sentiment Analyst
analyst_news = Agent(
    role="Analista News & Sentiment",
    goal=(
        "Monitorare fonti ufficiali e rumor per scovare eventi market‑moving "
        "e sintetizzarli con un punteggio di confidenza."
    ),
    backstory=(
        "Questo agente segue da vicino fonti di notizie, release aziendali e "
        "social sentiment per individuare notizie rilevanti su titoli tech USA "
        "ed ETF.  Filtra il rumore e valuta l'impatto potenziale di ogni "
        "evento sul portafoglio."
    ),
    tools=[news_tool, kb_tool],
    allow_delegation=False,
)

# Technical Analysis Analyst
analyst_tech = Agent(
    role="Analista Tecnico",
    goal=(
        "Generare segnali operativi e livelli chiave utilizzando indicatori "
        "robusti e conferme multi‑timeframe."
    ),
    backstory=(
        "Questo agente si concentra sull'analisi tecnica dei grafici dei prezzi, "
        "calcolando indicatori come RSI, medie mobili e breakouts per "
        "produrre livelli di supporto/resistenza e segnali di trading."
    ),
    tools=[price_tool, ind_tool],
    allow_delegation=False,
)

# Fundamental Analyst
analyst_fund = Agent(
    role="Analista Fondamentale",
    goal=(
        "Valutare trimestrali, sorprese sugli utili e multipli per costruire "
        "una tesi d'investimento basata su fondamentali solidi."
    ),
    backstory=(
        "Questo agente esamina report trimestrali, guidance aziendali e "
        "indicatori fondamentali per comprendere la salute finanziaria "
        "delle aziende.  Confronta i multipli di valutazione e fornisce una "
        "valutazione rapida."
    ),
    tools=[fund_tool, kb_tool],
    allow_delegation=False,
)

# Portfolio & Risk Manager
portfolio_mgr = Agent(
    role="Portfolio & Rischio",
    goal=(
        "Proporre ribilanciamenti conformi alle politiche di rischio e alle "
        "preferenze dell'investitore (es. limite di esposizione a singolo titolo, "
        "priorità a ETF)."
    ),
    backstory=(
        "Questo agente vigila sulla composizione del portafoglio, valutando il "
        "rischio complessivo, la diversificazione e la coerenza con gli obiettivi "
        "dell'investitore.  Suggerisce aggiustamenti per mantenere l'equilibrio."
    ),
    tools=[kb_tool],
    allow_delegation=False,
)
