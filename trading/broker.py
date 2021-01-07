import asyncio
from typing import Dict, Any

import orjson
import aioredis

from trading.redis import RedisClient
from trading.service import create_position
from trading import position_producer


class FeedCache(dict):
    def __repr__(self):
        return str({k: len(v.clients) for k, v in self.items()})


class Broker:

    cache = FeedCache()

    def __init__(self, name: str):
        self.name = name
        self.lock = asyncio.Lock()
        self.pool = None
        self.task = None
        self.redis_client = RedisClient()

    @classmethod
    async def get(cls, name: str):
        """Get feed instance"""
        if name in cls.cache:
            feed = cls.cache[name]
        else:
            feed = cls(name=name)
            cls.cache[name] = feed
        return feed

    async def connect_redis(self, name: str) -> aioredis.ConnectionsPool:
        self.pool = await self.redis_client.get_conn(ignore_exception=True)

    async def start_task(self):
        async with self.lock:
            await self.subscribe_channel(self.name)
            loop = asyncio.get_event_loop()
            self.task = loop.create_task(self.receiver())

    async def subscribe_channel(self, name):
        if not self.pool or self.pool.closed:
            await self.connect_redis(self.name)
        channels = await self.pool.subscribe(name)
        if channels:
            self.pubsub = channels[0]

    async def receiver(self) -> None:
        while True:
            try:
                data = await self._get_stream_data()
            except aioredis.errors.ChannelClosedError:
                await self.subscribe_channel(self.name)
                continue
            if not data:
                continue
            await self._send_data_to_executor(data)

    async def _get_stream_data(self) -> Dict[str, Any]:
        """Get stream dat a from redis channel"""
        await self.pubsub.wait_message()
        data = await self.pubsub.get(encoding="utf-8")
        data = orjson.loads(data)
        return data

    async def _send_data_to_executor(self, order):
        await position_producer.produce()
        await create_position(order["account_id"], order)
        self.destroy()

    async def destroy(self) -> None:
        async with self.lock:
            if self.name in self.cache:
                del self.cache[self.name]
            try:
                self.pool.close()
                await self.pool.wait_closed()
                self.task.cancel()
                await asyncio.sleep(0)
            except aioredis.ConnectionForcedCloseError:
                await self.pool.wait_closed()
                self.task.cancel()
                await asyncio.sleep(0)
            except AttributeError:
                pass
