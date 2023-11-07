from kafka import KafkaProducer
import os

def send_kafka_message(message):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    if isinstance(message, str):
        message = message.encode('utf-8')

    topic = os.getenv('TOPIC_ENV')
    if not topic:
        topic = 'quickstart-events'

    producer.send(topic, value=message)
    producer.close()
