from aiokafka import AIOKafkaProducer

from src.conf import KAFKA_BROKERCONNECT as kafka_connection_url

producer = AIOKafkaProducer(bootstrap_servers=kafka_connection_url)


async def send_message(topic_name: str, message: str) -> None:
    """Отправка сообщения в топик Kafka"""
    await producer.send(topic_name, message)
