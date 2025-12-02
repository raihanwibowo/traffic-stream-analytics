from Packages.ClickHouseService import ClickHouseService
from Packages.GeocodingService import GeocodingService
import logging

class ClickHouseQuery:
    def __init__(self):
        self.client = ClickHouseService.get_connection()
    
    def init_traffic_table(self):
        """Creates the traffic_data table in ClickHouse if it doesn't exist."""
        self.client.execute("""
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
            ORDER BY stream_id
        """)
        logging.info("✅ ClickHouse traffic_data table initialized")
    
    def insert_traffic_data(self, data):
        """
        Insert traffic data into ClickHouse.
        ReplacingMergeTree will automatically handle duplicates based on ORDER BY key (stream_id).
        """
        try:
            insert_query = """
                INSERT INTO traffic_data 
                (stream_id, timestamp, location, longitude, latitude, total_in_area, estimated_max_people, label, type, fulladdress, created_at)
                VALUES
            """
            
            # Prepare data tuple
            values = [(
                data.get('stream_id'),
                data.get('timestamp'),
                data.get('location'),
                data.get('longitude'),
                data.get('latitude'),
                data.get('total_in_area'),
                data.get('estimated_max_people'),
                data.get('label'),
                data.get('type'),
                data.get('fulladdress'),
                'now()'
            )]
            
            self.client.execute(insert_query, values)
            
            logging.info(f"✅ Inserted traffic data to ClickHouse for stream_id: {data.get('stream_id')}")
            
        except Exception as e:
            logging.error(f"❌ Failed to insert traffic data to ClickHouse: {e}")
            raise
