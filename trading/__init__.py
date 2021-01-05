import asyncio

import aiokafka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from gino import Gino

from .config import DB_URL, CORS_ORIGINS, KAFKA_BOOTSTRAP_SERVERS
from .redis import RedisClient

db = Gino()
redis_client = RedisClient()


def init_views(app):
    from trading import views  # noqa

    @app.get("/ping")
    async def ping():
        return "pong"

    app.include_router(views.router, prefix="/trading")


def create_app():
    """
    Create FastAPI application
    """
    app = FastAPI(
        docs_url="/docs",
        openapi_url="/openapi.json",
        default_response_class=ORJSONResponse,
    )

    # fastapi CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_views(app)

    @app.on_event("startup")
    async def startup():
        await db.set_bind(DB_URL, min_size=1, echo=False)
        await redis_client.get_conn(ignore_exception=True)
        await initialize()
        await consume()

    @app.on_event("shutdown")
    async def shutdown():
        await db.pop_bind().close()
        await redis_client.close_pool()
        consumer_task.cancel()
        await consumer.stop()

    return app


async def initialize():
    loop = asyncio.get_event_loop()
    global consumer
    consumer = aiokafka.AIOKafkaConsumer(
        "Order",
        loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="Broker",
    )
    # get cluster layout and join group
    await consumer.start()


async def consume():
    global consumer_task
    consumer_task = asyncio.create_task(send_consumer_message(consumer))


async def send_consumer_message(consumer):
    try:
        async for msg in consumer:
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
    finally:
        await consumer.stop()


app = create_app()
