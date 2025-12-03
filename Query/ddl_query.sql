-- Traffic Data Table
CREATE TABLE IF NOT EXISTS traffic_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stream_id UUID NOT NULL,
    day_month_year VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    location TEXT NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    latitude NUMERIC(10, 6) NOT NULL,
    total_in_area INTEGER NOT NULL,
    estimated_max_people INTEGER NOT NULL,
    label VARCHAR(10) NOT NULL,
    type VARCHAR(10) NOT NULL,
    fulladdress TEXT,
    city TEXT,
    province TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index on stream_id for lookups
CREATE INDEX idx_traffic_stream_id ON traffic_data(stream_id);

-- Time-based queries (most common for analytics)
CREATE INDEX idx_traffic_timestamp ON traffic_data(timestamp DESC);

-- Geospatial queries
CREATE INDEX idx_traffic_location ON traffic_data(location);
CREATE INDEX idx_traffic_coordinates ON traffic_data(longitude, latitude);

-- Filtering by type/label
CREATE INDEX idx_traffic_type ON traffic_data(type);
CREATE INDEX idx_traffic_label ON traffic_data(label);

-- Composite index for common query patterns
CREATE INDEX idx_traffic_time_location ON traffic_data(timestamp DESC, location);

