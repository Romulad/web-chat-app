from contextlib import asynccontextmanager

import motor.motor_asyncio
from fastapi import FastAPI

from .configs import settings

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
    app.db = app.mongo_client[settings.mongodb_database]

    yield

    app.mongo_client.close()
