---
inclusion: always
---

# Technology Stack

## Core Technologies

- **Language**: Python 3.x
- **Message Broker**: Apache Kafka
- **Database**: PostgreSQL with psycopg2 driver
- **Web Framework**: FastAPI (for WebSocket API)
- **Environment Management**: python-dotenv

## Key Libraries

- `kafka-python`: Kafka client for producers and consumers
- `psycopg2`: PostgreSQL database adapter
- `fastapi`: Modern web framework for WebSocket endpoints
- `python-dotenv`: Environment variable management

## Environment Configuration

All configuration is managed through `.env` file:
- Kafka bootstrap servers
- Kafka consumer offset reset behavior
- PostgreSQL connection parameters (PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD)

## Common Commands

### Running the Worker

```bash
# Run as Kafka producer
python Worker.py --mode producer

# Run as Kafka consumer
python Worker.py --mode consumer
```

### Running the WebSocket API

```bash
# Start FastAPI WebSocket server (typically with uvicorn)
uvicorn Api.Websocket:app --reload
```

## Docker Support

The project includes a Dockerfile for containerization (currently empty/in development).
