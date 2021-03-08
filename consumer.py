import asyncio

import aioredis
from aioredlock import Aioredlock
from aiokafka import AIOKafkaConsumer
from aiokafka.cluster import ClusterMetadata

from _aiokafka import _update_metadata, _add_coordinator


ClusterMetadata.update_metadata = _update_metadata
ClusterMetadata.add_coordinator = _add_coordinator

haproxy_host = "localhost"


async def consume():
    consumer = AIOKafkaConsumer(
        "virtual-trading.logging.transaction.1",
        bootstrap_servers=[
            f"{haproxy_host}:9091",
            f"{haproxy_host}:9092",
            f"{haproxy_host}:9093",
        ],
        group_id="virtual-trading-simulator",
        enable_auto_commit=False,
        isolation_level="read_committed",
    )
    # Get cluster layout and join group `my-group`
    try:
        await consumer.start()
        assign = consumer.assignment()
        end_offsets = await consumer.end_offsets(assign)
        for tp in assign:
            committed = await consumer.committed(tp)
            print("end_offsets = ", end_offsets[tp])
            if end_offsets[tp] == 0:
                continue
            if committed is None:
                consumer.seek(*[tp], 0)
                msg = await consumer.getone(*[tp])
                print(msg)
                consumer.seek(*[tp], 1)
            print(f"{tp.partition} : {committed} | {end_offsets[tp]} ")

        while True:
            data = await consumer.getmany(timeout_ms=1000)
            print(data)
            if not data:
                break

        # async for msg in consumer:
        #     print(
        #         "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
        #             msg.topic,
        #             msg.partition,
        #             msg.offset,
        #             msg.key,
        #             msg.value,
        #             msg.timestamp,
        #         )
        #     )
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


async def test_aioredlock():
    redis = await aioredis.create_redis_pool(
        address="redis://103.244.108.98:5000",
        timeout=5,
        encoding="utf-8",
    )
    keys = await redis.keys("*")
    print(keys)
    await redis.flushall()
    # redis_instance = [
    #     "redis://103.244.108.98:5000",
    # ]
    # lock_manager = Aioredlock(redis_instance)
    # await redis.rpush("song", 1)
    # async with await lock_manager.lock("virtual-trading:test", lock_timeout=10):
    #     keys = await redis.keys("*")
    #     print(keys)


if __name__ == "__main__":
    # asyncio.run(consume())
    asyncio.run(test_aioredlock())
