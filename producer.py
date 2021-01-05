from aiokafka import AIOKafkaProducer
import asyncio


async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"],
        acks="all",
        enable_idempotence=True,
    )
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("Order", b"message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


asyncio.run(send_one())