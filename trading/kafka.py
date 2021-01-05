from typing import Dict, Any

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import orjson

# from trading import redis_client
# from trading import service
from trading.config import KAFKA_BOOTSTRAP_SERVERS


async def produce_order(order: Dict[str, Any]):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        acks="all",
        enable_idempotence=True,
    )
    await producer.start()
    try:
        await producer.send_and_wait("Order", orjson.dumps(order))
    finally:
        await producer.stop()


async def consume_order():
    consumer = AIOKafkaConsumer(
        "Order",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="Broker",
        enable_auto_commit=False,
    )
    await consumer.start()
    try:
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
            # data = await service.create_order(msg.value)
            # await redis_client.hset(msg.value["id"], "order", orjson.dumps(msg.value))
            # await consumer.commit()
    finally:
        await consumer.stop()
    # return data


async def produce_position():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        acks="all",
        enable_idempotence=True,
    )
    await producer.start()
    try:
        await producer.send_and_wait("Position", b"message")
    finally:
        await producer.stop()


async def consume_position():
    consumer = AIOKafkaConsumer(
        "Position",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="Broker",
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
