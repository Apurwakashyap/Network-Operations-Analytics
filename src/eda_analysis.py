
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 1. LOAD CLEANED DATA

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"
CHART_DIR = BASE_DIR / "notebooks" / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_DIR / "cleaned_telemetry.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

sns.set_theme(style="whitegrid")

# 2. DESCRIPTIVE STATISTICS

print("\nDESCRIPTIVE STATISTICS")

print(
    df[
        [
            "cpu_utilization",
            "memory_utilization",
            "latency_ms",
            "packet_loss_pct",
            "bandwidth_utilization"
        ]
    ].describe().round(2)
)


# 3. AVERAGE LATENCY BY DEVICE

device_latency = (
    df.groupby("device_id")["latency_ms"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTOP 10 DEVICES BY LATENCY")
print(device_latency.head(10).round(2))

plt.figure(figsize=(12, 6))

device_latency.head(10).plot(kind="bar")

plt.title("Top 10 Devices by Average Network Latency")
plt.xlabel("Device ID")
plt.ylabel("Average Latency (ms)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(CHART_DIR / "top_latency_devices.png")
plt.show()


# 4. NETWORK PERFORMANCE OVER TIME

daily_latency = (
    df.groupby(df["timestamp"].dt.date)["latency_ms"]
    .mean()
)

plt.figure(figsize=(12, 6))

daily_latency.plot()

plt.title("Daily Average Network Latency")
plt.xlabel("Date")
plt.ylabel("Average Latency (ms)")

plt.tight_layout()
plt.savefig(CHART_DIR / "daily_latency_trend.png")
plt.show()


# 5. CPU AND LATENCY CORRELATION

correlation = df[
    ["cpu_utilization", "latency_ms"]
].corr()

print("\nCPU AND LATENCY CORRELATION")
print(correlation.round(3))

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="cpu_utilization",
    y="latency_ms",
    alpha=0.4
)

plt.title("CPU Utilization vs Network Latency")
plt.xlabel("CPU Utilization (%)")
plt.ylabel("Latency (ms)")

plt.tight_layout()
plt.savefig(CHART_DIR / "cpu_latency_correlation.png")
plt.show()

# 6. NETWORK STATUS DISTRIBUTION

status_counts = df["status"].value_counts()

print("\nNETWORK STATUS DISTRIBUTION")
print(status_counts)

plt.figure(figsize=(8, 5))

status_counts.plot(kind="bar")

plt.title("Network Device Status Distribution")
plt.xlabel("Status")
plt.ylabel("Number of Records")

plt.tight_layout()
plt.savefig(CHART_DIR / "network_status.png")
plt.show()

# 7. REGIONAL PERFORMANCE

devices = pd.read_csv(BASE_DIR / "data" / "raw" / "devices.csv")

regional_data = df.merge(
    devices[["device_id", "region"]],
    on="device_id",
    how="left",
    validate="many_to_one"
)

regional_latency = (
    regional_data.groupby("region")["latency_ms"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE LATENCY BY REGION")
print(regional_latency.round(2))

print("\nEDA COMPLETED SUCCESSFULLY")
