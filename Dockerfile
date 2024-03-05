
FROM python:3.7-alpine
WORKDIR /app
COPY . .
RUN apk add --no-cache curl && pip3 install --no-cache-dir -r requirements.txt && pip install prometheus-flask-exporter
CMD ["python", "app.py"]