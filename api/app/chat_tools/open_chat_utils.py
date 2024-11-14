import asyncio

from fastapi import WebSocket

from ..req_resp_models import OpenChatMsgDataSchema
from ..utils.constants import open_chat_msg_type
from ..schemas import OpenChatUser, OpenChatRequestJoin
from ..utils.functions import get_redis_from_request, parse_json, get_chat_users_from_redis_or_none
from ..redis import redis_key


class OpenChatUtils:

    async def get_chat_data_or_msg_error(
        self, chat_id, websocket: WebSocket
    ) -> list[dict] | None:
        redis_c = get_redis_from_request(websocket)
        if (chat_data := redis_c.hget(redis_key.chats, chat_id)) == None:
            resp_data = {"msg": "Chat not found", "chat_id": chat_id, "type": open_chat_msg_type.error}
            await websocket.send_json(resp_data)
        else:
            return parse_json(chat_data)
    

    async def get_user_data_or_msg_error(
        self, chat_data: list[dict], user_id: str, websocket: WebSocket
    ):
        user_data = None
        for existing_user in chat_data:
            validated_data = OpenChatUser(**existing_user)
            if validated_data.user_id == user_id:
                user_data = validated_data
                break

        if not user_data:
            resp_data = {
                "msg": "You are not allowed to acess this chat. Ask to join first", 
                "type": open_chat_msg_type.not_allowed_user
            }
            await websocket.send_json(resp_data)
        else:
            return user_data
    

    def get_user_data_or_none(
            self, 
            webSocket: WebSocket, 
            chat_id, 
            user_id
    ):
        chat_users = get_chat_users_from_redis_or_none(get_redis_from_request(webSocket), chat_id)

        if not chat_users:
            return None

        for chat_user in chat_users:
            validated_data = OpenChatUser(**chat_user)
            if validated_data.user_id == user_id:
                return validated_data
        
        return None
    

    def is_chat_admin(
            self, 
            webSocket: WebSocket, 
            chat_id, 
            admin_id
    ):
        """check if the user is the chat admin"""
        chat_users = get_chat_users_from_redis_or_none(get_redis_from_request(webSocket), chat_id)

        if not chat_users:
            return False

        for chat_user in chat_users:
            validated_data = OpenChatUser(**chat_user)
            if validated_data.user_id == admin_id and validated_data.is_owner:
                return True
        
        return False


    async def broadcast_msg(
        self, websockets: list[WebSocket], data: dict
    ):
        await asyncio.gather(
            *[websocket.send_json(data) for websocket in websockets]
        )