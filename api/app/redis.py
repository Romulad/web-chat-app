import redis
from contextlib import asynccontextmanager
from collections import namedtuple

from .config import config


@asynccontextmanager
async def redis_lifespan(app):
    print('\nConnecting to redis...')
    r = redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password,
        decode_responses=True
    )

    resp = r.ping()

    if resp:
        print('Connected to redis.')
        app.state.redis = r

        yield

        app.state.redis.close()
        print('\nClose redis connection.')
    else:
        print('❌ Unable to connect to redis.')
        yield
    

RedisKey = namedtuple(
    "RedisKey", 
    ['chats', "chat_owners_ref", "chat_msgs"]
)
redis_key = RedisKey(
    chats="chats",
    chat_owners_ref="chat_owners_ref",
    chat_msgs="chat_msgs",
)