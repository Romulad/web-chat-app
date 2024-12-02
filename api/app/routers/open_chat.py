import datetime

from fastapi import (
    APIRouter, 
    WebSocket, 
    status, 
    WebSocketDisconnect, 
    Request, 
    HTTPException
)

from ..req_resp_models import OpenChatInitSchema
from ..chat_tools.open_chat_manager import open_chat_manager
from ..utils.functions import get_redis_from_request, parse_json, stringify
from ..redis import redis_key
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
    chat_data : str | None = redis_c.hget(redis_key.chats, data.chat_id)

    if chat_data:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Chat id already exists"
        )

    user_data = OpenChatUser(
        created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        is_owner=True,
        name=data.initiator_name,
        user_id=data.initiator_id
    ).model_dump()

    chat_users = [user_data]

    # add chat metadata to the owner data
    user_data["chat_name"] = data.chat_name

    redis_c.hset(redis_key.chats, data.chat_id, stringify(chat_users))
    redis_c.hset(redis_key.chat_owners_ref, data.chat_id, stringify(user_data))
    redis_c.hset(redis_key.chat_msgs, data.chat_id, stringify([]))

    return data


@router.delete("/{chat_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_open_chat(
    request: Request, chat_id: str, user_id: str
):
    redis_c = get_redis_from_request(request)
    chat_users = redis_c.hget(redis_key.chats, chat_id)
    chat_owner = redis_c.hget(redis_key.chat_owners_ref, chat_id)
    
    if not chat_users:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Chat can't be found"
        )
    
    owner_data = OpenChatUser(**parse_json(chat_owner))
    if owner_data.user_id != user_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "You need to be the creator of the chat to be able to delete it"
        )

    redis_c.hdel(redis_key.chats, chat_id)
    redis_c.hdel(redis_key.chat_owners_ref, chat_id)
    redis_c.hdel(redis_key.chat_msgs, chat_id)

    await open_chat_manager.manage_chat_deletion(chat_id, owner_data.user_id)

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
        await open_chat_manager.disconnect_websocket(websocket, chat_id, user_id)

