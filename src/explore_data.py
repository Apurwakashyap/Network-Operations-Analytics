
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

# Load datasets
devices = pd.read_csv(DATA_DIR / "devices.csv")
telemetry = pd.read_csv(DATA_DIR / "network_telemetry.csv")
incidents = pd.read_csv(DATA_DIR / "incidents.csv")

print("DEVICE DATA")
print(devices.head())
print(devices.shape)

print("\nTELEMETRY DATA")
print(telemetry.head())
print(telemetry.shape)

print("\nINCIDENT DATA")
print(incidents.head())
print(incidents.shape)

print("\nTELEMETRY STATISTICS")
print(telemetry.describe())

print("\nMISSING VALUES")
print(telemetry.isnull().sum())

print("\nDUPLICATE RECORDS")
print(telemetry.duplicated().sum())

print("\nDEVICE DISTRIBUTION")
print(devices["device_type"].value_counts())

print("\nREGIONAL DISTRIBUTION")
print(devices["region"].value_counts())
