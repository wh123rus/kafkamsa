# Kafka - Django Miniproject
Kafka를 이용한 간단한 Django 앱 Docker image 파일

## 환경 변수
- 파드 이름 : POD_NAME
- 토픽 이름 : TOPIC_ENV
- 브로커 주소 : BROKER_ENV

## 사용방법
대응하는 링크에 접속 시 환경 변수에 설정한 파드 이름, 토픽 이름, 브로커 주소로 kafka 메시지가 전송된다.
메시지를 전송할 때마다 전체 메시지를 수를 세는 카운트가 증가하며, 모든 메시지엔 카운트가 포함된다.

- CONTAINER_IP/send : 파드의 이름 전달
```Plain Text
Hello from Pod: POD_NAME, Message Count: N
```
- CONTAINER_IP/random_menu : 무작위 아이템과 수량 전달
```Plain Text
Random Element from Pod: POD_NAME, Element: RANDOM_ITEM, Number: RANDOM_NUMBER, Message Count: N
```
- CONTAINER_IP/k_menu : 무작위 아이템과 수량 1000번 전달
```Plain Text
Random Element from Pod: POD_NAME, Element: RANDOM_ITEM, Number: RANDOM_NUMBER, Message Count: N
...
Random Element from Pod: POD_NAME, Element: RANDOM_ITEM, Number: RANDOM_NUMBER, Message Count: N+1000
```
- CONTAINER_IP/send_os_info : 컨테이너의 운영체제 전달
```Plain Text
OS Info from Pod: POD_NAME, OS: Linux, Message Count: N
```
- CONTAINER_IP/reset : 메시지 카운트 숫자 0으로 초기화