FROM python:3.8-alpine

WORKDIR /connector

COPY . /connector/

RUN apk update && apk add --no-cache python3-dev mariadb-connector-c mariadb-connector-c-dev build-base\
    && pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python3"]
CMD ["kafka_consumer.py"]