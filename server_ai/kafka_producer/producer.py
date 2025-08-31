from confluent_kafka import Producer
from dotenv import dotenv_values
import json
import os
from kafka_producer.produce_schema import ProduceMessage

env = dotenv_values('.env')
KAFKA_BROKER_URL = os.environ.get('KAFKA_URL') if 'KAFKA_URL' in os.environ else env.get('KAFKA_URL')
KAFKA_TOPIC = 'reply_from_ai_request'

def send_message(message: ProduceMessage):
    producer = Producer({'bootstrap.servers': KAFKA_BROKER_URL})
    msg = json.dumps(message)
    producer.produce(KAFKA_TOPIC, key='message', value=msg)
    print(f"Message sent to topic {KAFKA_TOPIC}: {msg}")
    producer.flush()