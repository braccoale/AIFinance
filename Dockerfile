FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# NON forzare ENV PORT qui: lasciamo che Cloud Run la imposti
EXPOSE 8080

# Usa la shell per espandere $PORT; fallback 8080 se non presente
CMD ["bash","-lc","uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
