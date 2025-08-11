# AI Portfolio Orchestrator

This folder contains a skeleton implementation of the **multi‑agent
orchestrator** described in your design.  It uses [CrewAI](https://github.com/joaomlourenco/crewai) to
coordinate several specialised agents, [LangChain](https://github.com/langchain-ai/langchain) to
wrap your data sources as tools, and [FastAPI](https://fastapi.tiangolo.com/) to
expose an HTTP endpoint for integration with automation services such
as n8n.

The goal of this orchestrator is to produce a **Weekly Investment
Brief**: a consolidated report that combines news highlights,
technical analysis, fundamental analysis and portfolio/risk
recommendations for your tech/ETF holdings.

## Project structure

```
orchestrator/
├── __init__.py        # Package marker and module docstring
├── agents.py          # Definitions of the four CrewAI agents
├── main.py            # FastAPI app with the `/kickoff` endpoint
├── tools.py           # Stubbed tool functions wrapped as LangChain Tools
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container build instructions (optional)
├── .env.sample        # Example environment variables
└── README.md          # This file
```

## Quick start

1. **Install Python dependencies.**  It's recommended to create a
   virtual environment first:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r orchestrator/requirements.txt
   ```

2. **Provide API keys.**  Copy `.env.sample` to `.env` and fill in
   your OpenAI API key or other secrets as needed.  The code uses
   [`python-dotenv`](https://github.com/theskumar/python-dotenv) (installed
   automatically) to load variables from `.env` at runtime.  For
   example:

   ```bash
   cp orchestrator/.env.sample orchestrator/.env
   echo "OPENAI_API_KEY=sk-..." >> orchestrator/.env
   ```

3. **Run the server.**  Start the FastAPI application using
   [uvicorn](https://www.uvicorn.org/):

   ```bash
   uvicorn orchestrator.main:app --reload --port 8000
   ```

   You should see logs indicating the server is running on
   `http://127.0.0.1:8000`.

4. **Call the orchestrator.**  Use `curl`, Postman or integrate with
   n8n to call the `/kickoff` endpoint.  The request body can
   optionally include a `query` field to customise the report:

   ```bash
   curl -X POST http://127.0.0.1:8000/kickoff \
        -H 'Content-Type: application/json' \
        -d '{"query": "Analizza l\'impatto dell\'AI su MSFT e AAPL"}'
   ```

   The response will be JSON containing the final report assembled by
   the agents.

## Deployment

The included `Dockerfile` builds a lightweight container for the
orchestrator suitable for deployment on platforms such as Google Cloud
Run or AWS App Runner.  To build and run locally:

```bash
docker build -t ai-portfolio-orchestrator -f orchestrator/Dockerfile .
docker run -p 8000:8080 ai-portfolio-orchestrator
```

## Customising the system

This skeleton provides stub implementations for the agents' tools.
You'll need to replace these stubs with real logic to fetch data and
perform analysis.  Here are some suggestions:

* **Market data** (`market_data` in `tools.py`) – integrate with an
  API such as [Yahoo Finance](https://pypi.org/project/yfinance/),
  [Polygon.io](https://polygon.io/), or [Alpha Vantage](https://www.alphavantage.co/).
* **News feed** (`news_feed`) – read from RSS feeds, call
  [NewsAPI](https://newsapi.org/) or similar services, then summarise
  using a language model.
* **Technical indicators** (`indicators`) – use a library like
  [`pandas_ta`](https://github.com/twopirllc/pandas-ta) or
  [`ta`](https://github.com/bukosabino/ta) to compute RSI, moving
  averages, breakouts and other signals.
* **Fundamental data** (`fundamentals`) – fetch earnings reports,
  revenue and valuation multiples from a provider such as
  [Financial Modeling Prep](https://site.financialmodelingprep.com/)
  or your own dataset.
* **Knowledge base queries** (`kb_query`) – use
  [LlamaIndex](https://github.com/run-llama/llama_index) (installed
  automatically) to build a vector index over transcripts, 10‑K/10‑Q
  filings or your own notes and retrieve relevant passages.

When you're ready to scale, you can enable asynchronous execution,
persist agent memory between calls, and integrate the orchestrator
with workflow automation (e.g. n8n) to trigger it on events like
earnings releases.

## License

This skeleton is provided for educational purposes and does not
constitute financial advice.  You are responsible for verifying the
accuracy of all data and complying with applicable laws when trading
financial instruments.