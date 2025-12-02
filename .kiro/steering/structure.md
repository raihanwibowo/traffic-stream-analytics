---
inclusion: always
---

# Project Structure

## Directory Organization

```
.
├── Api/                    # API layer
│   └── Websocket.py       # FastAPI WebSocket endpoint
├── Configs/               # Configuration files
│   └── Config.json        # Application config (currently unused)
├── DockerCompose/         # Docker compose configurations
├── Packages/              # Core business logic modules
│   ├── KafkaService.py    # Kafka producer/consumer factory
│   ├── Parser.py          # Kafka message parsing and processing
│   ├── PostgresService.py # PostgreSQL connection management
│   └── Query.py           # Database queries and schema management
├── Worker.py              # CLI entry point for Kafka operations
├── Dockerfile             # Container definition
└── .env                   # Environment variables
```

## Architecture Patterns

### Service Layer Pattern
- Services are organized in `Packages/` as reusable modules
- Each service handles a specific concern (Kafka, Postgres, parsing)
- Static methods used for factory patterns (e.g., `KafkaService.get_producer()`)

### Configuration Management
- Environment variables loaded via `python-dotenv`
- `.env` file for local configuration
- Services read config at initialization time

### Database Schema
- `users`: User authentication and role management
- `stocks`: Inventory tracking with quantities
- `traffic_data`: Real-time traffic monitoring with geolocation

## Code Conventions

- **Class naming**: PascalCase (e.g., `KafkaService`, `QuerySql`)
- **Method naming**: snake_case (e.g., `get_producer`, `init_db`)
- **Static methods**: Used for service factories and utility functions
- **Logging**: Standard Python logging with INFO level, formatted with timestamps
- **Database**: Schema initialization handled in `Query.py` with `CREATE TABLE IF NOT EXISTS`
- **Message format**: JSON serialization for Kafka messages
- **CLI**: argparse for command-line argument parsing

## Module Dependencies

- `Worker.py` → `Packages/Parser.py`
- `Parser.py` → `KafkaService.py`
- `Query.py` → `PostgresService.py`
- `Websocket.py` → `KafkaService.py`
- All services → `.env` configuration
