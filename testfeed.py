import random
import json
import time
import asyncio

import aioredis

from trading.config import REDIS_ORDER


class TestFeed:
    def __init__(self):
        self.rs = None

    async def setup(self):
        self.rs = await aioredis.create_redis_pool(REDIS_ORDER["address"])


async def publich_socket():
    test_code = ["005930", "005940", "005950", "005960"]
    test_dumy1 = list(range(50000, 60000, 100))
    test_dumy2 = list(range(5000, 5500, 50))
    testfeed = TestFeed()
    await testfeed.setup()
    while True:
        code = random.sample(test_code, 1)[0]
        if code in ["005930", "005940"]:
            price = random.sample(test_dumy1, 1)[0]
        else:
            price = random.sample(test_dumy2, 1)[0]
        volume = random.randint(0, 199)
        data = dict(code=code, price=price, volume=volume)
        await testfeed.rs.publish("real:" + data["code"], json.dumps(data))
        time.sleep(random.random())


if __name__ == "__main__":
    asyncio.run(publich_socket())
