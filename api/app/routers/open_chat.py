import datetime

from fastapi import (
    APIRouter, WebSocket, status, WebSocketDisconnect, Request, HTTPException
)

from ..req_resp_models import OpenChatInitSchema
from ..chat_tools.open_chat_manager import open_chat_manager
from ..utils.functions import get_redis_from_request
from ..redis import redis_key
from ..utils.typing import ChatUserList, ChatOwnersRef
from ..schemas import OpenChatUser


router = APIRouter(prefix="/open-chat")


@router.post(
    "/init", 
    status_code=status.HTTP_201_CREATED, 
    response_model=OpenChatInitSchema
)
async def create_new_open_chat(
    request: Request, data: OpenChatInitSchema,
):
    redis_c = get_redis_from_request(request)
    chat_data : ChatUserList | None = redis_c.hget(redis_key.chats, data.chat_id)
    chat_owners_ref : ChatOwnersRef | None = redis_c.get(redis_key.chat_owners_ref)

    if chat_data and chat_data.get(data.chat_id):
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Chat id already exists"
        )

    user_data = OpenChatUser(
        created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        is_owner=True,
        name=data.initiator_name,
        user_id=data.initiator_id
    )

    if chat_data:
        chat_data[data.chat_id] = [user_data.model_dump()]
    else:
        chat_data = {}
        chat_data[data.chat_id] = [user_data.model_dump()]

    if chat_owners_ref:
        chat_owners_ref[data.chat_id] = user_data.model_dump()
    else:
        chat_owners_ref = {}
        chat_owners_ref[data.chat_id] = user_data.model_dump()

    redis_c.hset(redis_key.chats, mapping=chat_data)
    redis_c.hset(redis_key.chat_owners_ref, mapping=chat_owners_ref)
    
    return data


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_open_chat(
    chat_id
):
    await open_chat_manager.delete_chat(chat_id)
    return ""


@router.websocket("/ws/{chat_id}/{user_id}")
async def open_chat_messages(
    websocket: WebSocket, chat_id: str, user_id: str
):
    await websocket.accept()
    try:
        while True:
            await open_chat_manager.on_new_message(websocket)
    except WebSocketDisconnect:
        await open_chat_manager.disconnect_user(websocket, chat_id, user_id)
