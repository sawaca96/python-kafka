import asyncio
from aiokafka import AIOKafkaConsumer

import aioredis
from aioredlock import Aioredlock


async def consume():
    consumer = AIOKafkaConsumer(
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"],
        group_id="Order",
        enable_auto_commit=False,
    )
    # Get cluster layout and join group `my-group`
    try:
        await consumer.start()
        # Consume messages
        async for msg in consumer:
            print(
                "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    msg.key,
                    msg.value,
                    msg.timestamp,
                )
            )
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


async def test_aioredlock():
    redis = await aioredis.create_redis_pool(
        address="redis://localhost:6379/1",
        timeout=5,
        encoding="utf-8",
    )
    redis_instance = [
        "redis://localhost:6379/1",
    ]
    lock_manager = Aioredlock(redis_instance)

    async with await lock_manager.lock("virtual-trading", lock_timeout=10):
        keys = await redis.keys("*")
        print(keys)


# asyncio.run(consume())
asyncio.run(test_aioredlock())
