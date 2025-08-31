from confluent_kafka import Producer
from kafka_producer.produce_schema import ProduceMessage
import json
import config

KAFKA_BROKER_URL = config.KAFKA_URL
KAFKA_TOPIC = 'sent_to_ai_request'
PRODUCER_CLIENT_ID = 'fastapi_producer'

def send_message(message: ProduceMessage):
    msg = json.dumps(message)
    producer = Producer({'bootstrap.servers': KAFKA_BROKER_URL})
    producer.produce(KAFKA_TOPIC, key='message', value=msg)
    print(f"Message sent to topic {KAFKA_TOPIC}: {msg}")
    producer.flush()