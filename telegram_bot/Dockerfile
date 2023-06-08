FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TOKEN="your_token"
ENV API_URL="http://0.0.0.0:8000/api/v1/"

CMD ["python", "handlers.py"]
