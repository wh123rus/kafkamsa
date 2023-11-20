FROM python:3.8-alpine

WORKDIR /connector

COPY . /connector/

RUN apk update && apk add --no-cache mariadb-connector-c-dev build-base\
    && pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir \
    && apk del --rdepends --purge build-base


ENTRYPOINT ["python3"]
CMD ["kafka_consumer.py"]