from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


async def produce_order():
    producer = AIOKafkaProducer(
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"],
    )
    await producer.start()
    try:
        await producer.send_and_wait("Order", b"message")
    finally:
        await producer.stop()


async def produce_position():
    producer = AIOKafkaProducer(
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"],
    )
    await producer.start()
    try:
        await producer.send_and_wait("Position", b"message")
    finally:
        await producer.stop()


async def consume_order():
    consumer = AIOKafkaConsumer(
        "Order",
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"],
        group_id="Redis",
        enable_auto_commit=False,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
            await consumer.commit()
    finally:
        await consumer.stop()


async def consume_position():
    consumer = AIOKafkaConsumer(
        "Position",
        bootstrap_servers=["localhost:9091", "localhost:9092", "localhost:9093"],
        group_id="Redis",
        enable_auto_commit=False,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
            await consumer.commit()
    finally:
        await consumer.stop()
