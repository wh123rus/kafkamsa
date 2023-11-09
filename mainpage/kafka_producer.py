from kafka import KafkaProducer
import os, traceback

def send_kafka_message(message, topic='quickstart-events'):
    broker = os.getenv('BROKER_ENV', 'localhost:9092')
    sasl_user = os.getenv('SASL_USER', 'cccr')
    sasl_passwd = os.getenv('SASL_PASSWORD', 'cccr')

    try:
        data = (message).encode('utf-8')

        broker_params= {
            "bootstrap_servers" : broker,
            "compression_type" : 'snappy',
            "security_protocol" : 'SASL_PLAINTEXT',
            "sasl_mechanism" : 'PLAIN',
            "sasl_plain_username" : sasl_user,
            "sasl_plain_password" : sasl_passwd
        }
        
        producer = KafkaProducer(**broker_params)
        if producer.bootstrap_connected():
            producer.send(topic, value=data)
            producer.flush()
            producer.close()
            print(f"Message sent to {topic} successfully!")

        else:  
            print("Failed to connect to Kafka broker.")

    except Exception as e:
        print(f"Failed to send message to Kafka: {e}")
        print(traceback.format_exc())  # 전체 예외 정보를 출력
