import requests
from pathlib import Path
from dotenv import load_dotenv
import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "configs" / ".env")

API_KEY = os.getenv("API_KEY")

CITY = "Fortaleza,BR"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&lang=pt_br&appid={API_KEY}"


def extract_data(url: str) -> list:

    logging.info("Search data")

    request = requests.get(url)

    data = request.json()

    if request.status_code != 200:
        logging.error(f"Error in request. Code: {request.status_code}\nBody: {data}")
        return []

    if not data:
        logging.info("Not has data")
        return []

    file_path = BASE_DIR / "data" / "weather_data.json"

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f)
        logging.info(f"Data saved successfully in {file_path}")

    return data


extract_data(URL)
