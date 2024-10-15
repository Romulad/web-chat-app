import datetime

from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from bson import ObjectId

from ..dependencies import get_user, get_socket_user
from ..schemas import UserWithId, ChatMetaData, ChatMessage
from ..req_resp_models import ChatHistories, ChatMessages
from ..utils.db import get_db_from_request
from ..database import db_collection_names
from ..chat_tools.chat_manager import chat_manager


router = APIRouter(prefix="/chat")


connected_users = []

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
        
    return {"data": datas}
        

@router.websocket("/ws")
async def chat_messages(
    websocket: WebSocket,
    user: Annotated[UserWithId, Depends(get_socket_user)]
):
    await websocket.accept()
    try:
        while True:
            await chat_manager.manage_new_msg(user, websocket)
    except WebSocketDisconnect:
        chat_manager.disconnect_user(user.id, websocket)


@router.get("/messages/{chat_id}", response_model=ChatMessages)
async def get_chat_messages(
    chat_id: str,
    request: Request,
    user: Annotated[UserWithId, Depends(get_user)]
):
    db = get_db_from_request(request)
    mta_collection = db.get_collection(db_collection_names.chat_metadata)
    msg_collection = db.get_collection(db_collection_names.chat_messages)

    unread_messages = await msg_collection.find({
        "$and": [
            {"chat_id": chat_id},
            {"receiver_id": user.id},
            {"read": False}
        ]
    }).to_list(1000)
    for unread_msg in unread_messages:
        unread_id = unread_msg.get('_id')
        await msg_collection.update_one(
            {"_id": unread_id},
            {"$set": {"read": True, "read_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}}
        )

    chat_metadata = await mta_collection.find_one({'chat_id': chat_id})
    if chat_metadata and chat_metadata.get('unread_user_id') == user.id:
        mta_id = chat_metadata.get('_id')
        await mta_collection.update_one(
            {"_id": mta_id}, 
            {"$set": {"unread_count": 0, "unread_user_id": ""}}
        )

    messages = await msg_collection.find(
        {"chat_id": chat_id}
    ).to_list(100)

    return {"data": messages}

