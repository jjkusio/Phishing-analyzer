FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=15s --timeout=3s --start-period=15s --retries=3 CMD curl --silent --fail http://localhost:8000/healthz || exit 1
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
