from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Request
from bson import ObjectId

from ..dependencies import get_user
from ..schemas import UserWithId, ChatMetaData
from ..response_model import ChatHistories
from ..utils.db import get_db_from_request
from ..database import db_collection_names

router = APIRouter(prefix="/chat")


@router.get("/histories", response_model=ChatHistories)
async def user_chat_histories(
    user: Annotated[UserWithId, Depends(get_user)],
    request: Request
):
    db = get_db_from_request(request)
    collection = db.get_collection(db_collection_names.chat_metadata)
    user_collection = db.get_collection(db_collection_names.users)

    datas = []

    # get messages where user is already involved
    cursor = collection.find({
        '$or': [
            { "first_user_id": user.id }, 
            { "second_user_id": user.id }
        ]
    }).sort({
        "last_updated": -1
    }).limit(100)

    async for metadata_doc in cursor:
        metadata = ChatMetaData(**metadata_doc)
        
        friend_id = (
            metadata.second_user_id 
            if metadata.first_user_id == user.id 
            else metadata.first_user_id
        )
        friend_data = await user_collection.find_one({"_id": ObjectId(friend_id)})
        friend_data = UserWithId(**friend_data)

        data = metadata.model_dump()
        data.update({"friend": friend_data})
        datas.append(data)
        
    return {"datas": datas}
        

@router.get("/messages/{chat_id}")
async def chat_messages(
    user: Annotated[UserWithId, Depends(get_user)],
    chat_id: str,
):
    pass