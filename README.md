# events-collector

Сервис создан для чтения сообщений из Kafka и матчингом с подходящим индикатором.

### Информация о файлах конфигурации

- Все конфигурции можно найти в директории:
```
src/events_collector/config
```

## Информаци о ENV-параметрах
Имеющиеся env-параметры в проекте:
```env
KAFKA_BOOTSTRAP_SERVER=localhost:9092
KAFKA_GROUP_ID=main
TOPIC_CONSUME_EVENTS=consume
APP_POSTGRESQL_NAME=test_name
APP_POSTGRESQL_USER=user
APP_POSTGRESQL_PASSWORD=password
APP_POSTGRESQL_HOST=localhost
APP_POSTGRESQL_PORT=5432
CSRF_ENABLED=True
SESSION_COOKIE_SECURE=True
CONFIG_DIRECTORY=config/directory
CONFIG_FILE=path/file
```

### Локальный запуск

Для запуска приложения локально нужно:

1. Создать виртуальное окружение:
```bash
python3 -m venv venv
```

2. Активировать виртуальное окружение:
```bash
source venv/bin/activate
```

3. Установить зависимости:
```bash
pip3 install -r requirements.txt
```

4. Собрать приложение как модуль:
```bash
python3 -m pip install .
```

5. Запустить приложение:
```bash
events-collector
```

### Требования к инфраструктуре
1. Минимальная версия Kafka:
  ```yaml
    wurstmeister/kafka:>=2.13-2.7.2
  ```
2. Минимальная версия Postgres:
  ```yaml
    postgres:>=14-alpine
  ```
3. Минимальная версия zookeper:
  ```yaml
    wurstmeister/zookeeper
  ```

### Запуск с помощью докера
1. Dockerfile:
```dockerfile
FROM python:3.10.8-slim as deps
WORKDIR /app
COPY . ./
RUN apt-get update -y && apt-get -y install gcc python3-dev
RUN pip --no-cache-dir install -r requirements.txt 
RUN pip --no-cache-dir install -r requirements.setup.txt 
RUN pip install -e .

FROM deps as build
ARG ARTIFACT_VERSION=local
RUN python setup.py sdist bdist_wheel
RUN ls -ll /app/
RUN ls -ll /app/dist/


FROM python:3.10.8-slim as runtime
COPY --from=build /app/dist/*.whl /app/
RUN apt-get update -y && apt-get -y install gcc python3-dev
RUN pip --no-cache-dir install /app/*.whl
ENTRYPOINT ["events-collector"]
```

2. docker-compose.yml
```yaml
version: '3'


services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
  kafka:
    image: wurstmeister/kafka:latest
    ports:
      - target: 9094
        published: 9094
        protocol: tcp
        mode: host
    environment:
      HOSTNAME_COMMAND: "docker info | grep ^Name: | cut -d' ' -f 2"
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: INSIDE://:9092,OUTSIDE://_{HOSTNAME_COMMAND}:9094
      KAFKA_LISTENERS: INSIDE://:9092,OUTSIDE://:9094
      KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  db:
    image: db_image:staging

  collector:
    restart: always
    build: ./
    ports:
    - "8080:8080"
    environment:
      KAFKA_BOOTSTRAP_SERVER: kafka:9092
      TOPIC_CONSUME_EVENTS: syslog
      KAFKA_GROUP_ID: main
      APP_POSTGRESQL_USER: dbuser
      APP_POSTGRESQL_PASSWORD: test
      APP_POSTGRESQL_NAME: db
      APP_POSTGRESQL_HOST: db
      APP_POSTGRESQL_PORT: 5432
    depends_on:
      - db

 
networks:
    external:
      name: kafka_net
```

3. Запуск контейнеров:
```bash
docker-compose up --build
```

4. Применить дамп файла для бд в контейнере:
```bash
cat restore.sql | docker exec -i db psql -U dbuser -d db
```

5. Перзапустить контейнер collector