from kafka import KafkaConsumer
import mariadb, os, datetime

# DB 환경 변수 받아오기
db_user = os.getenv('MARIA_DB_USER', 'user')
db_passwd = os.getenv('MARIA_DB_PASSWARD', 'user')
db_host = os.getenv('MARIA_DB_HOST', 'localhost')
db_database = os.getenv('MARIA_DB_DATABASE_NAME', 'test')
db_table = os.getenv('MARIA_DB_TABLE', 'testmenu')
db_port = os.getenv('MARIA_DB_PORT')

# Kafka 환경 변수 받아오기
kafka_topic = os.getenv('TOPIC_ENV', 'testdb')
kafka_broker = os.getenv('BROKER_ENV', 'localhost:9092')
sasl_user = os.getenv('SASL_USER', 'cccr')
sasl_passwd = os.getenv('SASL_PASSWORD', 'cccr')


# Kafka consumer 설정
broker_params= {
            "bootstrap_servers" : kafka_broker,
            "security_protocol" : 'SASL_PLAINTEXT',
            "sasl_mechanism" : 'PLAIN',
            "sasl_plain_username" : sasl_user,
            "sasl_plain_password" : sasl_passwd
        }

consumer = KafkaConsumer(kafka_topic, **broker_params)

if consumer.bootstrap_connected():
    print(f"Consumer connected to {kafka_broker} with Topic:{kafka_topic}!!")

# MySQL 연결 설정
conn_params= {
    "user" : db_user,
    "password" : db_passwd,
    "host" : db_host,
    "database" : db_database,
    "port" : db_port
}
try:
    connection = mariadb.connect(**conn_params)
    print(f"Connected to MariaDB: {db_host} - {db_database}")

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    exit(1)
    
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
            sql = "INSERT INTO {} (pod_name, name, item, number, uuid) VALUES (%s, %s, %s, %s, %s)".format(db_table)
            cursor.execute(sql, (pod_name, name, item, number, uuid))
            connection.commit()

        current_time = datetime.datetime.now()
        print(f"{current_time} Data inserted into MariaDB successfully!")

    except Exception as e:
        print(f"Failed to process or insert data: {e}")

# 연결 종료
connection.close()
