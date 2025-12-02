from Packages.KafkaService import KafkaService
from Packages.GeocodingService import GeocodingService
from Packages.Query import QuerySql
# from Packages.ClickHouseQuery import ClickHouseQuery

import os
import time
import logging
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class Parser:
    @staticmethod
    def time_to_day_month_year(timestamp):
        # Handle string timestamp (ISO format)
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        # Format as day_month_year
        return timestamp.strftime("%Y-%m-%d")

class KafkaParser:
    def consumer_kafka(topic):
        
        consumer = KafkaService.get_consumer(topic)
        postgres_service = QuerySql()
        # clickhouse_service = ClickHouseQuery()

        logging.info("📡 Consumer listening...")
        for message in consumer:
            try:
                data = message.value
                
                # Get coordinates
                longitude = data.get('longitude')
                latitude = data.get('latitude')
                time = data.get('timestamp')
                
                # Reverse geocode to get full address
                fulladdress = None
                if longitude is not None and latitude is not None:
                    if GeocodingService.validate_coordinates(latitude, longitude):
                        results = GeocodingService.reverse_geocode(latitude, longitude)
                    else:
                        logging.warning(f"⚠️ Invalid coordinates ({latitude}, {longitude})")
                
                # Add fulladdress to data
                data['city'] = results['city']
                data['province'] = results['province']
                data['fulladdress'] = results['fulladdress']
                data['day_month_year'] = Parser.time_to_day_month_year(time)
                
                # Insert traffic data into PostgreSQL
                postgres_service.insert_traffic_data(data)
                
                # Insert traffic data into ClickHouse
                # clickhouse_service.insert_traffic_data(data)
                
            except Exception as e:
                logging.error(f"Error processing message: {e}")
                continue

class GeocodingParser:
    """
    Parser for consuming traffic messages from Kafka, geocoding them,
    and storing enriched data in the database.
    """
    
    @staticmethod
    def consume_and_geocode():
        """
        Consumes messages from Kafka, geocodes them, and stores in database.
        Reads topic name from TRAFFIC_TOPIC environment variable.
        """
        # Read topic name from environment variable
        topic = os.getenv("TRAFFIC_TOPIC")
        
        if not topic:
            logging.error("TRAFFIC_TOPIC environment variable is not set")
            raise ValueError("TRAFFIC_TOPIC environment variable is required")
        
        # Create Kafka consumer without automatic deserialization
        # This allows us to handle JSON parsing errors gracefully
        consumer = KafkaService.get_raw_consumer(topic)
        
        logging.info(f"📡 Geocoding consumer listening on topic: {topic}")
        
        # Consume messages
        for message in consumer:
            try:
                # Deserialize JSON message (Requirement 3.3)
                try:
                    message_dict = json.loads(message.value.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError, AttributeError, TypeError) as e:
                    # Log deserialization error and continue to next message (Requirement 3.4)
                    logging.error(f"Failed to deserialize message: {e}. Skipping message.")
                    continue
                
                # Process the message
                GeocodingParser.process_message(message_dict)
            except Exception as e:
                logging.error(f"Error processing message: {e}")
                # Continue processing next message
                continue
    
    @staticmethod
    def process_message(message: dict) -> dict:
        """
        Processes a single message: validates, geocodes, enriches.
        Returns enriched message dict.
        
        Args:
            message: Dictionary containing traffic data with coordinates
            
        Returns:
            Enriched message dictionary with address field
        """
        # Extract coordinates from message (Requirement 1.1)
        try:
            longitude = message.get("longitude")
            latitude = message.get("latitude")
            
            # Check if coordinates exist
            if longitude is None or latitude is None:
                logging.error(f"Missing coordinates in message with stream_id: {message.get('stream_id', 'unknown')}")
                message["address"] = None
                return message
            
            # Validate coordinates (Requirements 1.2, 1.3, 1.4)
            if not GeocodingService.validate_coordinates(latitude, longitude):
                logging.error(f"Invalid coordinates ({latitude}, {longitude}) for stream_id: {message.get('stream_id', 'unknown')}")
                # Skip geocoding for invalid coordinates
                message["address"] = None
                return message
            
            # Call geocoding service for valid coordinates (Requirement 1.5)
            address = GeocodingService.reverse_geocode(latitude, longitude)
            
            # Enrich message with address field (Requirement 3.5)
            message["address"] = address
            
            return message
            
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            message["address"] = None
            return message