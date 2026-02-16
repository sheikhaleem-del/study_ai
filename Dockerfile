FROM mcr.microsoft.com/playwright/python:v1.48.0-noble
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy + install ONLY core deps first
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir flask flask-cors gunicorn playwright flask-jwt-extended pillow jinja2 werkzeug openai && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Verify EVERY import before gunicorn
CMD ["sh", "-c", "pip list | grep cors && python -c 'import flask_cors; print(\"flask_cors imported\")' && gunicorn -b 0.0.0.0:5000 api:app"]
