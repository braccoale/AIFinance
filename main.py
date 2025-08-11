from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI(title="AI Finance Orchestrator")

class KickoffRequest(BaseModel):
    query: str | None = None

@app.get("/")
def root():
    return {"service": "aifinance", "status": "ok"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/kickoff")
def kickoff(req: KickoffRequest):
    q = req.query or "no-query"
    return {"result": f"orchestrator online - query: {q}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))   # Cloud Run imposta PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)
