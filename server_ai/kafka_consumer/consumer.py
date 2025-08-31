from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import dotenv_values
import json
import time
import threading
import queue
import os
from utils.openai_request import get_openai_response
from kafka_producer.producer import send_message

env = dotenv_values('.env')
KAFKA_BROKER_URL = os.environ.get('KAFKA_URL') if 'KAFKA_URL' in os.environ else env.get('KAFKA_URL')
KAFKA_TOPIC = 'sent_to_ai_request'

def create_topic():
    # Configuration for the Kafka Admin client
    conf = {
        'bootstrap.servers': KAFKA_BROKER_URL  # Change to your broker or Confluent Cloud bootstrap server
    }
    admin_client = AdminClient(conf)
    metadata = admin_client.list_topics(timeout=10)
    if KAFKA_TOPIC in metadata.topics:
        print(f"Topic '{KAFKA_TOPIC}' already exists.")
        return
    # Define new topic
    new_topic = NewTopic(
        topic=KAFKA_TOPIC,
        num_partitions=3,          # adjust as needed
        replication_factor=1       # set >1 in production cluster
    )

    # Create the topic
    fs = admin_client.create_topics([new_topic])

    # Wait for operation to finish
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None if successful
            print(f"✅ Topic '{topic}' created successfully")
        except Exception as e:
            print(f"⚠️ Failed to create topic '{topic}': {e}")


def consume_messages():
    create_topic()
    consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER_URL,
    'group.id': 'fastapi-group',
    'auto.offset.reset': 'earliest',
    })
    consumer.subscribe([KAFKA_TOPIC])
    time.sleep(3)
    print("Starting to consume messages...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        msg_dict = json.loads(msg.value().decode('utf-8'))
        data_queue = queue.Queue()
        thread = threading.Thread(target=get_openai_response, args=(msg_dict, data_queue, ))
        thread.start()
        thread.join()
        if not data_queue.empty():
            thread = threading.Thread(target=send_message, args=(data_queue.get(), ))
            thread.start()
            thread.join()
        for device in msg_dict:
            print(f"Device: {device}, IP: {msg_dict[device]['src_ip']}, Is IoT: {msg_dict[device]['is_iot']}")