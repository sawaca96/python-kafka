from aiokafka import AIOKafkaProducer
import asyncio


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers=["localhost:9092"])
    await producer.start()
    try:
        await producer.send_and_wait("Topic", b"message")
    finally:
        await producer.stop()


asyncio.run(send_one())