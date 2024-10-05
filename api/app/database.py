from contextlib import asynccontextmanager
from collections import namedtuple

import motor.motor_asyncio
from fastapi import FastAPI

from .configs import settings


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
    app.db = app.mongo_client[settings.mongodb_database]

    yield

    app.mongo_client.close()


DbCollectionNames = namedtuple("DbCollectionNames", ['users', 'user_friends', 'chat_messages', 'user_chat_histories'])
db_collection_names = DbCollectionNames(
    users='users',
    user_friends='user_friends',
    chat_messages='chat_messages',
    user_chat_histories='user_chat_histories'
)