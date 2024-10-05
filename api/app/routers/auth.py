from fastapi import APIRouter, Request

from motor import MotorCollection
from ..schemas import UserWithPassword, User
from ..database import db_collection_names

router = APIRouter(prefix="/auth")

@router.post("/sign-up", response_model=User)
async def create_account(user: UserWithPassword, request: Request):
    collection: MotorCollection = request.app.db.get_collection(db_collection_names.users)
    new_user = await collection.insert_one(user.model_dump())

    return new_user

