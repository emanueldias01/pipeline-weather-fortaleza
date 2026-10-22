import os
from dotenv import load_dotenv
import logging
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "configs" / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")


def get_engine():
    logging.info("Connect to database")
    return create_engine(DATABASE_URL)


engine = get_engine()


def load_data(table_name: str, df: pd.DataFrame):
    df.to_sql(table_name, con=engine, if_exists="append", index=False)

    logging.info("Load data is sucessful")

    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)

    logging.info(f"Total rows in table: {len(df_check)}")
