from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from gino import Gino

from trading.config import DB_URL, CORS_ORIGINS, KAFKA_BOOTSTRAP_SERVERS
from trading.producer import Producer

db = Gino()
order_producer = Producer(
    "Order",
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    acks="all",
    enable_idempotence=True,
)
position_producer = Producer(
    "Position",
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    acks="all",
    enable_idempotence=True,
)


def get_consumer(topic):
    from trading.consumer import Consumer  # noqa

    consumer = Consumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="Broker",
        enable_auto_commit=False,
    )

    return consumer


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

    order_consumer = get_consumer("Order")

    @app.on_event("startup")
    async def startup():
        await db.set_bind(DB_URL, min_size=1, echo=False)
        await order_consumer.initialize()

    @app.on_event("shutdown")
    async def shutdown():
        await db.pop_bind().close()
        await order_consumer.stop()

    return app


app = create_app()
