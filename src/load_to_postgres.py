import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Database connection
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

# Load datasets
devices = pd.read_csv(RAW_DIR / "devices.csv")

telemetry = pd.read_csv(
    PROCESSED_DIR / "cleaned_telemetry.csv"
)

incidents = pd.read_csv(RAW_DIR / "incidents.csv")

# Convert timestamps
telemetry["timestamp"] = pd.to_datetime(
    telemetry["timestamp"]
)

incidents["incident_timestamp"] = pd.to_datetime(
    incidents["incident_timestamp"]
)

# Load dimension table first
devices.to_sql(
    "devices",
    engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)

# Load fact tables
telemetry.to_sql(
    "network_telemetry",
    engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)

incidents.to_sql(
    "incidents",
    engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)

print("All datasets successfully loaded into PostgreSQL!")
