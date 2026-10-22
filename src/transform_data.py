import logging
from pathlib import Path
import pandas as pd
import json


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

PATH_DIR = Path(__file__).resolve().parent.parent / "data" / "weather_data.json"
columns_names_to_drop = ["weather", "weather_icon", "sys.type"]
columns_to_normalize_datetime = ["datetime", "sunrise", "sunset"]

columns_names_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "datetime",
    "timezone": "timezone",
    "id": "city_id",
    "name": "city_name",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset",
}


def create_dataframe(path_name: str) -> pd.DataFrame:
    logging.info("Creating dataframe")
    path = Path(path_name)

    if not path.exists():
        logging.error("Error in open data. File not exists")
        raise FileNotFoundError("File not exists")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    logging.info("Dataframe created")
    return df


def normalizer_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df["weather"].apply(lambda x: x[0]))

    df_weather = df_weather.rename(
        columns={
            "id": "weather_id",
            "main": "weather_main",
            "description": "weather_description",
            "icon": "weather_icon",
        }
    )

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"\n✓ weather coloumns normalized - {len(df.columns)} columns")
    return df


def drop_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    logging.info(f"Remove columns call: {columns}")
    df = df.drop(columns)
    logging.info("Columns removed")
    return df


def rename_columns(df: pd.DataFrame, columns: dict[str, str]) -> pd.DataFrame:
    logging.info(f"Rename columns call: {columns}")
    df = df.rename(columns=columns)
    logging.info("Columns renamed")
    return df


def normalize_date_time_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    logging.info(f"Normalizer datetime columns call: {columns}")
    for name in columns:
        df[name] = pd.to_datetime(df[name], unit="s", utc=True).dt.tz_convert(
            "America/Sao_Paulo"
        )
    logging.info("Normalized columns")
    return df


def data_transformations():
    logging.info("\n Init transformer")
    df = create_dataframe(PATH_DIR)
    df = normalizer_weather_columns(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalizer_weather_columns(df, columns_to_normalize_datetime)
    logging.info("Transformation done\n")
    return df
