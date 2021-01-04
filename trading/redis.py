import asyncio

import aioredis

from trading.config import REDIS_ORDER

redis_exception_classes = (asyncio.TimeoutError, aioredis.errors.RedisError)


class RedisClient:
    def __init__(self):
        self._conn = None

    async def get(self, *arg, **kwargs):
        redis = await self.get_conn()
        return await redis.get(*arg, **kwargs)

    async def hget(self, *arg, **kwargs):
        redis = await self.get_conn()
        return await redis.hget(*arg, **kwargs)

    async def hset(self, *arg, **kwargs):
        redis = await self.get_conn()
        return await redis.hset(*arg, **kwargs)

    async def mset(self, *arg, **kwargs):
        redis = await self.get_conn()
        return await redis.mset(*arg, **kwargs)

    async def mget(self, *arg, **kwargs):
        redis = await self.get_conn()
        return await redis.mget(*arg, **kwargs)

    async def expire(self, *args, **kwargs):
        redis = await self.get_conn()
        return await redis.expire(*args, **kwargs)

    async def get_conn(self, ignore_exception=False):
        if self._conn is None:
            try:
                self._conn = await self._create_pool()
            except redis_exception_classes:
                if ignore_exception:
                    return
                raise
        return self._conn

    async def _create_pool(self) -> aioredis.ConnectionsPool:
        """Create redis client"""
        return await aioredis.create_redis_pool(
            address=REDIS_ORDER["address"],
            minsize=REDIS_ORDER["minsize"],
            maxsize=REDIS_ORDER["maxsize"],
            timeout=1.0,
            encoding="utf-8",
        )

    async def close_pool(self):
        self._redis.close()
        await self._redis.wait_closed()
