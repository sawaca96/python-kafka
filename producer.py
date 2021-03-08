import asyncio

from aiokafka import AIOKafkaProducer
from aiokafka.cluster import ClusterMetadata

from _aiokafka import _update_metadata

ClusterMetadata.update_metadata = _update_metadata

haproxy_host = "103.244.108.142"


async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers=[
            f"{haproxy_host}:9091",
            f"{haproxy_host}:9092",
            f"{haproxy_host}:9093",
        ],
        acks="all",
        enable_idempotence=True,
        transactional_id="txn",
    )
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        async with producer.transaction():
            await producer.send_and_wait("virtual-trading.streaming.order.1", b"song")
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_one())