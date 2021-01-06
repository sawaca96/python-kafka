from aiokafka import AIOKafkaConsumer

from trading.worker import ConsumerWorker


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
