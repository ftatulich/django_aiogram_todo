import os

HEADERS = {
    'Content-Type': 'application/json; charset=UTF-8',
}

API_URL = os.getenv('API_URL', 'http://0.0.0.0:8000/api/v1/')

TOKEN = os.getenv('TOKEN')