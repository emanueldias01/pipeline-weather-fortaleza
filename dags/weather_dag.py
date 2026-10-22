import sys, os
from datetime import datetime, timedelta
from pathlib import Path
from airflow.decorators import dag, task

sys.path.insert(0, '/opt/airflow/src')

from extract_data import extract_data
from transform_data import data_transformations
from load_data import load_data
from dotenv import load_dotenv
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "config" / ".env")

API_KEY = os.getenv('API_KEY')

CITY = "Fortaleza,BR"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&lang=pt_br&appid={API_KEY}"

TABLE_NAME = "for_weather"


@dag(
    dag_id='weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL - Fortaleza Weather',
    schedule='0 */1 * * * ',
    start_date=datetime(2026, 2, 7),
    catchup=False,
    tags=['weather', 'etl']
)
def weather_pipeline():
    @task
    def extract():
        extract_data(URL)

    @task
    def transform():
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/temp_data.parquet')

    @task
    def load():
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_data(TABLE_NAME, df)


    extract() >> transform() >> load()


weather_pipeline()
