# Bewise Applications
Этот проект представляет собой сервис для обработки заявок пользователей, разработанный с использованием FastAPI, PostgreSQL и Kafka. Сервис позволяет принимать заявки через REST API, сохранять их в базу данных, публиковать информацию о новых заявках в Kafka, а также предоставляет эндпоинт для получения списка заявок с фильтрацией и пагинацией.


## Основные функции
 - Прием заявок через REST API
 - Сохранение заявок в PostgreSQL 
 - Публикация заявок в Kafka 
 - Получение списка заявок

## Технологии   
- **FastAPI** — фреймворк для создания API.
- **PostgreSQL** — реляционная база данных для хранения информации о заявках.
- **Docker** — контейнеризация приложения.
- **Docker Compose** — управление многоконтейнерными приложениями.
- **SQLAlchemy** — ORM для работы с базой данных.

## Запуск проекта

### Требования
- Установленный Docker и Docker Compose.
- Python 3.11+ (если требуется запуск вне Docker).
### Инструкции по запуску с помощью Docker Compose
1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/nariman079/bewise_application
    cd bewise_application
    ```

2. Создайте `.env` в корне проекта и заполните его переменными окружения:

    ```env
    POSTGRES_USER=bewise_user
    POSTGRES_PASSWORD=bewise_password
    POSTGRES_DB=bewise_application_db
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    ZOOKEEPER_CLIENT_PORT=2181
    ZOOKEEPER_TICK_TIME=2000

    KAFKA_BROKER_ID=1
    KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
    KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
    ```

3. Запустите проект с помощью Docker Compose:

    ```bash
    docker compose up --build
    ```

3