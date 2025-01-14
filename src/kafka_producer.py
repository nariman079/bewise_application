from aiokafka import AIOKafkaProducer

from src.conf import KAFKA_BROKERCONNECT

producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKERCONNECT)

async def send_message(topic_name: str, message: str) -> None:
    """Отправка сообщения в топик Kafka"""
    await producer.start()

    try:
        await producer.send(topic_name, message)
    finally:
        await producer.stop()
