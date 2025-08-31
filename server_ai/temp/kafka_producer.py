from kafka import KafkaProducer
from dotenv import dotenv_values
import json
import time
import os
from kafka_producer.produce_schema import ProduceMessage

env = dotenv_values('.env')

KAFKA_BROKER_URL = os.environ.get('KAFKA_URL') if 'KAFKA_URL' in os.environ else env.get('KAFKA_URL')
KAFKA_TOPIC = 'reply_from_ai_request'
PRODUCER_CLIENT_ID = 'fastapi_producer'

def create_kafka_producer():    
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        client_id=PRODUCER_CLIENT_ID,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON messages
    )
    return producer

def produce_kafka_message(messageRequest: ProduceMessage):
        producer = create_kafka_producer()
        print("Returning AI results to determine if devices are IoT")
        producer.send(KAFKA_TOPIC, messageRequest.message)
        time.sleep(1)  # Ensure the message is sent before closing the producer
        print("Message sent to Kafka topic:", KAFKA_TOPIC)
        producer.flush()
        producer.close()