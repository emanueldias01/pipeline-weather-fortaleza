from pathlib import Path
from dotenv import load_dotenv
import os
from src.extract_data import extract_data
from src.transform_data import data_transformations
from src.load_data import load_data
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

TABLE_NAME = "for_weather"

if __name__ == "__main__":
    try:
        logging.info("1 STEP: EXTRACT DATA:")
        extract_data(URL)

        logging.info("2 STEP: TRANSFORM DATA:")
        df = data_transformations()

        logging.info("3 STEP: LOAD_DATA")
        load_data(TABLE_NAME, df)
    except Exception as ex:
        logging.error(f"ERROR IN PIPELINE: {ex}")
