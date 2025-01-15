import json
import asyncio

from aiokafka import AIOKafkaProducer

from src.conf import KAFKA_BROKERCONNECT as kafka_connection_url

loop = asyncio.get_event_loop()
producer = AIOKafkaProducer(
    bootstrap_servers=kafka_connection_url, 
    loop=loop,
    value_serializer=lambda v: json.dumps(v).encode('utf-8') 
)


async def send_message(topic_name: str, value: dict) -> None:
    """Отправка сообщения в топик Kafka"""
    await producer.send(topic_name, value)
