from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    app.run(host="0.0.0.0", port=8080)
