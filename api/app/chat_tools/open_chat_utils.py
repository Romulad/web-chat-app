import asyncio

from fastapi import WebSocket

from ..req_resp_models import OpenChatMsgDataSchema
from ..utils.constants import open_chat_msg_type
from ..schemas import OpenChatUser, OpenChatRequestJoin
from ..utils.functions import get_redis_from_request, parse_json
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
        self, chat_data: list[OpenChatUser], user_id: str, websocket: WebSocket
    ):
        user_data = None
        for existing_user in chat_data:
            if existing_user.user_id == user_id:
                user_data = existing_user
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
            self, chats: dict[str, list[OpenChatUser]], 
            chat_id, user_id
    ):
        chat_users = chats.get(chat_id)

        if not chat_users:
            return None

        for chat_user in chat_users:
            if chat_user.user_id == user_id:
                return chat_user
        
        return None
    

    def get_user_request_or_none(
        self, data: OpenChatMsgDataSchema, user_requests: list[dict]
    ) -> dict | None:
        request = None
        for existing_request in user_requests:
            parsed_data = OpenChatRequestJoin(**existing_request)
            if (
                parsed_data.user_id == data.user_id
            ):
                request = existing_request
                break

        return request


    async def broadcast_msg(
        self, websockets: list[WebSocket], data: dict
    ):
        await asyncio.gather(
            *[websocket.send_json(data) for websocket in websockets]
        )