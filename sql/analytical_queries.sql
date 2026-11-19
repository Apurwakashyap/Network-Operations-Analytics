WITH telemetry_summary AS (
    SELECT
        device_id,
        AVG(cpu_utilization) AS avg_cpu,
        AVG(latency_ms) AS avg_latency,
        AVG(packet_loss_pct) AS avg_packet_loss
    FROM network_telemetry
    GROUP BY device_id
),
incident_summary AS (
    SELECT
        device_id,
        COUNT(*) AS total_incidents,
        SUM(downtime_minutes) AS total_downtime
    FROM incidents
    GROUP BY device_id
)
SELECT
    d.region,
    COUNT(*) AS total_devices,
    ROUND(AVG(t.avg_cpu), 2) AS avg_cpu,
    ROUND(AVG(t.avg_latency), 2) AS avg_latency,
    ROUND(AVG(t.avg_packet_loss), 2) AS avg_packet_loss,
    SUM(COALESCE(i.total_incidents, 0)) AS total_incidents,
    SUM(COALESCE(i.total_downtime, 0)) AS total_downtime
FROM devices d
LEFT JOIN telemetry_summary t
    ON d.device_id = t.device_id
LEFT JOIN incident_summary i
    ON d.device_id = i.device_id
GROUP BY d.region
ORDER BY total_downtime DESC;