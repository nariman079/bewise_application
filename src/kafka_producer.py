from aiokafka import AIOKafkaProducer
import asyncio


producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')

async def send_message(topic_name: str, message: str) -> None:
    """Отправка сообщения в топик Kafka"""
    await producer.start()

    try:
        await producer.send(topic_name, message)
    finally:
        await producer.stop()
