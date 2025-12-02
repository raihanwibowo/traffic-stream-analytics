import argparse
import time
from Packages.Parser import KafkaParser


TOPIC = "ws_incoming"

def main():
    KafkaParser.consumer_kafka(TOPIC)

if __name__ == "__main__":
    main()