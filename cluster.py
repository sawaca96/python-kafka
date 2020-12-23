from kafka.cluster import ClusterMetadata

import asyncio


async def get_metatdata():
    print(
        ClusterMetadata(
            bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"]
        ).brokers()
    )


asyncio.run(get_metatdata())