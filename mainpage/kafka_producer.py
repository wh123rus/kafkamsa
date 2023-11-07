from kafka import KafkaProducer
import os

def send_kafka_message(message):
    broker = os.getenv('BROKER_ENV', 'localhost:9092')

    producer = KafkaProducer(bootstrap_servers=broker)
    if isinstance(message, str):
        message = message.encode('utf-8')

    topic = os.getenv('TOPIC_ENV', 'quickstart-events')

    producer.send(topic, value=message)
    producer.close()
