import redis
from contextlib import asynccontextmanager
from collections import namedtuple

from .config import config


@asynccontextmanager
async def redis_lifespan(app):
    print('Connecting to redis...')
    r = redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password
    )

    resp = r.ping()
    print(resp)
    print('Connected to redis.')

    app.state.redis = r

    yield

    app.state.redis.close()


RedisKey = namedtuple(
    "RedisKey", 
    ['chats', 'user_requests', "chat_owners_ref", "chat_msgs"]
)
redis_key = RedisKey(
    chats="chats",
    user_requests="user_requests",
    chat_owners_ref="chat_owners_ref",
    chat_msgs="chat_msgs",
)