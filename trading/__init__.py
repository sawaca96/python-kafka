from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from gino import Gino

from .config import DB_URL, CORS_ORIGINS
from .redis import RedisClient

db = Gino()
redis_client = RedisClient()


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

    @app.on_event("startup")
    async def startup():
        await db.set_bind(DB_URL, min_size=1, echo=False)
        await redis_client.get_conn(ignore_exception=True)

    @app.on_event("shutdown")
    async def shutdown():
        await db.pop_bind().close()
        await redis_client.close_pool()

    return app


app = create_app()
