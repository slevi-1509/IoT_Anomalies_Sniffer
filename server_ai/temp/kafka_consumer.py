from kafka import KafkaConsumer
from dotenv import dotenv_values
import os
import json
import threading
import queue
from utils.openai_request import get_openai_response
# from kafka_producer.kafka_producer import produce_kafka_message
# from kafka_producer.produce_schema import ProduceMessage

env = dotenv_values('.env')

KAFKA_BROKER_URL = os.environ.get('KAFKA_URL') if 'KAFKA_URL' in os.environ else env.get('KAFKA_URL')
KAFKA_TOPIC = 'sent_to_ai_request'
KAFKA_CONSUMER_ID = 'fastapi_consumer'
# url = input("Enter the URL of the Kafka broker (default: 'broker-2:9092'): ") or 'broker-2:9092'
# if url == "":
#     KAFKA_BROKER_URL = env.get('KAFKA_URL')

def create_kafka_consumer():   
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        auto_offset_reset='latest',  # Start reading from the latest messages
        enable_auto_commit=True,  # Enable automatic offset committing
        group_id='my-consumer-group',  # Consumer group ID
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserializer for JSON messages
    )
    return consumer

# Poll for new messages from Kafka and print them.
def start_consumer():
    consumer = create_kafka_consumer()
    print(f"Starting Kafka consumer on topic: {KAFKA_TOPIC}")
    try:
        for message in consumer:  
            for device in message.value:
                print(f"Device: {device}, IP: {message.value[device]['src_ip']}")
            data_queue = queue.Queue()
            thread = threading.Thread(target=get_openai_response, args=(message.value, data_queue, ))
            thread.start()
            thread.join()
            # if not data_queue.empty():
                # thread = threading.Thread(target=produce_kafka_message, args=(ProduceMessage(message=data_queue.get()), ))
                # thread.start()
                # thread.join()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        consumer.close()
        print("Kafka consumer closed.")