from aiokafka import AIOKafkaProducer
import asyncio


async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"]
    )
    await producer.start()
    try:
        await producer.send_and_wait("my_topic", b"hahahahaha message")
    finally:
        await producer.stop()


asyncio.run(send_one())