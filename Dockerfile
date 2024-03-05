
FROM python:3.7-alpine
WORKDIR /app
COPY . .
RUN apk add --no-cache curl && pip3 install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]

# Dockerfile
# FROM python:3.8

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# CMD ["python", "app.py"]