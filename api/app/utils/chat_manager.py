import datetime

from fastapi import WebSocket, WebSocketException, status

from ..schemas import UserWithId, ChatMessage, ChatMetaData
from ..response_model import SocketDataSchema, ChatResponse
from .constants import socket_msg_type
from .db import get_db_from_request
from ..database import db_collection_names


class ChatManager:
    connected_user: dict[str, WebSocket] = {}

    async def manage_new_msg(self, user: UserWithId, websocket: WebSocket):
        data = await websocket.receive_json()
        parsed_data = SocketDataSchema(**data)

        if parsed_data.type == socket_msg_type.init:
            await self.init_user_connection(user.id, websocket)
        elif parsed_data.type == socket_msg_type.msg:
            if (not parsed_data.chat_id) or (not parsed_data.to_user_id):
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Invalid data format"
                )
            await self.manage_chat_message(user, parsed_data, websocket)


    async def init_user_connection(
        self, user_id: str, websocket: WebSocket
    ):
        if self.connected_user.get(user_id):
            sockets: list = self.connected_user[user_id]
            sockets.append(websocket)
            self.connected_user[user_id] = sockets
        else:
            self.connected_user[user_id] = [websocket]
        
        await websocket.send_text('Connected')
    

    async def manage_chat_message(
        self, user: UserWithId, data: SocketDataSchema, websocket: WebSocket
    ):
        await self.insert_new_text_chat_message(user, data, websocket)
        await self.insert_or_update_metadata(user, data, websocket)

        resp_data = ChatResponse(
            chat_id=data.chat_id,
            msg=data.data,
            sender_id=user.id
        )
        
        if(
            client_socket := self.connected_user.get(data.to_user_id)
        ):
            await client_socket.send_json(resp_data.model_dump())
        
        await websocket.send_json(resp_data.model_dump())


    async def insert_new_text_chat_message(
        self, user: UserWithId, data: SocketDataSchema, websocket: WebSocket
    ):
        db = get_db_from_request(websocket)
        chat_collection = db.get_collection(db_collection_names.chat_messages)

        msg_data = ChatMessage(
            chat_id=data.chat_id,
            sender_id=user.id,
            receiver_id=data.to_user_id,
            text=data.data
        )
        await chat_collection.insert_one(msg_data.model_dump())
    

    async def insert_or_update_metadata(
        self, user: UserWithId, data: SocketDataSchema, websocket: WebSocket
    ):
        db = get_db_from_request(websocket)
        metadata_collection = db.get_collection(db_collection_names.chat_metadata)

        if(
            existed_metadata := await metadata_collection.find_one({"chat_id": data.chat_id})
        ):
            object_id = existed_metadata.get('_id')
            await metadata_collection.update_one(
                {"_id": object_id}, 
                {"$set": {
                    "unread_count": int(existed_metadata.get('unread_count')) + 1,
                    "unread_user_id": data.to_user_id, "last_message": data.data,
                    "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }}
            )
        else:
            metadata = ChatMetaData(
                chat_id=data.chat_id,
                first_user_id=user.id,
                last_message=data.data,
                last_updated=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                second_user_id=data.to_user_id,
                unread_count=1,
                unread_user_id=data.to_user_id,
            )
            await metadata_collection.insert_one(metadata.model_dump())
    

    def disconnect_user(
        self, user_id: str, websocket: WebSocket
    ):
        if not self.connected_user.get(user_id):
            return

        websockets: list = self.connected_user[user_id]
        websockets.remove(websocket)

        if not len(websockets):
            del self.connected_user[user_id]

    
chat_manager = ChatManager()