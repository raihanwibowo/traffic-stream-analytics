import os
from dotenv import load_dotenv
from kafka import KafkaProducer, KafkaConsumer
import json

load_dotenv()

class KafkaService:
    @staticmethod
    def get_producer():
        return KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    @staticmethod
    def get_consumer(topic):
        return KafkaConsumer(
            topic,
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            auto_offset_reset=os.getenv("KAFKA_OFFSET_RESET", "latest"),
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
    
    @staticmethod
    def get_raw_consumer(topic):
        """
        Returns a Kafka consumer without automatic JSON deserialization.
        Used when manual deserialization with error handling is needed.
        """
        return KafkaConsumer(
            topic,
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            auto_offset_reset=os.getenv("KAFKA_OFFSET_RESET", "latest"),
            enable_auto_commit=True
        )
