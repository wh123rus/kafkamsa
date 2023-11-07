# 기본 이미지 설정
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /app

# .dockerignore에서 제외된 디렉토리 이외의 모든 파일을 복사
COPY . /app/

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y libsnappy-dev openjdk-8-jre \
    && pip install django kafka-python crc32c pyproject python-snappy \
    && pip install -r requirements.txt --no-cache-dir

# 환경 변수 설정 (기본값은 localhost:9092 및 quickstart-events)
ENV BROKER_ENV=localhost:9092
ENV TOPIC_ENV=quickstart-events

# 컨테이너 실행 시 자동으로 실행될 명령어 설정
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
