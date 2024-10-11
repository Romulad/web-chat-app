from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase


def get_db_from_request(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.db