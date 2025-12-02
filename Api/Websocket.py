from fastapi import FastAPI, WebSocket
from Packages.KafkaService import KafkaService
import logging
import json
import ast

app = FastAPI()
producer = KafkaService.get_producer()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WS→Kafka")

TOPIC = "ws_incoming"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")

    try:
        while True:
            # Client sends message → WS receives it
            msg = await websocket.receive_text()
            try:
                # Try to parse as JSON first (double quotes)
                data = json.loads(msg)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to evaluate as Python dict (single quotes)
                try:
                    data = ast.literal_eval(msg)
                    logger.info("Parsed message using ast.literal_eval (Python dict format)")
                except (ValueError, SyntaxError) as e:
                    logger.error(f"Failed to parse message: {e}")
                    await websocket.send_text(json.dumps({"error": "Invalid message format"}))
                    continue

            # Send to Kafka
            producer.send(TOPIC, data)
            producer.flush()
            logger.info(f"Sent to Kafka topic '{TOPIC}': {data}")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        logger.info("Client disconnected")
