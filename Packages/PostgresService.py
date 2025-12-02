import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresService:
    def get_connection():
        return psycopg2.connect(
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
            database=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD")
        )
