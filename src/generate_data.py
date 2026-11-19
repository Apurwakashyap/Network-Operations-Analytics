
import pandas as pd
import numpy as np
from pathlib import Path

# Reproducibility
np.random.seed(42)

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


# 1. CREATE NETWORK DEVICES DATASET

device_ids = [f"DEV_{i:03d}" for i in range(1, 26)]

regions = ["North", "South", "East", "West", "Central"]
device_types = ["Router", "Switch", "Firewall"]

devices = pd.DataFrame({
    "device_id": device_ids,
    "device_type": np.random.choice(device_types, 25),
    "region": np.random.choice(regions, 25),
    "location": [
        f"Site_{i:02d}" for i in range(1, 26)
    ],
    "installation_year": np.random.randint(2018, 2026, 25)
})

devices.to_csv(RAW_DIR / "devices.csv", index=False)



# 2. CREATE NETWORK TELEMETRY DATA

records = []

timestamps = pd.date_range(
    start="2026-10-25",
    periods=400,
    freq="30min"
)

for device in device_ids:

    base_cpu = np.random.uniform(20, 60)
    base_memory = np.random.uniform(30, 70)

    for timestamp in timestamps:

        cpu = np.random.normal(base_cpu, 8)
        memory = np.random.normal(base_memory, 7)

        latency = np.random.normal(35, 10)
        packet_loss = np.random.exponential(0.4)
        bandwidth = np.random.uniform(20, 95)

        # Introduce occasional abnormal network behavior
        if np.random.random() < 0.025:
            latency += np.random.uniform(80, 150)
            packet_loss += np.random.uniform(2, 8)
            cpu += np.random.uniform(15, 35)

        cpu = np.clip(cpu, 1, 100)
        memory = np.clip(memory, 1, 100)
        latency = max(latency, 1)
        packet_loss = np.clip(packet_loss, 0, 20)

        status = (
            "Critical" if latency > 120 or packet_loss > 5
            else "Warning" if latency > 70 or cpu > 85
            else "Healthy"
        )

        records.append({
            "device_id": device,
            "timestamp": timestamp,
            "cpu_utilization": round(cpu, 2),
            "memory_utilization": round(memory, 2),
            "latency_ms": round(latency, 2),
            "packet_loss_pct": round(packet_loss, 2),
            "bandwidth_utilization": round(bandwidth, 2),
            "status": status
        })

telemetry = pd.DataFrame(records)

#  missing values for data quality 
for column in [
    "cpu_utilization",
    "memory_utilization",
    "latency_ms"
]:
    indexes = np.random.choice(
        telemetry.index,
        size=50,
        replace=False
    )
    telemetry.loc[indexes, column] = np.nan

#  duplicate records for validation 
duplicates = telemetry.sample(n=30, random_state=42)
telemetry = pd.concat(
    [telemetry, duplicates],
    ignore_index=True
)

telemetry.to_csv(
    RAW_DIR / "network_telemetry.csv",
    index=False
)


# 3. CREATE NETWORK INCIDENT DATA

incident_types = [
    "High Latency",
    "Packet Loss",
    "Device Failure",
    "High CPU Utilization",
    "Network Outage"
]

severities = ["Low", "Medium", "High", "Critical"]

incidents = pd.DataFrame({
    "incident_id": [
        f"INC_{i:04d}" for i in range(1, 301)
    ],
    "device_id": np.random.choice(device_ids, 300),
    "incident_timestamp": np.random.choice(
        timestamps, 300
    ),
    "incident_type": np.random.choice(
        incident_types, 300
    ),
    "severity": np.random.choice(
        severities, 300,
        p=[0.25, 0.40, 0.25, 0.10]
    ),
    "downtime_minutes": np.random.randint(5, 240, 300),
    "resolution_status": np.random.choice(
        ["Resolved", "In Progress"],
        300,
        p=[0.85, 0.15]
    )
})

incidents.to_csv(
    RAW_DIR / "incidents.csv",
    index=False
)


# 4. DISPLAY DATASET INFORMATION

print("\nDATASET GENERATION COMPLETED")

print("\nDevices:", len(devices))
print("Telemetry records:", len(telemetry))
print("Incident records:", len(incidents))

print("\nGenerated files:")
for file in RAW_DIR.glob("*.csv"):
    print(file.name)

print("\nTelemetry preview:")
print(telemetry.head())

print("\nMissing values:")
print(telemetry.isnull().sum())
