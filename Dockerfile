FROM mcr.microsoft.com/playwright/python:v1.48.0-noble
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir --force-reinstall flask flask-cors gunicorn playwright flask-jwt-extended && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "pip list | grep -E 'flask|cors|jwt|gunicorn' && python -c 'from flask_cors import CORS; print(\"CORS OK\")' && gunicorn -b 0.0.0.0:5000 api:app"]
