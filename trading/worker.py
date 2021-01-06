import asyncio


class ConsumerWorker:
    def __init__(self, consumer):
        self.consumer = consumer
        self.consumer_task = None

    async def create_worker(self):
        self.consumer_task = asyncio.create_task(self._consume_order())

    async def close_worker(self):
        await self.consumer_task.cancel()

    async def _consume_order(self):
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

    async def _consume_position(self):
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
