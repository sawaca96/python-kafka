import asyncio

import orjson
import tenacity

from trading.redis import RedisClient
from trading.service import create_order
from trading.broker import Broker


class ConsumerWorker:
    def __init__(self, consumer):
        self.consumer = consumer
        self.consumer_task = None
        self.redis_client = RedisClient()

    async def create_worker(self):
        await self.redis_client.get_conn(ignore_exception=True)
        self.consumer_task = asyncio.create_task(self._consume_order())

    async def close_worker(self):
        await self.redis_client.close_pool()
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
                await self._commit_order(orjson.loads(msg.value))
        finally:
            await self.consumer.stop()

    @tenacity.retry(wait=tenacity.wait_fixed(2), reraise=True)
    async def _commit_order(self, order):
        await create_order(order)
        await self.redis_client.hset(order["id"], "order", orjson.dumps(order))
        await self.register_order(order)
        await self.consumer.commit()

    async def register_order(self, order):
        name = "real:" + order["code"]
        feed = await Broker.get(name)
        if not feed.task or feed.task.done():
            await feed.start_task()

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

    @tenacity.retry(wait=tenacity.wait_fixed(2), reraise=True)
    async def _commit_position(self, order):
        await create_order(order)
        await self.redis_client.hset(order["id"], "order", orjson.dumps(order))
        await self.register_order(order)
        await self.consumer.commit()