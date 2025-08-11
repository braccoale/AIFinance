import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI

# 👇 importa l’orchestratore
from orchestrator import run_orchestration, plan_from_llm  # plan_from_llm è opzionale, vedi /plan

logging.basicConfig(level=logging.INFO)

# Client OpenAI condiviso (passato all’orchestratore)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="AI Finance Orchestrator")

class KickoffRequest(BaseModel):
    query: str | None = None

@app.exception_handler(Exception)
async def unhandled_exc(request: Request, exc: Exception):
    logging.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(status_code=200, content={"error": "unhandled", "detail": str(exc)})

@app.get("/")
def root():
    return {"service": "aifinance", "status": "ok"}

@app.get("/health")
def health():
    return {
        "ok": True,
        "openai_sdk": OpenAI.__module__,
        "has_key": bool(os.getenv("OPENAI_API_KEY")),
    }

# 🔹 endpoint principale: DELEGA all’orchestratore
@app.post("/kickoff")
def kickoff(req: KickoffRequest):
    if not req.query:
        return {"result": "No query provided"}
    try:
        answer = run_orchestration(query=req.query, client=client)
        return {"result": answer}
    except Exception as e:
        logging.exception("Kickoff failed")
        return {"error": "orchestration_failed", "detail": str(e)}

# 🔹 utile per debug: vedere solo il piano dell’orchestratore
@app.post("/plan")
def plan(req: KickoffRequest):
    if not req.query:
        return {"error": "no_query"}
    try:
        plan = plan_from_llm(query=req.query, client=client)
        return plan  # deve essere JSON serializzabile
    except Exception as e:
        logging.exception("Plan failed")
        return {"error": "plan_failed", "detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
