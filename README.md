# Traffic Stream Analytics

Real-time traffic monitoring system that ingests, processes, and stores vehicle count data with geolocation tracking through a streaming architecture.

## Features

- **Real-time Data Streaming**: Kafka-based message broker for high-throughput traffic data ingestion
- **Geocoding Integration**: Automatic reverse geocoding to enrich traffic data with location details (city, province, full address)
- **WebSocket API**: Real-time client connections for streaming traffic updates
- **Dual Database Support**: PostgreSQL for transactional data, ClickHouse ready for analytics
- **Configurable Pipeline**: JSON-based configuration for flexible data schema management

## Architecture

```
WebSocket Client → Kafka Producer → Kafka Topic → Kafka Consumer → PostgreSQL
                                                                  → ClickHouse (optional)
```

## Tech Stack

- **Language**: Python 3.x
- **Message Broker**: Apache Kafka with Zookeeper
- **Database**: PostgreSQL 17
- **Web Framework**: FastAPI (WebSocket)
- **Geocoding**: Nominatim OpenStreetMap API
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Git

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/raihanwibowo/traffic-stream-analytics.git
cd traffic-stream-analytics
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

Example `.env`:
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_OFFSET_RESET=earliest
TRAFFIC_TOPIC=traffic_data

GEOCODING_API_URL=https://nominatim.openstreetmap.org/reverse
GEOCODING_API_KEY=
GEOCODING_TIMEOUT=5

PGHOST=localhost
PGPORT=5433
PGDATABASE=appdb
PGUSER=docker
PGPASSWORD=docker
```

### 3. Start infrastructure services

```bash
cd DockerCompose
docker-compose up -d
```

This starts:
- PostgreSQL (port 5433)
- Kafka (port 9092)
- Zookeeper (port 2181)
- Kafka UI (port 8081)

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

**Start Kafka Consumer:**
```bash
python Worker.py --mode consumer
```

**Start WebSocket API:**
```bash
uvicorn Api.Websocket:app --reload --port 8000
```

## Project Structure

```
.
├── Api/
│   └── Websocket.py          # FastAPI WebSocket endpoint
├── Configs/
│   └── Config.json           # Database schema configuration
├── DockerCompose/
│   └── docker-compose.yml    # Infrastructure services
├── Packages/
│   ├── KafkaService.py       # Kafka producer/consumer factory
│   ├── Parser.py             # Message parsing and processing
│   ├── PostgresService.py    # PostgreSQL connection management
│   ├── Query.py              # Database queries
│   ├── GeocodingService.py   # Reverse geocoding service
│   ├── ClickHouseService.py  # ClickHouse connection (optional)
│   └── ClickHouseQuery.py    # ClickHouse queries (optional)
├── Query/
│   ├── ddl_query.sql         # PostgreSQL schema
│   └── clickhouse_ddl.sql    # ClickHouse schema (optional)
├── Worker.py                 # CLI entry point
└── requirements.txt          # Python dependencies
```

## Usage

### Sending Traffic Data via WebSocket

Connect to `ws://localhost:8000/ws` and send JSON messages:

```json
{
  "stream_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-12-02T15:21:42+0700",
  "location": "Jakarta",
  "longitude": 106.816666,
  "latitude": -6.200000,
  "total_in_area": 150,
  "estimated_max_people": 200,
  "label": "heavy",
  "type": "vehicle"
}
```

The system will automatically:
1. Receive the message via WebSocket
2. Publish to Kafka topic
3. Consume and enrich with geocoding data
4. Store in PostgreSQL with city, province, and full address

### Kafka UI

Access Kafka UI at `http://localhost:8081` to:
- Monitor topics and messages
- View consumer groups
- Inspect message content

## Configuration

Edit `Configs/Config.json` to modify database schema:

```json
{
  "traffic_data": {
    "fields": ["timestamp", "stream_id", "location", ...],
    "conflict_key": "stream_id",
    "update_fields": ["timestamp", "location", ...]
  }
}
```

## Database Schema

### PostgreSQL - traffic_data

| Column | Type | Description |
|--------|------|-------------|
| stream_id | UUID | Primary key |
| timestamp | TIMESTAMP WITH TIME ZONE | Event timestamp |
| day_month_year | VARCHAR | Formatted date (DD_MM_YYYY) |
| location | TEXT | Location name |
| longitude | NUMERIC(10,6) | Longitude coordinate |
| latitude | NUMERIC(10,6) | Latitude coordinate |
| total_in_area | INTEGER | Vehicle count |
| estimated_max_people | INTEGER | Capacity estimate |
| label | VARCHAR(10) | Traffic label |
| type | VARCHAR(10) | Traffic type |
| fulladdress | TEXT | Complete address from geocoding |
| city | TEXT | City name |
| province | TEXT | Province/state name |
| created_at | TIMESTAMP | Record creation time |

## Development

### Running Tests

```bash
pytest test_*.py
```

### Adding New Fields

1. Update `Configs/Config.json`
2. Update `Query/ddl_query.sql`
3. Recreate database: `docker-compose down -v && docker-compose up -d`

## License

MIT

## Author

Raihan Wibowo
