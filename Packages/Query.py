from Packages.PostgresService import PostgresService
from Packages.GeocodingService import GeocodingService
import logging
import json
import os

class QuerySql:
    # Load configuration from Config.json
    @staticmethod
    def _load_config():
        config_path = os.path.join(os.path.dirname(__file__), '..', 'Configs', 'Config.json')
        with open(config_path, 'r') as f:
            return json.load(f)
    
    _config = _load_config()
    
    # Configuration for traffic_data table
    TRAFFIC_DATA_FIELDS = _config['traffic_data']['fields']
    TRAFFIC_DATA_CONFLICT_KEY = _config['traffic_data']['conflict_key']
    TRAFFIC_DATA_UPDATE_FIELDS = _config['traffic_data']['update_fields']
    
    def __init__(self):
        self.conn = PostgresService.get_connection()
    
    def insert_traffic_data(self, data):
        try:
            cur = self.conn.cursor()
            
            # Build query dynamically from configuration
            fields = ', '.join(self.TRAFFIC_DATA_FIELDS)
            placeholders = ', '.join(['%s'] * len(self.TRAFFIC_DATA_FIELDS))
            
            insert_query = f"""
                INSERT INTO traffic_data ({fields})
                VALUES ({placeholders})
            """
            
            # Extract values in the same order as fields
            values = tuple(data.get(field) for field in self.TRAFFIC_DATA_FIELDS)
            
            cur.execute(insert_query, values)
            
            self.conn.commit()
            cur.close()
            
            logging.info(f"✅ Inserted traffic data for stream_id: {data.get('stream_id')}")
            
        except Exception as e:
            logging.error(f"❌ Failed to insert traffic data: {e}")
            self.conn.rollba
        except Exception as e:
            logging.error(f"❌ Failed to insert traffic data: {e}")
            self.conn.rollback()
            raise