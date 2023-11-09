from kafka import KafkaConsumer
import pymysql

# Kafka 소비자 설정
consumer = KafkaConsumer('testdb',
                        bootstrap_servers='localhost:9092')

# MySQL 연결 설정
connection = pymysql.connect(
    host='localhost:3306',
    user='user',
    password='user',
    database='test'
)

# Kafka 메시지 소비 및 MariaDB에 저장
for message in consumer:
    try:
        # Kafka 메시지 파싱
        kafka_message = message.value.decode('utf-8').split(', ')
        pod_name = kafka_message[0].split(': ')[1]
        name = kafka_message[1].split(': ')[1]
        item = kafka_message[2].split(': ')[1]
        number = int(kafka_message[3].split(': ')[1])
        uuid = kafka_message[4].split(': ')[1]

        # MariaDB에 데이터 저장
        with connection.cursor() as cursor:
            sql = "INSERT INTO your_table (pod_name, name, item, number, uuid) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (pod_name, name, item, number, uuid))
            connection.commit()

        print("Data inserted into MariaDB successfully!")

    except Exception as e:
        print(f"Failed to process or insert data: {e}")

# 연결 종료
connection.close()
