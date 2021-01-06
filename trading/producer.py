import orjson
from typing import Dict, Any

from aiokafka import AIOKafkaProducer


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
