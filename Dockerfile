FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .         # il tuo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .                        # copia main.py in /app

ENV PORT=8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

