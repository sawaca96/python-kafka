from typing import Dict, Any
import asyncio

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import orjson

from trading.config import KAFKA_BOOTSTRAP_SERVERS


class Producer:
    pass


class Consumer:
    def __init__(
        self,
        topic: str,
        **options,
    ):
        self.topic = topic
        self.options = options
        self.consumer = None
        self.consumer_task = None

    async def get_one(self, topic_partition, offset):
        self.consumer.seek(topic_partition, offset)
        msg = await self.consumer.getone()
        return msg

    async def initialize(self):
        self.consumer = AIOKafkaConsumer(self.topic, **self.options)
        await self.consumer.start()
        await self.consume()

    async def stop(self):
        await self.consumer_task.cancel()
        await self.consumer.stop()

    async def consume(self):
        self.consumer_task = asyncio.create_task(self.consume_order())

    async def consume_order(self):
        try:
            async for msg in self.consumer:
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
                await self.consumer.commit()
        finally:
            await self.consumer.stop()

    async def consume_position(self):
        try:
            async for msg in self.consumer:
                print(
                    "consumed: ",
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    msg.key,
                    msg.value,
                    msg.timestamp,
                )
            await self.consumer.commit()
        finally:
            await self.consumer.stop()


async def produce_order(order: Dict[str, Any]):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        acks="all",
        enable_idempotence=True,
    )
    await producer.start()
    try:
        data = await producer.send_and_wait("Order", orjson.dumps(order))
    finally:
        await producer.stop()
    return data


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
