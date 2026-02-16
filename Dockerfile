FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "ls -la /app && python -c 'from api import app; print(\"app found:\", app)' && gunicorn -b 0.0.0.0:5000 api:app"]
