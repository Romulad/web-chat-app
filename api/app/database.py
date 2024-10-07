import os

from contextlib import asynccontextmanager
from collections import namedtuple

import motor.motor_asyncio
from fastapi import FastAPI

from .configs import settings
from .settings import (
    MONGODB_DATABASE_NAME, IN_PRODUCTION, MONGODB_DEFAULT_URL,
    TESTING
)


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.state.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.mongodb_url if IN_PRODUCTION else MONGODB_DEFAULT_URL
    )
    app.state.db = app.state.mongo_client[MONGODB_DATABASE_NAME]

    yield

    app.state.mongo_client.close()

@asynccontextmanager
async def test_db_lifespan(app: FastAPI):
    print("Creating test database...")
    db_name = "test_database"
    app.state.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGODB_DEFAULT_URL
    )
    app.state.db = app.state.mongo_client[db_name]

    yield

    print("Deleting test database...")
    await app.state.mongo_client.drop_database(db_name)
    app.state.mongo_client.close()

def get_db_lifespan():
    if TESTING:
        return test_db_lifespan
    else:
        return db_lifespan


DbCollectionNames = namedtuple("DbCollectionNames", ['users', 'user_friends', 'chat_messages', 'user_chat_histories'])
db_collection_names = DbCollectionNames(
    users='users',
    user_friends='user_friends',
    chat_messages='chat_messages',
    user_chat_histories='user_chat_histories'
)