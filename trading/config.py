import os


def get_env(key, default=None, optional=False):
    """Read environment variable"""
    env = os.getenv(key, default)
    if not optional and env is None:
        raise KeyError(f"It requires '{key}' env variable")
    return env


DB_NAME = get_env("DB_NAME")
DB_USER = get_env("DB_USER")
DB_PASSWORD = get_env("DB_PASSWORD")
DB_HOST = get_env("DB_HOST")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


# REDIS DB
REDIS_ORDER = {
    "address": "redis://" + get_env("REDIS_ORDER_HOST", "127.0.0.1:6379/1"),
    "minsize": int(get_env("REDIS_POOL_MIN", "2")),
    "maxsize": int(get_env("REDIS_POOL_MAX", "10")),
}

REDIS_PRICE = {
    "address": "redis://" + get_env("REDIS_PRICE_HOST", "127.0.0.1:6379/1"),
    "minsize": int(get_env("REDIS_POOL_MIN", "2")),
    "maxsize": int(get_env("REDIS_POOL_MAX", "10")),
}

KAFKA_BOOTSTRAP_SERVERS = get_env(
    "KAFKA_BOOTSTRAP_SERVERS", "broker-1:29091,broker-2:29092,broker-3:29093"
).split(",")

CORS_ORIGINS = get_env(
    "CORS_ORIGINS", "http://127.0.0.1:8080,http://localhost:8080"
).split(",")
