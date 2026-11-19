
-- Create device dimension table

CREATE TABLE devices (
    device_id VARCHAR(20) PRIMARY KEY,
    device_type VARCHAR(30),
    region VARCHAR(30),
    location VARCHAR(30),
    installation_year INTEGER
);


-- Create network telemetry fact table

CREATE TABLE network_telemetry (
    telemetry_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_id VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    cpu_utilization NUMERIC(6,2),
    memory_utilization NUMERIC(6,2),
    latency_ms NUMERIC(10,2),
    packet_loss_pct NUMERIC(6,2),
    bandwidth_utilization NUMERIC(6,2),
    status VARCHAR(20),

    CONSTRAINT fk_telemetry_device
    FOREIGN KEY (device_id)
    REFERENCES devices(device_id),

    CONSTRAINT chk_cpu
    CHECK (cpu_utilization BETWEEN 0 AND 100),

    CONSTRAINT chk_memory
    CHECK (memory_utilization BETWEEN 0 AND 100),

    CONSTRAINT chk_packet_loss
    CHECK (packet_loss_pct BETWEEN 0 AND 100)
);


-- Create incidents fact table

CREATE TABLE incidents (
    incident_id VARCHAR(20) PRIMARY KEY,
    device_id VARCHAR(20) NOT NULL,
    incident_timestamp TIMESTAMP,
    incident_type VARCHAR(50),
    severity VARCHAR(20),
    downtime_minutes INTEGER,
    resolution_status VARCHAR(30),

    CONSTRAINT fk_incident_device
    FOREIGN KEY (device_id)
    REFERENCES devices(device_id),

    CONSTRAINT chk_downtime
    CHECK (downtime_minutes >= 0)
);


-- Create indexes for analytical queries

CREATE INDEX idx_telemetry_device
ON network_telemetry(device_id);

CREATE INDEX idx_telemetry_timestamp
ON network_telemetry(timestamp);

CREATE INDEX idx_incidents_device
ON incidents(device_id);

CREATE INDEX idx_incidents_timestamp
ON incidents(incident_timestamp);
