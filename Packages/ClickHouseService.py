import os
from clickhouse_driver import Client
from dotenv import load_dotenv

load_dotenv()

class ClickHouseService:
    @staticmethod
    def get_connection():
        return Client(
            host=os.getenv("CLICKHOUSE_HOST", "localhost"),
            port=int(os.getenv("CLICKHOUSE_PORT", "9000")),
            database=os.getenv("CLICKHOUSE_DATABASE", "default"),
            user=os.getenv("CLICKHOUSE_USER", "default"),
            password=os.getenv("CLICKHOUSE_PASSWORD", "")
        )
