from fastapi import APIRouter, Request

from motor.motor_asyncio import AsyncIOMotorCollection

from ..schemas import UserWithPassword, SerializedUser
from ..database import db_collection_names

router = APIRouter(prefix="/auth")

@router.post("/sign-up", response_model=SerializedUser)
async def create_account(user: UserWithPassword, request: Request):
    collection : AsyncIOMotorCollection = request.app.state.db.get_collection(
        db_collection_names.users
    )
    new_user = await collection.insert_one(user.model_dump())
    created_user = await collection.find_one({'_id': new_user.inserted_id})

    return created_user

