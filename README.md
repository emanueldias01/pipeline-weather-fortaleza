# Fortaleza Weather Data Pipeline

An ETL data engineering project that uses Apache Airflow to orchestrate the extraction, transformation, and loading of current weather data for Fortaleza, Brazil, into PostgreSQL.

## Architecture

The `weather_pipeline` DAG runs hourly and has three sequential tasks:

1. **Extract** — requests current conditions for Fortaleza from the OpenWeatherMap API and saves the response as JSON.
2. **Transform** — flattens the JSON into a tabular format, renames and removes fields, and converts Unix timestamps to the `America/Sao_Paulo` timezone. The transformed data is temporarily stored as Parquet.
3. **Load** — appends the transformed records to the `for_weather` table in PostgreSQL.

The DAG retries failed tasks twice, with a five-minute delay between retries. Catchup is disabled.

## Tech stack

- Python 3.12+
- Apache Airflow 3.3.2
- PostgreSQL 16 for weather data
- PostgreSQL and Redis services for Airflow metadata and task execution
- Docker Compose
- pandas, SQLAlchemy, psycopg, and Requests

## Requirements

- Docker Engine with the Docker Compose plugin
- An OpenWeatherMap API key

## Configuration

Docker Compose reads a root-level `.env` file. Create one for the Airflow settings:

```dotenv
AIRFLOW_UID=50000
FERNET_KEY=replace-with-a-generated-fernet-key
```

Generate a Fernet key locally with Python and `cryptography` installed:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

The DAG and PostgreSQL loader read application settings from `config/.env`. Create that file with your API key and the weather database connection URL:

```dotenv
API_KEY=your_openweathermap_api_key
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/weather_db
```

The `db` hostname is the PostgreSQL service name on the Docker Compose network. The Compose configuration publishes this database on `localhost:5432` for connections from the host machine. The `.env` files are ignored by Git; do not commit credentials.

## Run with Docker Compose

From the project root, initialize Airflow's metadata database and start the services:

```bash
docker compose up airflow-init
docker compose up -d
```

Open the Airflow UI at [http://localhost:8080](http://localhost:8080). The default local-development credentials are `airflow` / `airflow`. In the UI, enable the `weather_pipeline` DAG if it is paused, then trigger a run or wait for its hourly schedule.

Inspect the running services and logs with:

```bash
docker compose ps
docker compose logs -f airflow-scheduler airflow-worker
```

Stop the services with:

```bash
docker compose down
```

To also remove the persisted PostgreSQL volumes and their data, run `docker compose down --volumes`.

> The Compose configuration is intended for local development, not production. Change the default credentials and review Airflow's deployment and security settings before exposing the services.

## Project structure

```text
.
├── config/
│   └── airflow.cfg
├── dags/
│   └── weather_dag.py
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
├── docker-compose.yaml
└── pyproject.toml
```

## Data destination

Weather records are appended to the `for_weather` table in the `weather_db` PostgreSQL database. To connect from a PostgreSQL client running on the host, use:

| Setting | Value |
| --- | --- |
| Host | `localhost` |
| Port | `5432` |
| Database | `weather_db` |
| User | `postgres` |
| Password | `postgres` |

These are the default local-development values in `docker-compose.yaml`; update the Compose configuration and `DATABASE_URL` together if you change them.
