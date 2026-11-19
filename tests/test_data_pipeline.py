
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "processed" / "cleaned_telemetry.csv"

def load_telemetry():
    return pd.read_csv(DATA_FILE)

def test_telemetry_file_exists():
    assert DATA_FILE.exists(), "Cleaned telemetry file is missing"

def test_no_duplicate_records():
    df = load_telemetry()
    assert not df.duplicated(subset=["device_id", "timestamp"]).any()

def test_no_missing_critical_values():
    df = load_telemetry()
    critical_columns = [
        "device_id",
        "timestamp",
        "cpu_utilization",
        "memory_utilization",
        "latency_ms",
        "packet_loss_pct",
        "bandwidth_utilization",
        "status",
    ]
    assert df[critical_columns].notnull().all().all()

def test_valid_metric_ranges():
    df = load_telemetry()

    assert df["cpu_utilization"].between(0, 100).all()
    assert df["memory_utilization"].between(0, 100).all()
    assert df["packet_loss_pct"].between(0, 100).all()
    assert df["bandwidth_utilization"].between(0, 100).all()
    assert (df["latency_ms"] >= 0).all()