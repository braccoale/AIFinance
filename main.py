import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError, AuthenticationError


logging.basicConfig(level=logging.INFO)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="AI Finance Orchestrator")

class KickoffRequest(BaseModel):
    query: str | None = None
    
@app.exception_handler(Exception)
async def unhandled_exc(request: Request, exc: Exception):
    # Evita 500 generici: torniamo sempre JSON con dettaglio
    logging.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(status_code=200, content={"error": "unhandled", "detail": str(exc)})

@app.get("/")
def root():
    return {"service": "aifinance", "status": "ok"}

@app.get("/health")
def health():
    return {
        "ok": True,
        "openai_sdk": getattr(OpenAI, "__module__", "openai"),
        "has_key": bool(os.getenv("OPENAI_API_KEY")),
    }
@app.post("/kickoff")
def kickoff(req: KickoffRequest):
    if not req.query:
        return {"result": "No query provided"}

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un assistente finanziario amichevole e preciso."},
                {"role": "user", "content": req.query}
            ],
            temperature=0.2
        )
        answer = resp.choices[0].message.content
        return {"result": answer}
    except Exception as e:
        return {"error": "Unhandled", "detail": str(e)}

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Cloud Run passa PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)
