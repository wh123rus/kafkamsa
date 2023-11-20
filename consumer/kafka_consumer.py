from kafka import KafkaConsumer
import mariadb
import os
import datetime

def connect_to_kafka(broker, topic, sasl_user, sasl_passwd):
    consumer_params = {
        "bootstrap_servers": broker,
        "security_protocol": 'SASL_PLAINTEXT',
        "sasl_mechanism": 'PLAIN',
        "sasl_plain_username": sasl_user,
        "sasl_plain_password": sasl_passwd
    }

    consumer = KafkaConsumer(topic, **consumer_params)

    if consumer.bootstrap_connected():
        print(f"Consumer connected to {broker} with Topic:{topic}!!")

    return consumer

def connect_to_mariadb(user, passwd, host, database, port):
    conn_params = {
        "user": user,
        "password": passwd,
        "host": host,
        "database": database,
        "port": port
    }

    try:
        connection = mariadb.connect(**conn_params)
        return connection
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def insert_data_to_mariadb(connection, table, data):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y/%m/%d %H:%M:%S")

    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table} (pod_name, name, item, number, uuid) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, data)
            connection.commit()

        print(f"[{formatted_time}] Data inserted into MariaDB successfully!")
    except Exception as e:
        print(f"[{formatted_time}] Failed to process or insert data: {e}")
    finally:
        connection.close()

def is_connected(connection):
    try:
        connection.ping()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # 환경 변수 받아오기
    db_user = os.getenv('MARIA_DB_USER', 'user')
    db_passwd = os.getenv('MARIA_DB_PASSWARD', 'user')
    db_host = os.getenv('MARIA_DB_HOST', 'localhost')
    db_database = os.getenv('MARIA_DB_DATABASE_NAME', 'test')
    db_table = os.getenv('MARIA_DB_TABLE', 'testmenu')
    db_port = int(os.getenv('MARIA_DB_PORT'))

    kafka_topic = os.getenv('TOPIC_ENV', 'testdb')
    kafka_broker = os.getenv('BROKER_ENV', 'localhost:9092')
    sasl_user = os.getenv('SASL_USER', 'cccr')
    sasl_passwd = os.getenv('SASL_PASSWORD', 'cccr')

    # Kafka 연결
    consumer = connect_to_kafka(kafka_broker, kafka_topic, sasl_user, sasl_passwd)

    # MariaDB 연결
    db_connection = connect_to_mariadb(db_user, db_passwd, db_host, db_database, db_port)

    try:
        for message in consumer:
            # 전달 받은 메시지 SQL문으로 사용하기 위해서 분해
            kafka_message = message.value.decode('utf-8').split(', ')
            data = (
                kafka_message[0].split(': ')[1],
                kafka_message[1].split(': ')[1],
                kafka_message[2].split(': ')[1],
                int(kafka_message[3].split(': ')[1]),
                kafka_message[4].split(': ')[1]
            )
            # DB 연결 확인
            if not is_connected(db_connection):
                db_connection = connect_to_mariadb(db_user, db_passwd, db_host, db_database, db_port)
            # DB로 데이터 저장
            insert_data_to_mariadb(db_connection, db_table, data)
    finally:
        if is_connected(db_connection):
            db_connection.close()
