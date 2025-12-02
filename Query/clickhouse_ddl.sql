-- Traffic Data Table for ClickHouse
CREATE TABLE IF NOT EXISTS traffic_data (
    stream_id String,
    timestamp DateTime64(3, 'UTC'),
    location String,
    longitude Decimal(10, 6),
    latitude Decimal(10, 6),
    total_in_area Int32,
    estimated_max_people Int32,
    label String,
    type String,
    fulladdress Nullable(String),
    created_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree()
ORDER BY stream_id;
