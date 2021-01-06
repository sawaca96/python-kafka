import orjson
from typing import Dict, Any

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from trading.worker import ConsumerWorker


class Producer:
    def __init__(
        self,
        topic,
        **options,
    ):
        self.topic = topic
        self.options = options

    async def produce(self, data: Dict[str, Any]):
        producer = AIOKafkaProducer(**self.options)
        await producer.start()
        try:
            data = await producer.send_and_wait(self.topic, orjson.dumps(data))
        finally:
            await producer.stop()
        return data


class Consumer:
    def __init__(
        self,
        topic: str,
        **options,
    ):
        self.topic = topic
        self.options = options
        self.consumer = None
        self.worker = None

    async def initialize(self):
        self.consumer = AIOKafkaConsumer(self.topic, **self.options)
        self.worker = ConsumerWorker(self.consumer)
        await self.consumer.start()
        await self.worker.create_worker()

    async def stop(self):
        await self.consumer.stop()
        await self.worker.close_worker()
