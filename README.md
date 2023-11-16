# Kafka - Django Miniproject
Kafka를 이용한 간단한 Django 앱 Docker image 파일

## 환경 변수
- POD_NAME : 파드 이름 (기본값 : 호스트 네임)
- POD_IP : 파드 IP (기본값: hostip)
- INFO_TOPIC : 정보 메시지의 토픽 (기본값 : quickstart-events)
- SHOP_TOPIC : 매장 메시지의 토픽 (기본값 : quickstart-events)
- SASL_USER : Producer SASL 암호화에 사용되는 사용자 이름 (기본값 : cccr)
- SASL_PASSWORD : Producer SASL 암호화에 사용되는 비밀번호 (기본값 : cccr)

## 사용방법
대응하는 링크에 접속 시 환경 변수에 설정한 파드 이름, 토픽 이름, 브로커 주소로 kafka 메시지가 전송된다.

## 접속 가능 URL
- CONTAINER_IP/send : 파드의 정보 전달
```Plain Text
Pod Name: {pod_name}, Pod IP: {pod_ip}
```

- CONTAINER_IP/random_menu : 무작위 아이템과 수량 전달
```Plain Text
Pod Name: {pod_name}, Name: {random_name}, Item: {random_item}, Number: {random_number}, UUID: {userid}
```

- CONTAINER_IP/k_menu : 무작위 아이템과 수량 1000번 전달
```Plain Text
Pod Name: {pod_name}, Name: {random_name}, Item: {random_item}, Number: {random_number}, UUID: {userid}
```

### 쿠버네티스 생성시 파드 IP 설정 방법
쿠버네티스 api를 사용해 생성되는 파드의 IP를 받아와 환경변수에 지정할 수 있다.
```YAML
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: my-image
  env:
  - name: POD_IP
    valueFrom:
      fieldRef:
        fieldPath: status.podIP
```

# Consumer Container
MariaDB를 kafka의 컨슈머와 연결하는 컨테이너이다.
지정한 토픽의 컨슈머가 되어서 연결해둔 DB로 카프카 메시지를 저장한다.
Django의 /random_menu /k_menu 두 url에 접속시에 전달한 메시지를 슬라이싱하여 DB에 저장한다.


## 환경 변수
### DB 정보
- MARIA_DB_USER : DB 사용자 (기본값: user)
- MARIA_DB_PASSWARD : DB 사용자 비밀번호 (기본값: user)
- MARIA_DB_HOST : DB 주소 (기본값: localhost)
- MARIA_DB_DATABASE_NAME : DB 데이터베이스 이름 (기본값: test)
- MARIA_DB_TABLE : DB 테이블 이름 (기본값: testmenu)

### kafka 정보
- TOPIC_ENV : 받아올 토픽의 이름 (기본값: testdb)
- BROKER_ENV : 브로커 주소 (기본값:  localhost:9092)
- SASL_USER : Producer SASL 암호화에 사용되는 사용자 이름 (기본값 : cccr)
- SASL_PASSWORD : Producer SASL 암호화에 사용되는 비밀번호 (기본값 : cccr)

