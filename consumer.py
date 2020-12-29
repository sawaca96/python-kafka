from aiokafka import AIOKafkaConsumer
import asyncio


async def consume():
    consumer = AIOKafkaConsumer(
        "Topic_1",
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"],
        group_id="Redis",
        enable_auto_commit=False,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
            await consumer.commit()
    finally:
        await consumer.stop()


asyncio.run(consume())