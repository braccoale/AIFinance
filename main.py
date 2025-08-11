import os
from fastapi import FastAPI
from pydantic import BaseModel
import openai

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    if not req.query:
        return {"result": "No query provided"}

    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"Sei un assistente finanziario amichevole e preciso."},
            {"role":"user","content": req.query}
        ]
    )
    answer = resp.choices[0].message.content
    return {"result": answer}


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Cloud Run passa PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)
