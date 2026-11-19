
import pandas as pd
from pathlib import Path


# 1. LOAD RAW DATA

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_DIR / "network_telemetry.csv")

print("INITIAL DATASET SHAPE:", df.shape)


# 2. CHECK DATA QUALITY

print("\nMissing values before cleaning:")
print(df.isnull().sum())

print("\nDuplicate rows before cleaning:")
print(df.duplicated().sum())

# 3. REMOVE DUPLICATES

df = df.drop_duplicates().copy()

print("\nAfter removing duplicates:", df.shape)


# 4. CONVERT TIMESTAMP

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

# Remove records with invalid required identifiers/timestamps
df = df.dropna(
    subset=["device_id", "timestamp"]
).copy()


# 5. VALIDATE NUMERICAL RANGES

valid_ranges = {
    "cpu_utilization": (0, 100),
    "memory_utilization": (0, 100),
    "latency_ms": (0, float("inf")),
    "packet_loss_pct": (0, 100),
    "bandwidth_utilization": (0, 100)
}

for column, (minimum, maximum) in valid_ranges.items():

    invalid = (
        (df[column] < minimum) |
        (df[column] > maximum)
    )

    df.loc[invalid, column] = float("nan")


# 6. HANDLING MISSING VALUES

numeric_columns = list(valid_ranges.keys())

for column in numeric_columns:

    device_median = df.groupby("device_id")[column].transform("median")

    df[column] = df[column].fillna(device_median)

    # Fallback if a device has no valid readings
    df[column] = df[column].fillna(df[column].median())


# 7. FINAL QUALITY CHECK

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nDuplicate records after cleaning:")
print(df.duplicated().sum())

print("\nFinal dataset shape:", df.shape)


# 8. SAVE CLEANED DATA

output_file = PROCESSED_DIR / "cleaned_telemetry.csv"

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully!")
print(output_file)
