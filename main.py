"""
FastAPI application exposing the CrewAI orchestrator.

This module wires together the agents defined in agents.py into a Crew
process.  When the `/kickoff` endpoint is called, a new Crew is
instantiated with the defined agents and a task that asks them to
compile a weekly investment brief.  The result is returned to the
caller as JSON.

The endpoint accepts an optional `query` in the request body.  You can
extend the request model to include tickers, constraints or other
inputs to customise the briefing.  All configuration values (e.g.
OpenAI API keys) should be provided via environment variables or a
.env file (see .env.sample).
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from crewai import Crew, Task

from .agents import analyst_news, analyst_tech, analyst_fund, portfolio_mgr


class KickoffRequest(BaseModel):
    """Schema for the kickoff request.

    The `query` field contains a natural language instruction or
    question to seed the agents' discussion.  For example, you can
    specify a particular theme (e.g. "focalizzazione su intelligenza
    artificiale"), a list of tickers or leave it at the default to
    produce a general brief.
    """

    query: str = (
        "Compila il Weekly Investment Brief sintetizzando news, analisi "
        "tecnica, analisi fondamentale e suggerimenti di ribilanciamento."
    )


app = FastAPI(title="AI Portfolio Orchestrator")


def _create_crew(query: str) -> Crew:
    """Factory to build a Crew instance with the configured agents and tasks.

    Args:
        query: A natural language instruction guiding the agents' work.

    Returns:
        A Crew object ready for kickoff.
    """
    task_description = (
        "Compila il Weekly Investment Brief unendo news, analisi tecnica, "
        "analisi fondamentale e proposta di ribilanciamento.  Rispondi alla "
        f"seguente domanda o istruzione: {query}"
    )
    task = Task(
        description=task_description,
        agents=[analyst_news, analyst_tech, analyst_fund, portfolio_mgr],
        expected_output=(
            "Brief con watchlist, segnali, tesi sintetiche, piano operativo e "
            "rischi connessi alle posizioni."
        ),
    )
    crew = Crew(
        agents=[analyst_news, analyst_tech, analyst_fund, portfolio_mgr],
        tasks=[task],
    )
    return crew


@app.post("/kickoff")
async def kickoff(request: KickoffRequest):
    """Endpoint to trigger the orchestrator.

    You can POST a JSON body with a `query` key to customise the
    briefing.  The response will contain the agents' final report.

    Example:

        curl -X POST http://localhost:8000/kickoff \
             -H "Content-Type: application/json" \
             -d '{"query": "Analizza il settore AI e consiglia due titoli da comprare"}'
    """
    try:
        crew = _create_crew(request.query)
        # Run the crew synchronously.  In a production deployment you
        # might want to offload this to a worker thread or message
        # queue to avoid blocking the event loop.  The `kickoff` method
        # returns the final output of the process.
        result = crew.kickoff()
        return {"result": result}
    except Exception as exc:  # pragma: no cover - broad catch for demonstration
        # If something goes wrong we return an HTTP 500 with the error
        # message.  In production you might log the error and return a
        # more user‑friendly message.
        raise HTTPException(status_code=500, detail=str(exc))